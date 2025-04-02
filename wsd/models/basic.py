from typing import List

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression

from wsd.models import JMDict, Token
from wsd.parsers import Entry


class JMDictWithBCRanking(JMDict):
    """A dictionary with the ranking function based on Binary Classification."""

    def __init__(self, ranking_model=None, **kwargs):
        super().__init__(**kwargs)
        self.vec = DictVectorizer()
        self.model = ranking_model
        if self.model is None:
            self.model = LogisticRegression()

    def _preprocess(self, X, y):
        flat_X, flat_y = [], []
        for doc, labels in zip(X, y):
            tokens = self.tokenize(doc)
            for token, label in zip(tokens, labels):
                candidates = self._lookup(token.lemma)
                for candidate in candidates:
                    feat = self._create_features(candidate, token)
                    flat_X.append(feat)
                    flat_y.append(label)
        return flat_X, flat_y

    def fit(self, X: list[list[Token]], y):
        flat_X, flat_y = self._preprocess(X, y)
        vec_X = self.vec.fit_transform(flat_X)
        self.model.fit(vec_X, flat_y)
        return self

    def _rank(self, candidates: list[Entry], context: Token):
        if len(candidates) == 0:
            return []
        f = []
        for candidate in candidates:
            f.append(self._create_features(candidate, context))
        X = self.vec.transform(f)
        preds = self.model.predict_proba(X)
        return sorted(candidates, key=lambda c: preds[candidates.index(c)][1])

    def _create_features(self, candidate, token):
        features = {
            'ke_pri': {p for k in candidate.k_ele for p in k.ke_pri},
            're_pri': {p for r in candidate.r_ele for p in r.re_pri},
        }
        keb = {k.keb for k in candidate.k_ele}
        reb = {r.reb for r in candidate.r_ele}
        features['keb.text'] = token.text in keb
        features['keb.lemma'] = token.lemma in keb
        features['reb.text'] = token.text in reb
        features['reb.lemma'] = token.lemma in reb
        return features
