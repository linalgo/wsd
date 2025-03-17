"""A collection of parsers for various data sources."""
# from .jmdict import *
# from .xlwsd import *
from .jmdict import Entry, JMDictParser
from .xlwsd import XLWSDParser

__all__=["Entry", "JMDictParser", "XLWSDParser"]
