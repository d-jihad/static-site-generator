import unittest

from src.textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)
        
    def test_text(self):
        node = TextNode("This is a text node", "bold")
        self.assertEqual(node.text, "This is a text node")
    
    def test_text_type(self):
        node = TextNode("This is a text node", "bold")
        self.assertEqual(node.text_type, "bold")
        
    def test_url(self):
        node = TextNode("This is a text node", "bold", "https://www.boot.dev")
        self.assertEqual(node.url, "https://www.boot.dev")
        
    def test_no_url(self):
        node = TextNode("This is a text node", "bold")
        self.assertEqual(node.url, None)

    def test_repr(self):
        node = TextNode("This is a text node", "bold")
        self.assertEqual(repr(node), "TextNode(text='This is a text node', text_type='bold', url=None)")
