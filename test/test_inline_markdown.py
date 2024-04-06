import unittest

from src.inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from src.textnode import TextNode, TextType

class TestInlineMarkdown(unittest.TestCase):

    def test_inline_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual([
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)
        ], new_nodes)

    def test_inline_bold(self):
        node = TextNode("This is text with a **bold word**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual([
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold word", TextType.BOLD),
        ], new_nodes)

    def test_inline_italic(self):
        node = TextNode("This is text with a *italic word*.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)

        self.assertEqual([
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic word", TextType.ITALIC),
            TextNode(".", TextType.TEXT),
        ], new_nodes)

    def test_extract_images(self):
        text = "This is a text with a ![a boot](https://www.boot.dev) and another ![another boot](https://www.boot.dev) image."
        images = extract_markdown_images(text)

        self.assertEqual(images, [
            TextNode("a boot", TextType.IMAGE, "https://www.boot.dev"),
            TextNode("another boot", TextType.IMAGE, "https://www.boot.dev")
        ])

    def text_extract_links(self):
        text = "This is a text with a [a boot](https://www.boot.dev) and another [another boot](https://www.boot.dev) link."
        links = extract_markdown_links(text)

        self.assertEqual(links, [
            TextNode("a boot", TextType.LINK, "https://www.boot.dev"),
            TextNode("another boot", TextType.LINK, "https://www.boot.dev")
        ])
