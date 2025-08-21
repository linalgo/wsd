# pylint: disable=invalid-name,consider-using-enumerate
"""A collection of utils."""
import os
import xml.etree.ElementTree as ET

from fugashi import Tagger  # pylint: disable=no-name-in-module
from linalgo.annotate import Filter, Pipeline, Sequence2SequenceTransformer
from linalgo.hub import BQClient

from wsd.parsers.jmdict import Token

tagger = Tagger('-Owakati')


def tokenize(text):
    """A simple tokenizer that also returns the start offset of tokens."""
    idx = 0
    for token in tagger(text):
        yield idx, token.surface
        idx += len(token.surface)


def retrieve_dataset():
    """Retrieve the dataset from BigQuery"""
    client = BQClient(os.getenv('LINHUB_TASK'), project='linalgo-infra')
    task = client.get_task()

    pipeline = Pipeline([
        Filter(exclude_annotation_fn=lambda a: a.annotator.model == 'MACHINE'),
        Filter(include_document_fn=lambda d: len(d.annotations) > 0),
        Sequence2SequenceTransformer(tokenize_fn=tokenize)
    ])
    X, y = pipeline.transform(task)
    return X, y


def save_dataset(X, y):
    """Save the dataset to the local disk."""
    root = ET.Element("root")

    for xx, yy in zip(X, y):
        doc = ET.SubElement(root, "document")
        content = tagger(''.join(xx))
        for token, ent_seq in zip(content, yy):
            ET.SubElement(
                doc,
                "token",
                lemma=token.feature.lemma or token.surface,
                pos=token.pos,
                ent_seq=ent_seq
            ).text = token.surface
    tree = ET.ElementTree(root)
    ET.indent(tree, space="\t", level=0)
    tree.write("dataset.xml", encoding='utf-8')


def load_dataset(filename: str) -> tuple[list[list[str]], list[list[str]]]:
    """Reads the dataset from an XML file.

    Parameters
    ----------
    filename : str
        The path to the XML file.

    Returns
    -------
    Tuple[List[List[str]], List[List[str]]]
        A tuple containing two lists:
        - X: A list of documents, where each document is a list of tokens (strings).
        - y: A list of labels, where each label is a list of ent_seq (strings).
    """
    tree = ET.parse(filename)
    root = tree.getroot()

    X, y = [], []
    for doc_element in root.findall("document"):
        doc_tokens: list[Token] = []
        doc_labels: list[str] = []
        for token_element in doc_element.findall("token"):
            doc_tokens.append(
                Token(
                    text=token_element.text,
                    lemma=token_element.get("lemma"),
                    pos=token_element.get("pos")
                )
            )
            ent_seq = token_element.get("ent_seq")
            if ent_seq == '':
                ent_seq = None
            doc_labels.append(ent_seq)
        X.append(doc_tokens)
        y.append(doc_labels)

    return X, y


def accuracy(y_pred, y_true):
    """Compute the accuracy between sequences."""
    c, N = 0, 0
    for i in range(len(y_true)):
        for j in range(len(y_true[i])):
            N += 1
            c += y_pred[i][j] == y_true[i][j]
    return c / N


__all__ = [
    'tokenize', 'retrieve_dataset', 'save_dataset', 'load_dataset', 'accuracy'
]
