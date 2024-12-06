from collections import defaultdict
from dataclasses import asdict, dataclass, field
import time
from typing import List
import tqdm

from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage
from langchain_core.prompts import HumanMessagePromptTemplate

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


class ClusterByMeaningModel:
    """Add a meaning id to every annotation."""

    def __init__(self, comparator):
        self.comparator = comparator

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
                pred = self.comparator.invoke(messages)
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
        self.probability = probability
    
    def invoke(self, X):
        return BinaryWSD(probability=self.probability)