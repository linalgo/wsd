import xml.etree.ElementTree as ET

from wsd.models import Candidate


def load_data(lang):
    clusters = f'data/training_datasets/semcor_{lang}/semcor_{lang}.gold.key.txt'
    data = f'data/training_datasets/semcor_{lang}/semcor_{lang}.data.xml'

    with open(clusters) as f:
        lines = f.readlines()
    m = {}
    for line in lines:
        items = line.split(' ')
        k = items[0]
        m[k] = items[1]

    tree = ET.parse(data)
    corpus = tree.getroot()
    X, y = [], []
    for text in corpus:
        for sentence in text:
            i = sentence.find('instance')
            if i is not None:
                lemma, pos = i.attrib['lemma'], i.attrib['pos']
                context = ' '.join(tok.text for tok in sentence)
                if lang == 'ja':
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