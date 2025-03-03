import xml.etree.ElementTree as ET
from dotenv import load_dotenv
import os
from linalgo.annotate.models import Document, Target, SelectorFactory, Annotation, Corpus, AnnotatorFactory, Task
from collections import defaultdict
from linalgo.hub.client import LinalgoClient
from lineval.utils import Body


def xml_to_dicts(lang: str, clusters: str, data: str)->list[dict]:
    """
    Load Semcor data from xml file and clusters file.

    Parameters
    ----------
    clusters : str
        Path to clusters file.
    data : str
        Path to data file.

    Returns
    -------
    list of dict
        List of dictionaries with the data.
    """
    with open(clusters) as f:
        lines = f.readlines()
    m = {}
    for line in lines:
        items = line.split(' ')
        k = items[0]
        m[k] = items[1]

    tree = ET.parse(data)
    corpus = tree.getroot()

    dicts = []
    for text in corpus:
        for sentence in text:
            start,end = 0,0
            for wf in sentence:
                end = start + len(wf.text)
                if wf.tag == 'instance':
                    meaning = m[wf.attrib['id']]
                    lemma = wf.attrib['lemma']
                    pos = wf.attrib['pos']
                    context = ' '.join(wf.text for wf in sentence)
                    if lang == 'ja':
                        context = ''.join(wf.text for wf in sentence)
                    dicts.append({'lemma': lemma,
                                 'pos': pos,
                                 'context': context,
                                 'startContainer': '/',
                                 'endContainer': '/',
                                 'startOffset': start,
                                 'endOffset': end,
                                 'meaning': meaning,
                                 }
                                )
                if lang != 'ja':
                    end += 1
                start = end
    return dicts


def dicts_to_corpus(dicts : list[dict],
                    client: LinalgoClient,
                    corpus: Corpus,
                    task : Task,
                    )->Corpus:
    """
    Convert list of dictionaries to a corpus.

    Parameters
    ----------
    dicts : list of dict
        List of dictionaries with the Semcor data.
    client : LinalgoClient
        Linalgo client.
    corpus : Corpus
        Corpus object.
    task : str
        Task.

    Returns
    -------
    Corpus
        Corpus object with documents and annotations.
"""

    #getting the gold annotator
    gold_id = 'dcbb80f3-62cc-4334-9d23-960a76d059e4'
    url = f"https://linhub.api.linalgo.com/v1/annotators/{gold_id}"
    gold_dict = client.get(url=url)
    gold = AnnotatorFactory.from_dict(gold_dict)

    # group by pos/lemma
    grouped = defaultdict(list)
    for d in dicts:
        grouped[(d['pos'], d['lemma'])].append(d)
    items = grouped.items()

    docs = []
    for g, lst in items:
        contexts= "\n".join(d["context"] for d in lst)
        doc = Document(content = contexts,
                       corpus=corpus
        )
        doc_annos = []
        offset = 0
        for d in lst:
            d['startOffset'] += offset
            d['endOffset'] += offset
            offset += len(d['context']) + 2
            target = Target(source = doc,
                            selector = [SelectorFactory.factory(d)]
                            )
            anno = Annotation(document=doc,
                              entity=d['meaning'],
                              body=Body(text=d['lemma'], context=d['context']),
                              task=task,
                              annotator=gold,
                              target=target,
                              )

            doc_annos.append(anno)
        docs.append(doc)

    corpus.documents = docs
    return corpus


def load_corpus(lang, task_id, org_id, token):
    clusters = f'data/training_datasets/semcor_{lang}/semcor_{lang}.gold.key.txt'
    data = f'data/training_datasets/semcor_{lang}/semcor_{lang}.data.xml'
    dicts = xml_to_dicts(lang, clusters, data)
    url = "https://linhub.api.linalgo.com/v1"
    client = LinalgoClient(token, url)
    my_org = client.get_organization(org_id)
    task = client.get_task(task_id)
    corpus = Corpus(name=f'Semcor_{lang}',
                    description=f'The Semcor wsd corpus for {lang}',
                    organization=my_org)
    corpus = dicts_to_corpus(dicts, client, corpus, task)
    return corpus

if __name__ == "__main__":
    load_dotenv()
    token = os.getenv('LINHUB_TOKEN')
    url = "https://linhub.api.linalgo.com/v1"
    client = LinalgoClient(token, url)
    jack_org_id = "acf7a1aa-ec18-4fa2-a981-a756bc6e6af2"
    task_id = "635b8e9d-b590-4222-83a0-b46762a9fa58"
    jack_org = client.get_organization(jack_org_id)
    task = client.get_task(task_id)

    corpus = load_corpus("fr", task_id, jack_org_id, token)

    doc = corpus.documents[0]
    anno = list(doc.annotations)[0]
    annot = anno.annotator

    print(f"Corpus {corpus.name} has {len(corpus.documents)} documents")
    print("dtypes created:")
    print(f"""{task}
    {corpus}
    {doc}
    {annot}
    {anno}""")
