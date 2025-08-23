# pylint: disable=not-callable
"""A parser for the JMdict dictionary."""
import gzip
import os
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field

XML_NS = '{http://www.w3.org/XML/1998/namespace}'


@dataclass
class Kanji:
    """Kanji element."""
    keb: str = field(default_factory=str)
    ke_inf: list[str] = field(default_factory=list)
    ke_pri: list[str] = field(default_factory=list)
    id: int = field(default_factory=int)

    @classmethod
    def from_node(cls, node):
        """Create a Kanji object from an XML node."""
        keb = node.find('keb').text
        ke_inf = [k.text for k in node.findall('ke_inf')]
        ke_pri = [p.text for p in node.findall('ke_pri')]
        return cls(keb, ke_inf, ke_pri)


@dataclass
class Reading:
    """Reading element."""
    reb: str = field(default_factory=str)
    re_nokanji: bool = False
    re_restr: list[str] = field(default_factory=list)
    re_inf: list[str] = field(default_factory=list)
    re_pri: list[str] = field(default_factory=list)
    id: int = field(default_factory=int)

    @classmethod
    def from_node(cls, node):
        """Create a Reading object from an XML node."""
        reb = node.find('reb').text
        re_nokanji = bool(node.find('re_nokanji'))
        re_restr = [r.text for r in node.findall('re_restr')]
        re_inf = [r.text for r in node.findall('re_inf')]
        re_pri = [p.text for p in node.findall('re_pri')]
        return cls(reb, re_nokanji, re_restr, re_inf, re_pri)


@dataclass
class Gloss:
    """A gloss element."""
    text: str = field(default_factory=str)
    lang: str = field(default_factory=str)
    id: int = field(default_factory=int)

    @classmethod
    def from_node(cls, node):
        """Create a Gloss object from an XML node."""
        text = node.text
        lang = node.get(f'{XML_NS}lang')
        return cls(text, lang)


@dataclass
class Sense:
    """A sense element."""
    # pylint: disable=too-many-instance-attributes
    stagk: list[str] = field(default_factory=list)
    stagr: list[str] = field(default_factory=list)
    pos: list[str] = field(default_factory=list)
    xref: list[str] = field(default_factory=list)
    ant: list[str] = field(default_factory=list)
    field_: list[str] = field(default_factory=list)
    misc: list[str] = field(default_factory=list)
    s_inf: str = field(default_factory=str)
    lsource: list[str] = field(default_factory=list)
    dial: list[str] = field(default_factory=list)
    gloss: list[Gloss] = field(default_factory=list)
    id: int = field(default_factory=int)

    @classmethod
    def from_node(cls, node):
        """Create a Sense object from an XML node."""
        stagk = [s.text for s in node.findall('stagk')]
        stagr = [s.text for s in node.findall('stagr')]
        pos = [p.text for p in node.findall('pos')]
        xref = [x.text for x in node.findall('xref')]
        ant = [a.text for a in node.findall('ant')]
        field_ = [f.text for f in node.findall('field')]
        misc = [m.text for m in node.findall('misc')]
        s_inf_node = node.find('s_inf')
        s_inf = s_inf_node.text if s_inf_node is not None else None
        lsource = [lsource.text for lsource in node.findall('lsource')]
        dial = [d.text for d in node.findall('dial')]
        gloss = [Gloss.from_node(g) for g in node.findall('gloss')]
        return cls(stagk, stagr, pos, xref, ant, field_, misc, s_inf, lsource, dial, gloss)

    @classmethod
    def from_dict(cls, data):
        """Create a Sense object from a dictionary."""
        data['field_'] = data.pop('field')
        data['gloss'] = [Gloss(**g) for g in data.pop('glosses')]
        return cls(**data)


@dataclass
class Entry:
    """A dictionary entry."""
    ent_seq: str = field(default_factory=str)
    k_ele: list[Kanji] = field(default_factory=list)
    r_ele: list[Reading] = field(default_factory=list)
    sense: list[Sense] = field(default_factory=list)
    id: int = field(default_factory=int)

    @classmethod
    def from_node(cls, node):
        """Create an Entry object from an XML node."""
        ent_seq = node.find('ent_seq').text
        k_ele = [Kanji.from_node(k) for k in node.iter('k_ele')]
        r_ele = [Reading.from_node(r) for r in node.iter('r_ele')]
        senses = [Sense.from_node(s) for s in node.iter('sense')]
        return cls(ent_seq, k_ele, r_ele, senses)

    @classmethod
    def from_dict(cls, data):
        """Create an Entry object from a dictionary."""
        k_ele = [Kanji(**k) for k in data['kanjis']]
        r_ele = [Reading(**r) for r in data['readings']]
        senses = [Sense.from_dict(s) for s in data['senses']]
        return cls(data['ent_seq'], k_ele, r_ele, senses)

    def __hash__(self):
        return int(self.ent_seq)


# pylint: disable=too-few-public-methods
class JMDictParser:
    """A JMDICT parser."""

    @classmethod
    def parse(cls, file_path):
        """Parse a JMdict file."""
        if file_path is None:
            file_path = os.path.join(
                os.path.dirname(__file__), '../../data/JMdict_en.gz')
        entries = []
        with gzip.open(file_path, "rb") as f:  # pylint: disable=invalid-name
            tree = ET.parse(f)
            root = tree.getroot()
            for node in root.iter('entry'):
                entries.append(Entry.from_node(node))
        return entries


@dataclass
class Token:
    """Token dataclass."""
    text: str = ''
    lemma: str = ''
    pos: str = ''


__all__ = [
    'JMDictParser', 'Entry', 'Kanji', 'Reading', 'Gloss', 'Sense', 'Token'
]
