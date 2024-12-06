import xml.etree.ElementTree as ET

import pandas as pd

from wsd.models import Candidate


def load_data():
    clusters = 'data/training_datasets/semcor_ja/semcor_ja.gold.key.txt'
    data = 'data/training_datasets/semcor_ja/semcor_ja.data.xml'

    df = pd.read_csv(clusters, sep=' ', header=None, names=['key', 'sense'])
    records = df.to_dict(orient='records')
    m = {r['key']: r['sense'] for r in records}

    tree = ET.parse(data)
    corpus = tree.getroot()
    X, y = [], []
    for text in corpus:
        for sentence in text:
            i = sentence.find('instance')
            lemma, pos = i.attrib['lemma'], i.attrib['pos']
            context = ''.join(tok.text for tok in sentence)
            candidate = Candidate(
                text=i.text,
                lemma=lemma,
                pos=pos,
                context=context,
                example=context
            )
            X.append(candidate)
            y.append(m[i.attrib['id']])
    return X, y