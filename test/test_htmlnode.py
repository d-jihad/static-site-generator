import unittest

from src.htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("p", "This is a paragraph node", props={"class": "paragraph"})
        self.assertEqual(node.props_to_html(), 'class="paragraph"')


class TestLeafNode(unittest.TestCase):
    def test_paragraph_node(self):
        node = LeafNode("p", "This is a paragraph node", props={"class": "paragraph"})
        self.assertEqual(node.to_html(), '<p class="paragraph">This is a paragraph node</p>')

    def test_link_node(self):
        node = LeafNode("a", "This is a link node", props={"href": "https://www.boot.dev"})
        self.assertEqual(node.to_html(), '<a href="https://www.boot.dev">This is a link node</a>')

    def test_leaf_node_no_value(self):
        with self.assertRaises(ValueError):
            LeafNode("p", props={"class": "paragraph"})


class TestParentNode(unittest.TestCase):
    def test_paragraph_node(self):
        node = ParentNode(
            "p",
            children = [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
