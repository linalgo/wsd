# pylint: disable=not-callable
"""A parser for the JMdict dictionary."""
import gzip
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import List

XML_NS = '{http://www.w3.org/XML/1998/namespace}'


@dataclass
class Kanji:
    """Kanji element"""
    keb: str
    ke_inf: List[str] = field(default_factory=list)
    ke_pri: List[str] = field(default_factory=list)

    @classmethod
    def from_node(cls, node):
        """Create a Kanji object from an XML node"""
        keb = node.find('keb').text
        ke_inf = [k.text for k in node.findall('ke_inf')]
        ke_pri = [p.text for p in node.findall('ke_pri')]
        return cls(keb, ke_inf, ke_pri)


@dataclass
class Reading:
    """Reading element"""
    reb: str
    re_nokanji: bool = False
    re_restr: List[str] = field(default_factory=list)
    re_inf: List[str] = field(default_factory=list)
    re_pri: List[str] = field(default_factory=list)

    @classmethod
    def from_node(cls, node):
        """Create a Reading object from an XML node"""
        reb = node.find('reb').text
        re_nokanji = bool(node.find('re_nokanji'))
        re_restr = [r.text for r in node.findall('re_restr')]
        re_inf = [r.text for r in node.findall('re_inf')]
        re_pri = [p.text for p in node.findall('re_pri')]
        return cls(reb, re_nokanji, re_restr, re_inf, re_pri)


@dataclass
class Gloss:
    """A gloss element"""
    text: str
    lang: str = None

    @classmethod
    def from_node(cls, node):
        """Create a Gloss object from an XML node"""
        text = node.text
        lang = node.get(f'{XML_NS}lang')
        return cls(text, lang)


@dataclass
class Sense:
    """A sense element"""
    # pylint: disable=too-many-instance-attributes
    stagk: List[str] = field(default_factory=list)
    stagr: List[str] = field(default_factory=list)
    pos: List[str] = field(default_factory=list)
    xref: List[str] = field(default_factory=list)
    ant: List[str] = field(default_factory=list)
    field_: List[str] = field(default_factory=list)
    misc: List[str] = field(default_factory=list)
    s_inf: str = None
    lsource: List[str] = field(default_factory=list)
    dial: List[str] = field(default_factory=list)
    gloss: List[Gloss] = field(default_factory=list)

    @classmethod
    def from_node(cls, node):
        """Create a Sense object from an XML node"""
        stagk = [s.text for s in node.findall('stagk')]
        stagr = [s.text for s in node.findall('stagr')]
        pos = [p.text for p in node.findall('pos')]
        xref = [x.text for x in node.findall('xref')]
        ant = [a.text for a in node.findall('ant')]
        field_ = [f.text for f in node.findall('field')]
        misc = [m.text for m in node.findall('misc')]
        s_inf_node = node.find('s_inf')
        s_inf = s_inf_node.text if s_inf_node is not None else None
        lsource = [l.text for l in node.findall('lsource')]
        dial = [d.text for d in node.findall('dial')]
        gloss = [Gloss.from_node(g) for g in node.findall('gloss')]
        return cls(stagk, stagr, pos, xref, ant, field_, misc, s_inf, lsource, dial, gloss)


@dataclass
class Entry:
    """A dictionary entry"""
    ent_seq: str
    k_ele: List[Kanji] = field(default_factory=list)
    r_ele: List[Reading] = field(default_factory=list)
    sense: List[Sense] = field(default_factory=list)

    @classmethod
    def from_node(cls, node):
        """Create an Entry object from an XML node"""
        ent_seq = node.find('ent_seq').text
        k_ele = [Kanji.from_node(k) for k in node.iter('k_ele')]
        r_ele = [Reading.from_node(r) for r in node.iter('r_ele')]
        sense = [Sense.from_node(s) for s in node.iter('sense')]
        return cls(ent_seq, k_ele, r_ele, sense)


# pylint: disable=too-few-public-methods
class JMDictParser:
    """A JMDICT parser"""

    @classmethod
    def parse(cls, file_path):
        """Parse a JMdict file"""
        entries = []
        with gzip.open(file_path, "rb") as f:  # pylint: disable=invalid-name
            tree = ET.parse(f)
            root = tree.getroot()
            for node in root.iter('entry'):
                entries.append(Entry.from_node(node))
        return entries


__all__ = ['JMDictParser']
