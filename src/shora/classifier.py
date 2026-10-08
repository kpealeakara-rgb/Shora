"""Fast local classifier: TF-IDF (word + character n-grams) + logistic regression.

Two heads trained on NaijaScam:
  * binary   : scam vs legit
  * scam_type: 17-way type (9 scam types + 8 legit types)
Character n-grams make it robust to Pidgin spelling, missing Yoruba/Igbo diacritics and code-mixing.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import FeatureUnion, Pipeline

DEFAULT_MODEL_DIR = Path(__file__).resolve().parents[2] / "models" / "tfidf-logreg"


def _features() -> FeatureUnion:
    return FeatureUnion([
        ("word", TfidfVectorizer(analyzer="word", ngram_range=(1, 2), min_df=2, sublinear_tf=True, max_features=40000)),
        ("char", TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5), min_df=2, sublinear_tf=True, max_features=80000)),
    ])


def build_pipeline(C: float = 8.0) -> Pipeline:
    return Pipeline([("features", _features()),
                     ("clf", LogisticRegression(C=C, max_iter=3000, class_weight="balanced"))])


@dataclass
class Prediction:
    label: str
    scam_probability: float
    scam_type: str
    type_probability: float

    def to_dict(self):
        return self.__dict__.copy()


class ShoraClassifier:
    def __init__(self, binary: Pipeline, typer: Pipeline, meta: dict | None = None):
        self.binary, self.typer, self.meta = binary, typer, meta or {}

    @classmethod
    def train(cls, texts, labels, types, C: float = 8.0) -> "ShoraClassifier":
        b = build_pipeline(C).fit(texts, labels)
        t = build_pipeline(C).fit(texts, types)
        return cls(b, t, {"n_train": len(texts), "C": C})

    def predict(self, text: str) -> Prediction:
        return self.predict_many([text])[0]

    def predict_many(self, texts) -> list[Prediction]:
        pb = self.binary.predict_proba(texts)
        scam_idx = list(self.binary.classes_).index("scam")
        pt = self.typer.predict_proba(texts)
        out = []
        for i in range(len(texts)):
            p = float(pb[i][scam_idx])
            ti = pt[i].argmax()
            out.append(Prediction("scam" if p >= 0.5 else "legit", p, str(self.typer.classes_[ti]), float(pt[i][ti])))
        return out

    def save(self, model_dir: Path = DEFAULT_MODEL_DIR):
        model_dir = Path(model_dir)
        model_dir.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.binary, model_dir / "binary.joblib", compress=3)
        joblib.dump(self.typer, model_dir / "scam_type.joblib", compress=3)
        (model_dir / "meta.json").write_text(json.dumps(self.meta, indent=2))

    @classmethod
    def load(cls, model_dir: Path = DEFAULT_MODEL_DIR) -> "ShoraClassifier":
        model_dir = Path(model_dir)
        meta = json.loads((model_dir / "meta.json").read_text()) if (model_dir / "meta.json").exists() else {}
        return cls(joblib.load(model_dir / "binary.joblib"), joblib.load(model_dir / "scam_type.joblib"), meta)
