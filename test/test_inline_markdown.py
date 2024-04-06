import unittest

from src.inline_markdown import split_nodes_delimiter, extract_markdown_with_url, split_nodes_with_url, \
    text_to_textnodes
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

    def test_extract_markdown_image(self):
        text = "This is a text with a ![a boot](https://www.boot.dev) and another ![another boot](https://www.boot.dev) image."
        images = extract_markdown_with_url(text, TextType.IMAGE)

        self.assertEqual(images, [
            TextNode("a boot", TextType.IMAGE, "https://www.boot.dev"),
            TextNode("another boot", TextType.IMAGE, "https://www.boot.dev")
        ])

    def test_extract_markdown_link(self):
        text = "This is a text with a [a boot](https://www.boot.dev) and another [another boot](https://www.boot.dev) link."
        links = extract_markdown_with_url(text, TextType.LINK)

        self.assertEqual(links, [
            TextNode("a boot", TextType.LINK, "https://www.boot.dev"),
            TextNode("another boot", TextType.LINK, "https://www.boot.dev"),
        ])

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_with_url([node], TextType.IMAGE)

        self.assertEqual(new_nodes, [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE,
                     "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
            )
        ])

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with an [boot](https://www.boot.dev) and another [another boot](https://www.boot.dev) link.",
            TextType.TEXT
        )

        new_nodes = split_nodes_with_url([node], TextType.LINK)

        self.assertEqual(new_nodes, [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("boot", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("another boot", TextType.LINK, "https://www.boot.dev"),
            TextNode(" link.", TextType.TEXT)
        ])

    def test_text_to_textnodes(self):
        text = 'This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)'
        nodes = text_to_textnodes(text)

        self.assertEqual(nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE,
                     "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ])
