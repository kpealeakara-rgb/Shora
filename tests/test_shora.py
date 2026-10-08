import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from shora import analyze, find_red_flags, heuristic_score  # noqa: E402
from shora.benchmark import load_split, score  # noqa: E402
from shora.classifier import ShoraClassifier  # noqa: E402
from shora.taxonomy import LANGUAGES, LEGIT_TYPES, SCAM_TYPES  # noqa: E402

DATA = ROOT / "data" / "naijascam"
FIELDS = {"id", "text", "label", "scam_type", "language", "red_flags", "source", "generator"}


@pytest.mark.parametrize("split", ["train", "validation", "test"])
def test_dataset_schema(split):
    rows = load_split(split)
    assert len(rows) > 100
    for r in rows:
        assert FIELDS <= set(r)
        assert r["label"] in ("scam", "legit")
        assert r["language"] in LANGUAGES
        assert r["scam_type"] in SCAM_TYPES or r["scam_type"] in LEGIT_TYPES
        assert (r["label"] == "scam") == (r["scam_type"] in SCAM_TYPES)
        assert isinstance(r["red_flags"], list)
        if r["label"] == "scam":
            assert r["red_flags"], r["id"]


def test_test_split_is_held_out():
    train = {r["text"] for r in load_split("train") + load_split("validation")}
    test = {r["text"] for r in load_split("test")}
    assert not train & test


def test_rules_flag_otp_request():
    flags = {f["key"] for f in find_red_flags("Please send the OTP we just sent to you to unblock your BVN, bit.ly/xyz")}
    assert "asks_secret" in flags and "short_link" in flags
    assert heuristic_score("Your OTP is 482915. Do not share this code with anyone.") < 0.5


def test_score_perfect():
    rows = [{"label": "scam", "language": "en", "scam_type": "sim_swap"},
            {"label": "legit", "language": "pcm", "scam_type": "legit_otp"}]
    res = score(rows, ["scam", "legit"])
    assert res["accuracy"] == 1.0 and res["macro_f1"] == 1.0


def test_tiny_classifier_trains_and_predicts():
    texts = ["send your OTP now to unblock BVN", "abeg send the PIN make I unblock am", "10% daily profit AI trading",
             "Mama I don reach school", "Your order has been delivered", "Acct debited NGN5,000 Avail Bal NGN20,000"] * 3
    labels = ["scam"] * 3 + ["legit"] * 3
    labels = labels * 3
    types = ["bank_impersonation_otp", "bank_impersonation_otp", "ponzi_crypto",
             "legit_family_chat", "legit_delivery", "legit_bank_alert"] * 3
    clf = ShoraClassifier.train(texts, labels, types, C=4)
    assert clf.predict("send OTP to unblock your BVN").label == "scam"


def test_analyze_offline_returns_explanation():
    r = analyze("Congratulations! FG grant of N250,000. Pay N2,000 activation fee to claim: fg-grant.xyz", "pcm",
                use_llm=False)
    assert r["verdict"] in ("scam", "suspicious", "legit")
    assert r["what_to_do"]
    assert r["engine"] == "local"


@pytest.mark.skipif(not (ROOT / "models" / "tfidf-logreg" / "binary.joblib").exists(), reason="baseline not trained")
def test_trained_baseline_sanity():
    clf = ShoraClassifier.load()
    assert clf.predict("Your BVN has been suspended. Send the OTP sent to your phone to reactivate.").label == "scam"
    assert clf.predict("Mummy good morning, we go come house this Sunday after church.").label == "legit"
