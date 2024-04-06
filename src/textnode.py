from dataclasses import dataclass
from typing import Optional

from src.htmlnode import LeafNode

@dataclass
class TextNode:
    text: str
    text_type: str
    url: Optional[str] = None


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


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: str):
    raise NotImplementedError
