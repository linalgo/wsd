# pylint: disable=no-name-in-module,too-few-public-methods
"""A simple dictionary interface for JMDict."""
import json
import os
import uuid
from dataclasses import asdict

import joblib
import tqdm
from fugashi import Tagger
from linalgo.annotate import Annotation, Annotator, Document, Entity, Task

from wsd.parsers.jmdict import Entry, Token
from wsd.models.retrievers import Retriever, LocalRetriever
from wsd.models.rankers import Candidate, Ranker, DummyRanker, \
    PointWiseRanker, GeminiRanker


class Dictionary:
    """A simple dictionary base class."""

    def __init__(
            self,
            retriever: Retriever = None,
            ranker: Ranker = None,
            annotator: Annotator = None
    ):
        self.retriever = retriever
        self.ranker = ranker or DummyRanker()
        self.annotator = annotator or Annotator(
            id=uuid.uuid3(uuid.NAMESPACE_URL, 'jmdict-v3').hex,
            name='jmdict-v3',
            model='MACHINE',
            entity=Entity(id=os.getenv('LINHUB_ENTITY')),
            task=Task(id=os.getenv('LINHUB_TASK'))
        )

    def search(self, text: str, context=None) -> list[Entry]:
        """Search for an entry by text and rank the results.

        Currently returns all entries that contain the text in either the kanji
        or reading.
        """
        return self.ranker.rank(self.retriever.retrieve(text), context)[0]

    def feeling_lucky(self, text: str, context=None) -> Entry:
        """Return the first entry found.

        Currently returns the first entry that contains the text in either the
        kanji or reading.

        Parameters
        ----------
        text : str
            The text to search for

        Returns
        -------
        Entry
            The first entry that contains the query.
        """
        entries = self.search(text, context)
        return entries[0] if entries else None

    def annotate(
        self,
        documents: Document | list[Document],
        feeling_lucky=False
    ) -> list[Document]:
        """Annotate each token in a document with its (candidate) definitions.

        Parameters
        ----------
        doc : Document | List[Document]
            The documents to annotate.

        Returns
        -------
        Document | List[Document]
            The annotated documents.
        """
        if isinstance(documents, Document):
            documents = [documents]
        for doc in documents:
            start = 0
            for token in self.tokenize(doc.content):
                if feeling_lucky:
                    body = asdict(self.feeling_lucky(token.feture.lemma))
                else:
                    entries = self.search(token.feature.lemma)
                    body = [asdict(entry) for entry in entries]
                if body is not None:
                    a = Annotation(
                        document=doc,
                        body=json.dumps(
                            body, ensure_ascii=False).encode('utf-8'),
                        start=start,
                        end=start + len(token.surface),
                        annotator=self.annotator,
                        entity=self.annotator.entity,
                        task=self.annotator.task
                    )
                    doc.annotations.add(a)
                start += len(token.surface)
        if len(documents) == 1:
            return documents[0]
        return documents

    def tokenize(self, sentence: str) -> list[Token]:
        """Tokenize a sentence.
        Parameters
        ----------
        sentence : str
            The sentence to tokenize

        Returns
        -------
        List[Token]
            A list of tokens.
        """
        tagger = Tagger('-Owakati')
        tokens = []
        for token in tagger(sentence):
            tokens.append(
                Token(
                    text=token.surface,
                    lemma=token.feature.lemma,
                    pos=token.pos
                )
            )
        return tokens

    def fit(self, X: list[list[str]], y: list[list[str]]):
        """Fit the ranker.

        Parameters
        ----------
        X : list[list[Token]]
            The tokenized documents to 'featurize'.
        y : list[list[str]]
            The list of list of labels for each tokens in the X sentences.

        Returns
        -------
        self
            The fitted dictionary.
        """
        XX = []
        for doc in X:
            xx = []
            for token in doc:
                candidates = []
                for candidate in self.retriever.retrieve(token.lemma):
                    candidates.append(Candidate(candidate, token))
                xx.append(candidates)
            XX.append(xx)
        self.ranker.fit(XX, y)
        return self

    def predict(self, sentences: list[str | Token]) -> list[str]:
        """Predict the `ent_seq` for each token in a sentence.

        Parameters
        ----------
        sentences : Union[str, List[str]]
            The sentences to parse and query with the dictionary

        Returns
        -------
        preds : List[str]
            A list of predicted `ent_seq`.
        """
        if not hasattr(sentences, '__len__'):
            sentences = [sentences]
        preds = []
        for sentence in tqdm.tqdm(sentences):
            pred = []
            if isinstance(sentence, str):
                sentence = self.tokenize(sentence)
            for token in sentence:
                context = {'sentence': sentence, 'token': token}
                entry = self.feeling_lucky(token.lemma, context)
                ent_seq = entry.ent_seq if entry else None
                pred.append(ent_seq)
            preds.append(pred)
        return preds


class JMDict(Dictionary):
    """A simple dictionary interface for JMDict."""

    def __init__(self, retriever='local', ranker='dummy', file=None, *args, **kwargs):
        if retriever == 'local':
            retriever = LocalRetriever(file)
        elif isinstance(retriever, Retriever):
            pass
        else:
            raise ValueError(f"Invalid retriever: {retriever}")
        if ranker == 'dummy':
            ranker = DummyRanker()
        elif ranker == 'pointwise':
            ranker = PointWiseRanker()
        elif ranker == 'gemini':
            ranker = GeminiRanker()
        elif isinstance(ranker, Ranker):
            ranker.tokenize = self.tokenize
        else:
            raise ValueError(f"Invalid ranker: {ranker}")
        super().__init__(retriever, ranker, *args, **kwargs)

    def save(self, path: str):
        """Save the dictionary to a file."""
        joblib.dump({'retriever': self.retriever, 'ranker': self.ranker}, path)

    @classmethod
    def load(cls, path: str):
        """Load the dictionary from a file."""
        o = joblib.load(path)
        return cls(retriever=o['retriever'], ranker=o['ranker'])


__all__ = [
    'Dictionary', 'DummyRanker', 'JMDict', 'Ranker', 'Retriever', 'Token'
]
