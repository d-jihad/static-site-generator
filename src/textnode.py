from typing import Optional

from src.htmlnode import LeafNode


class TextNode:
    def __init__(self, text: str, text_type: str, url: Optional[str] = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value) -> bool:
        return (
                type(self) == type(value) and
                self.text == value.text and
                self.text_type == value.text_type and
                self.url == value.url
        )

    def __repr__(self) -> str:
        return f'TextNode({self.text}, {self.text_type}, {self.url})'


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case "bold":
            return LeafNode("b", text_node.text)
        case "italic":
            return LeafNode("i", text_node.text)
        case "code":
            return LeafNode("code", text_node.text)
        case "link":
            return LeafNode("a", text_node.text, props={"href": text_node.url})
        case "image":
            return LeafNode("img", props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError("Invalid text type")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    raise NotImplementedError
