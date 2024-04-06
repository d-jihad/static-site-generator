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


def url_type_to_regex(text_type: TextType) -> str:
    match text_type:
        case TextType.LINK:
            return InlineRegexes.LINK
        case TextType.IMAGE:
            return InlineRegexes.IMAGE
        case _:
            raise ValueError("Invalid with url type")


def extract_markdown_with_url(text: str, text_type: TextType):
    regex = url_type_to_regex(text_type)
    matches = re.finditer(regex, text)

    elements = []
    for match in matches:
        elements.append(TextNode(match.group(2), text_type, match.group(3)))
    return elements

def url_type_format(node: TextNode) -> str:
    match node.text_type:
        case TextType.LINK:
            return f"[{node.text}]({node.url})"
        case TextType.IMAGE:
            return f"![{node.text}]({node.url})"
        case _:
            raise ValueError("Invalid with url type")


def split_nodes_with_url(old_nodes, to_extract: TextType):
    new_nodes = []
    for node in old_nodes:
        original_text = node.text
        elements = extract_markdown_with_url(original_text, to_extract)
        if not elements:
            new_nodes.append(node)
        for el in elements:
            el_match = url_type_format(el)
            split_text = original_text.split(el_match, 1)

            if len(split_text) >= 1:
                new_nodes.append(TextNode(split_text[0], node.text_type))

            new_nodes.append(el)
            original_text = original_text[len(split_text[0]) + len(el_match):]

        if original_text:
            new_nodes.append(TextNode(original_text, node.text_type))

    return new_nodes


def text_to_textnodes(text: str):
    root = TextNode(text, TextType.TEXT)
    to_process = [root]
    processed = []

    while to_process:
        node = to_process.pop(0)
        if node.text_type == TextType.TEXT:
            if re.search(InlineRegexes.BOLD, node.text):
                to_process.extend(split_nodes_delimiter([node], "**", TextType.BOLD))
            elif re.search(InlineRegexes.ITALIC, node.text):
                to_process.extend(split_nodes_delimiter([node], "*", TextType.ITALIC))
            elif re.search(InlineRegexes.CODE, node.text):
                to_process.extend(split_nodes_delimiter([node], "`", TextType.CODE))
            # image before link, because link regex is a subset of image regex
            elif re.search(InlineRegexes.IMAGE, node.text):
                to_process.extend(split_nodes_with_url([node], TextType.IMAGE))
            elif re.search(InlineRegexes.LINK, node.text):
                to_process.extend(split_nodes_with_url([node], TextType.LINK))
            else:
                processed.append(node)
        else:
            processed.append(node)

    return processed

