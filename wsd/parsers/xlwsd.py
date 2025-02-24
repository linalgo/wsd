import zipfile 

import xml.etree.ElementTree as ET


class XLWSDParser:

    @staticmethod
    def parse(lang):
        zf = zipfile.ZipFile('../data/xl-wsd-data.zip', 'r')
        base_dir = f'xl-wsd/training_datasets/semcor_{lang}'
        labels = f'{base_dir}/semcor_{lang}.gold.key.txt'
        corpus = f'{base_dir}/semcor_{lang}.data.xml'

        m = {}
        with zf.open(labels, 'r') as f:
            for line in f:
                k, v = line.decode('utf-8').strip().split(' ')
                m[k] = v

        X, y = [], []
        with zf.open(corpus, 'r') as f:
            tree = ET.parse(f)
            corpus = tree.getroot()
            for text in corpus:
                for sentence in text:
                    i = sentence.find('instance')
                    lemma, pos = i.attrib['lemma'], i.attrib['pos']
                    X.append([tok.text for tok in sentence])
                    y.append((lemma, pos, m.get(i.attrib['id'])))
        return X, y

__all__ = ['XLWSDParser']
