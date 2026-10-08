/* Shora in-browser engine: a faithful re-implementation of the shipped sklearn pipeline
   FeatureUnion[TfidfVectorizer(word, 1-2), TfidfVectorizer(char_wb, 2-5)] -> LogisticRegression
   plus the regex red-flag rules from src/shora/rules.py. Pure JS, no dependencies. Nothing is sent anywhere. */
(function (root) {
  "use strict";

  // Python str.split() / \s whitespace set
  var WS = " \\t\\n\\r\\f\\v\\x1c-\\x1f\\x85\\xa0\\u1680\\u2000-\\u200a\\u2028\\u2029\\u202f\\u205f\\u3000";
  var RE_SPLIT = new RegExp("[" + WS + "]+", "u");
  var RE_MULTI_WS = new RegExp("[" + WS + "][" + WS + "]+", "gu");      // sklearn _white_spaces = \s\s+
  var RE_TOKEN = /[\p{L}\p{N}_]{2,}/gu;                                  // (?u)\b\w\w+\b

  function b64ToInt16(b64) {
    var bin = typeof atob === "function" ? atob(b64) : Buffer.from(b64, "base64").toString("binary");
    var n = bin.length >> 1, out = new Int16Array(n);
    for (var i = 0; i < n; i++) {
      var v = bin.charCodeAt(2 * i) | (bin.charCodeAt(2 * i + 1) << 8);
      out[i] = v > 32767 ? v - 65536 : v;
    }
    return out;
  }

  function Engine(M) {
    this.M = M;
    this.offset = { word: 0, char: M.word.vocab.length };
    this.nFeat = M.word.vocab.length + M.char.vocab.length;
    var self = this;
    ["word", "char"].forEach(function (k) {
      var v = M[k], map = new Map(), idf = new Float64Array(v.vocab.length);
      for (var i = 0; i < v.vocab.length; i++) {
        map.set(v.vocab[i], i);
        idf[i] = Math.log((1 + M.n) / (1 + v.df[i])) + 1;
      }
      self[k] = { map: map, idf: idf, ngram: v.ngram };
    });
    function head(h) {
      var q = b64ToInt16(h.coef), K = h.classes.length, F = self.nFeat;
      var W = new Float64Array(K * F);
      for (var c = 0; c < K; c++) for (var j = 0; j < F; j++) W[c * F + j] = q[c * F + j] * h.scales[c];
      return { W: W, b: h.intercept, classes: h.classes, K: K };
    }
    this.bin = head(M.binary);
    this.typ = head(M.type);
    this.rules = M.rules.map(function (r) {
      return { key: r.key, flag: r.flag, weight: r.weight, re: new RegExp(r.re, "iu") };
    });
    this.safe = M.safe_hints.map(function (s) { return new RegExp(s, "iu"); });
  }

  Engine.prototype._wordTerms = function (doc) {
    var toks = doc.match(RE_TOKEN) || [], out = toks.slice();
    for (var i = 0; i + 1 < toks.length; i++) out.push(toks[i] + " " + toks[i + 1]);
    return out;
  };

  Engine.prototype._charTerms = function (doc) {
    doc = doc.replace(RE_MULTI_WS, " ");
    var words = doc.split(RE_SPLIT), out = [];
    var lo = this.char.ngram[0], hi = this.char.ngram[1];
    for (var wi = 0; wi < words.length; wi++) {
      if (!words[wi]) continue;
      var w = Array.from(" " + words[wi] + " "), L = w.length;   // code points, like Python
      for (var n = lo; n <= hi; n++) {
        var off = 0;
        out.push(w.slice(0, n).join(""));
        while (off + n < L) { off++; out.push(w.slice(off, off + n).join("")); }
        if (off === 0) break;
      }
    }
    return out;
  };

  // sparse l2-normalised tf-idf block: returns [[globalIndex, value], ...]
  Engine.prototype._block = function (kind, terms) {
    var V = this[kind], counts = new Map();
    for (var i = 0; i < terms.length; i++) {
      var idx = V.map.get(terms[i]);
      if (idx !== undefined) counts.set(idx, (counts.get(idx) || 0) + 1);
    }
    var vals = [], ss = 0;
    counts.forEach(function (tf, idx) {
      var v = (1 + Math.log(tf)) * V.idf[idx];
      vals.push([idx, v]); ss += v * v;
    });
    var norm = Math.sqrt(ss), off = this.offset[kind];
    return vals.map(function (p) { return [p[0] + off, norm > 0 ? p[1] / norm : 0]; });
  };

  Engine.prototype.features = function (text) {
    var doc = String(text || "").toLowerCase();
    return this._block("word", this._wordTerms(doc)).concat(this._block("char", this._charTerms(doc)));
  };

  function scores(h, x, F) {
    var z = new Array(h.K);
    for (var c = 0; c < h.K; c++) {
      var s = h.b[c], base = c * F;
      for (var i = 0; i < x.length; i++) s += h.W[base + x[i][0]] * x[i][1];
      z[c] = s;
    }
    return z;
  }

  Engine.prototype.redFlags = function (text) {
    text = String(text || "");
    var out = [];
    for (var i = 0; i < this.rules.length; i++) {
      var r = this.rules[i], m = r.re.exec(text);
      if (m) out.push({ key: r.key, flag: r.flag, evidence: Array.from(m[0]).slice(0, 60).join(""), weight: r.weight });
    }
    return out;
  };

  Engine.prototype.heuristic = function (text, flags) {
    var s = 0;
    flags = flags || this.redFlags(text);
    for (var i = 0; i < flags.length; i++) s += flags[i].weight;
    for (var j = 0; j < this.safe.length; j++) if (this.safe[j].test(String(text || ""))) { s -= 1.5; break; }
    return Math.max(0, Math.min(1, s / 5));
  };

  Engine.prototype.predict = function (text) {
    var x = this.features(text), F = this.nFeat;
    var zb = scores(this.bin, x, F)[0];
    var pScam = 1 / (1 + Math.exp(-zb));                        // classes = [legit, scam]
    var zt = scores(this.typ, x, F), mx = Math.max.apply(null, zt), sum = 0;
    var pt = zt.map(function (z) { var e = Math.exp(z - mx); sum += e; return e; }).map(function (e) { return e / sum; });
    var ti = 0;
    for (var c = 1; c < pt.length; c++) if (pt[c] > pt[ti]) ti = c;
    var flags = this.redFlags(text), h = this.heuristic(text, flags);
    var risk = 0.8 * pScam + 0.2 * h;                            // same blend as shora.analyze.local_pass
    return {
      label: pScam >= 0.5 ? "scam" : "legit",
      scam_probability: pScam,
      scam_type: this.typ.classes[ti],
      type_probability: pt[ti],
      red_flags: flags,
      heuristic: h,
      risk: risk,
      verdict: risk >= 0.6 ? "scam" : (risk >= 0.35 ? "suspicious" : "legit")
    };
  };

  var api = { Engine: Engine };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.Shora = api;
})(typeof self !== "undefined" ? self : this);
