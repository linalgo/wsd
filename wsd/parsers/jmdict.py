import gzip
import xml.etree.ElementTree as ET


xml = '{http://www.w3.org/XML/1998/namespace}'


class Kanji:
    def __init__(self, node):
        self.keb = node.find('keb').text  # Searchable
        self.ke_inf = [k.text for k in node.findall('ke_inf')]
        self.ke_pri = [p.text for p in node.findall('ke_pri')]  # Filter

    def to_dict(self):
        d = {
            'keb': self.keb,
            'ke_inf': self.ke_inf,
            'ke_pri': self.ke_pri,
        }
        return d

    def __repr__(self):
        return str(self.to_dict())


class Reading:
    def __init__(self, node):
        self.reb = node.find('reb').text  # Searchable
        self.re_nokanji = bool(node.find('re_nokanji'))
        self.re_restr = [r.text for r in node.findall('re_restr')]
        self.re_inf = [r.text for r in node.findall('re_inf')]
        self.re_pri = [p.text for p in node.findall('re_pri')]  # Filter

    def to_dict(self):
        d = {
            'reb': self.reb,
            're_nokanji': self.re_nokanji,
            're_restr': self.re_restr,
            're_inf': self.re_inf,
            're_pri': self.re_pri,
        }
        return d

    def __repr__(self):
        return str(self.to_dict())


class Gloss:
    def __init__(self, node):
        self.text = node.text  # Searchable
        self.lang = node.get(f'{xml}lang')  # Filter

    def to_dict(self):
        d = {
            'text': self.text,
            'lang': self.lang
        }
        return d

    def __repr__(self):
        return str(self.to_dict())


class Sense:
    def __init__(self, node):
        self.stagk = [s.text for s in node.findall('stagk')]
        self.stagr = [s.text for s in node.findall('stagr')]
        self.pos = [p.text for p in node.findall('pos')]  # Filter
        self.xref = [x.text for x in node.findall('xref')]
        self.ant = [a.text for a in node.findall('ant')]
        self.field = [f.text for f in node.findall('field')]
        self.misc = [m.text for m in node.findall('misc')]
        self.s_inf = node.find('s_inf')
        self.lsource = [l.text for l in node.findall('lsource')]
        self.dial = [d.text for d in node.findall('dial')]
        self.gloss = [Gloss(g) for g in node.findall('gloss')]  # Searchable
        
        if self.s_inf is not None:
            self.s_inf = self.s_inf.text

    def to_dict(self):
        d = {
            'stagk': self.stagk,
            'stagr': self.stagr,
            'pos': self.pos,
            'xref': self.xref,
            'ant': self.ant,
            'field': self.field,
            'misc': self.misc,
            'lsource': self.lsource,
            'dial': self.dial,
            'gloss': [g.to_dict() for g in self.gloss]
        }
        if hasattr(self, 's_inf'):
            d['s_inf'] = self.s_inf
        return d

    def __repr__(self):
        return str(self.to_dict())
        

class Entry:

    def __init__(self, node):
        self.ent_seq = node.find('ent_seq').text
        self.k_ele = [Kanji(k) for k in node.iter('k_ele')]  # Searchable
        self.r_ele = [Reading(r) for r in node.iter('r_ele')]  # Searchable
        self.sense = [Sense(s) for s in node.iter('sense')]  # Searchable

    def to_dict(self):
        d = {
            'ent_seq': self.ent_seq,
            'r_ele': [r.to_dict() for r in self.r_ele],
            'sense': [s.to_dict() for s in self.sense]
        }
        if len(self.k_ele) > 0:
            d['k_ele'] = [k.to_dict() for k in self.k_ele]
        return d

    def __repr__(self):
        return str(self.to_dict())


class JMdictParser(object):
    """
    A JMDICT parser
    """

    @classmethod
    def parse(cls, file_path):
        entries = []
        with gzip.open(file_path, "rb") as f:
            tree = ET.parse(f)
            root = tree.getroot()
            for node in root.iter('entry'):
                entries.append(Entry(node))
        return entries


__all__ = [JMdictParser]
