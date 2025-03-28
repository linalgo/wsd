# pylint: disable=invalid-name,too-few-public-methods,too-many-locals
"""Parser for the XL-WSD dataset."""
import os
import xml.etree.ElementTree as ET
import zipfile


class XLWSDParser:
    """Parser for the XL-WSD dataset."""

    @staticmethod
    def parse(lang):
        """Parse the XL-WSD dataset.

        Returns a sequence to sequence dataset, where the input is a list of
        words and the output is a list of (lemma, pos, sense) tuples. Since only
        one token in the sentence is annotated, the other tokens are marked with
        'O'.

        Parameters
        ----------
        lang : str
            The language to parse

        Returns
        -------
        X : List[Tuple[str]]
            The input sequences
        y : List[Tuple[str, str, str]]
            The output sequences
        """
        current_dir = os.path.dirname(__file__)
        filepath = os.path.join(current_dir, '../../data/xl-wsd-data.zip')
        zf = zipfile.ZipFile(filepath, 'r')  # pylint: disable=consider-using-with

        base_dir = f'xl-wsd/training_datasets/semcor_{lang}'
        labels = f'{base_dir}/semcor_{lang}.gold.key.txt'
        corpus = f'{base_dir}/semcor_{lang}.data.xml'

        m = {}
        with zf.open(labels, 'r') as f:
            for line in f:
                s = line.decode('utf-8').strip().split(' ')
                k, v = s[0], s[1:]
                m[k] = v

        X, y = [], []
        with zf.open(corpus, 'r') as f:
            tree = ET.parse(f)
            corpus = tree.getroot()
            for text in corpus:
                for sentence in text:
                    xx, yy = [], []
                    for tok in sentence:
                        xx.append(tok.text)
                        if tok.tag == 'wf':
                            yy.append(('O', 'O', 'O'))
                        elif tok.tag == 'instance':
                            lemma, pos = tok.attrib['lemma'], tok.attrib['pos']
                            yy.append((lemma, pos, m.get(tok.attrib['id'])))
                    X.append(xx)
                    y.append(yy)
        return X, y


__all__ = ['XLWSDParser']
