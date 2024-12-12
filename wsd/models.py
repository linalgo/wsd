import re
from collections import defaultdict
from dataclasses import asdict, dataclass, field
import time
from typing import List
import tqdm

from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage
from langchain_core.prompts import HumanMessagePromptTemplate


from linalgo.annotate.models import Annotator, Annotation, Document, Entity, Target
from etl.models import Candidate


chat_template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=(
                "You are a linguist working on word sense disambiguation.\n"
                "Compare the two words provided and return the probability "
                "that they have the same meaning."
            )
        ),
        HumanMessagePromptTemplate.from_template(
            "Do the two words below have the same semantic meaning in their respective contexts?\n"
            "word: {word1}; lemma: {lemma1}; context: {context1}\n"
            "word: {word2}; lemma: {lemma2}; context: {context2}"
        ),
    ]
)


class BinaryWSD(BaseModel):
    probability: float = Field(
        description="The probability that the two words have the same meaning."
    )


@dataclass
class Candidate:
    """Type for entries with their associated examples."""
    pos: str = field(default='NA')
    text: str = field(default='NA')
    lemma: str = field(default='NA')
    lemma_meaning: str = field(default='NA')
    example: str = field(default='NA')
    context: str = field(default='NA')
    document: str | Document = field(default='NA')


class ClusterByMeaningModel:
    """Add a meaning id to every annotation."""

    def __init__(self, comparator):
        self.comparator = comparator
        self.structured_comparator = comparator.with_structured_output(BinaryWSD)

    def predict(self, candidates: List[Candidate], verbose=False, sleep=0) -> List[int]:
        """Compares word meanings.

        Parameters
        ----------
        word_pairs: List[Candiate]
            A list of candidates to cluster by meaning.

        Returns
        -------
        preds: Iterable[float]
            Probabilities that each pair has the same meaning.
        """
        grouped_candidates = defaultdict(list)
        for c in candidates:
            grouped_candidates[(c.lemma, c.pos)].append(c)
        items = grouped_candidates.items()
        for g, cc in (tqdm.tqdm(items) if verbose else items):
            if len(cc) == 1:
                cc[0].lemma_meaning = hash((g, 0))
            else:
                self._predict(cc, sleep)
        y_pred = []
        for c in candidates:
            y_pred.append(hash((c.lemma, c.pos, c.lemma_meaning)))
        return y_pred

    def _predict(self, candidates: List[Candidate], sleep=0) -> List[int]:
        # pylint: disable=missing-function-docstring
        senses = defaultdict(dict)
        senses[0] = [candidates[0]]
        n = 0
        for candidate in candidates:
            time.sleep(sleep)
            matched = False
            for sid in senses:
                ref = senses[sid][0]
                messages = chat_template.format_messages(
                    word1=ref.text,
                    lemma1=ref.lemma,
                    context1=ref.context,
                    word2=candidate.text,
                    lemma2=candidate.lemma,
                    context2=candidate.context,
                )
                pred = self.structured_comparator.invoke(messages)
                if pred is None:
                    continue
                if pred.probability > 0.5:
                    senses[sid].append(candidate)
                    candidate.lemma_meaning = sid
                    matched = True
                    break
            if not matched:
                n += 1
                senses[n] = [candidate]
                candidate.lemma_meaning = n
        return candidates


class DummyComparator:
    def __init__(self, probability=1):
        self.model_name = f'Dummy={probability}'
        self.probability = probability

    def invoke(self, X):
        return BinaryWSD(probability=self.probability)

    def with_structured_output(self, x):
        return self


def get_data(text):
    contexts = re.findall((
        "------Context------\n"
        "(.+)\n"
        "-------------------"""),
        text
    )
    word = re.findall("Word: (.+)\n", text)[0]
    return word, contexts


class ClusterByMeaningAnnotator(ClusterByMeaningModel):

    def __init__(self, comparator):
        super().__init__(comparator)
        self.annotator = Annotator(
            id=hash(self.comparator.model_name),
            name=self.comparator.model_name
        )

    def predict(self, docs, verbose=False, sleep=0):
        candidates = []
        for doc in docs:
            word, contexts = get_data(doc.content)
            for i, context in enumerate(contexts):
                candidate = Candidate(
                    text=word,
                    lemma=word,
                    context=context,
                    example=context,
                    document=doc
                )
                candidate.offset = i
                candidates.append(candidate)

        super().predict(candidates, verbose, sleep)
        for candidate in candidates:
            annotation = Annotation(
                id=hash((self.comparator.model_name, candidate.text, candidate.context)),
                annotator=self.annotator,
                entity=Entity(id=candidate.lemma_meaning),
                document=doc,
                target=Target(source=candidate.document, selector=[{
                    'startContainer': '/',
                    'endContainer': '/',
                    'startOffset': candidate.offset,
                    'endOffset': 0
                }])
            )
            candidate.document.annotations.add(annotation)
        return docs
