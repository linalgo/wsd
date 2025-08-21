import unittest

from wsd.models import JMDict


class TestJMDict(unittest.TestCase):
    """Test the JMDict model."""

    def setUp(self):
        self.jmdict = JMDict()

    def test_jmdict(self):
        entries, _ = self.jmdict.search('日本語')
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].ent_seq, '1464530')
    
    def test_no_entry_found(self):
        entries, _ = self.jmdict.search('qwefasdfasg')
        self.assertEqual(len(entries), 0)


if __name__ == '__main__':
    unittest.main()