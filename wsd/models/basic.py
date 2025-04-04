# pylint: disable=invalid-name
"""A basic dictionary with ranking based on a binary classifier."""
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression

from wsd.models.baseline import JMDict, Token
from wsd.parsers import Entry


class JMDictWithPointWiseRanking(JMDict):
    """A dictionary with the ranking function based on Binary Classification."""

    def __init__(self, ranking_model=None, **kwargs):
        super().__init__(**kwargs)
        self.vec = DictVectorizer()
        self.model = ranking_model
        if self.model is None:
            self.model = LogisticRegression()

    def _preprocess(self, X: list[str], y: list[str]):
        """Create features for each candidate

        In the PointWise Binary Classification, the preprocessing just creates
        a dataset that has one row per candidate, with the label for the
        classification indicating whether the candidate is the best definition
        or not.

        Parameters
        ----------
        X : list[str]
            A list of sentences to tokenize and 'featurize'.
        y : list[str]
            The list of labels for each tokens in the X sentences.

        Returns
        -------
        flat_X : list[dict]
            A list of features. One per candidate per token for each sentence.
        flat_y : list[bool]
            Indicates whether the candidate is the best definition or not.
        """
        flat_X, flat_y = [], []
        for doc, labels in zip(X, y):
            tokens = self.tokenize(doc)
            for token, label in zip(tokens, labels):
                candidates = self._lookup(token.lemma)
                for candidate in candidates:
                    feat = self._create_features(candidate, token)
                    flat_X.append(feat)
                    flat_y.append(label == candidate.ent_seq)
        return flat_X, flat_y

    def fit(self, X: list[list[Token]], y: list[list[str]]):
        """Flatten the data and fit a binary classifier.

        Note: During the fitting process, a dataset is created with one row per
        candidate. This means that `flat_X` contains many more rows than `X`.
        """
        flat_X, flat_y = self._preprocess(X, y)
        vec_X = self.vec.fit_transform(flat_X)
        self.model.fit(vec_X, flat_y)
        return self

    # pylint: disable=signature-differs
    def _rank(self, candidates: list[Entry], context):
        """A basic ranking function using the score of the binary classifier.

        Parameters
        ----------
        candidates: List[Entry]
            The candidates to rank
        context : Any
            A contet to inform the ranking

        Returns
        -------
        candidates: List[Entry]
            The ranked candidates
        scores: List[float]
            The score of each candidate
        """
        if len(candidates) < 1:
            return [], []
        f = []
        for candidate in candidates:
            f.append(self._create_features(candidate, context['token']))
        X = self.vec.transform(f)
        preds = self.model.predict_proba(X)
        res = sorted(candidates, key=lambda c: -preds[candidates.index(c)][1])
        scores = sorted(preds[:, 1], reverse=True)
        return res, scores

    def _create_features(self, candidate, token):
        """Create a feature dictionary for a candidate."""
        features = {
            'ke_pri': {p for k in candidate.k_ele for p in k.ke_pri},
            're_pri': {p for r in candidate.r_ele for p in r.re_pri},
            'sense.length': len(candidate.sense),
        }
        keb = {k.keb for k in candidate.k_ele}
        reb = {r.reb for r in candidate.r_ele}
        features['keb.text'] = token.text in keb
        features['keb.lemma'] = token.lemma in keb
        features['reb.text'] = token.text in reb
        features['reb.lemma'] = token.lemma in reb
        return features


__all__ = ['JMDictWithPointWiseRanking']
