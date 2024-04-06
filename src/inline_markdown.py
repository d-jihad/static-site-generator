import re
from src.textnode import TextNode, TextType


class InlineRegexes:
    """Regular expressions for markdown delimiters."""
    BOLD = r"(\*\*(.*?)\*\*)"
    ITALIC = r"(\*(.*?)\*)"
    CODE = r"(`(.*?)`)"
    LINK = r"(\[(.*?)\]\((.*?)\))"
    IMAGE = r"(\!\[(.*?)\]\((.*?)\))"

def inline_to_regex(delimiter: str) -> str:
    match delimiter:
        case "**":
            return InlineRegexes.BOLD
        case "*":
            return InlineRegexes.ITALIC
        case "`":
            return InlineRegexes.CODE
        case _:
            raise ValueError("Invalid delimiter")


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []

    pattern = inline_to_regex(delimiter)

    for node in old_nodes:
        matches = re.finditer(pattern, node.text)
        start = 0
        line_nodes = []
        for match in matches:
            if match.start() > start:
                node_str = node.text[start:match.start()]
                line_nodes.append(TextNode(node_str, node.text_type))

            node_str = match.group(2)
            line_nodes.append(TextNode(node_str, text_type))

            start = match.end()

        if start < len(node.text):
            node_str = node.text[start:]
            line_nodes.append(TextNode(node_str, node.text_type))

        new_nodes.extend(line_nodes)

    return new_nodes


def extract_markdown_images(text: str):
    matches = re.finditer(InlineRegexes.IMAGE, text)
    images = []
    for match in matches:
        images.append(TextNode(match.group(2), TextType.IMAGE, match.group(3)))
    return images


def extract_markdown_links(text: str):
    matches = re.finditer(InlineRegexes.LINK, text)
    links = []
    for match in matches:
        links.append(TextNode(match.group(2), TextType.LINK, match.group(3)))
    return links
