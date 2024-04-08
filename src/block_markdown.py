from enum import Enum

from src.htmlnode import LeafNode, ParentNode
from src.inline_markdown import text_to_textnodes
from src.textnode import text_node_to_html_node


class BlockType(Enum):
    H1 = 1
    H2 = 2
    H3 = 3
    H4 = 4
    H5 = 5
    H6 = 6
    UL = "ul"
    OL = "ol"
    P = "p"
    CODE = "code"
    QUOTE = "blockquote"


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType .P:
        return paragraph_to_html_node(block)
    if block_type in (BlockType.H1, BlockType.H2, BlockType.H3, BlockType.H4, BlockType.H5, BlockType.H6):
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.OL:
        return olist_to_html_node(block)
    if block_type == BlockType.UL:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("Invalid block type")

def markdown_to_blocks(markdown: str):
    return list(filter(lambda b: b, map(lambda b: b.strip(), markdown.split("\n\n"))))


def heading_level(block: str) -> BlockType:
    if block.startswith("# "):
        return BlockType.H1
    elif block.startswith("## "):
        return BlockType.H2
    elif block.startswith("### "):
        return BlockType.H3
    elif block.startswith("#### "):
        return BlockType.H4
    elif block.startswith("##### "):
        return BlockType.H5
    elif block.startswith("###### "):
        return BlockType.H6
    else:
       return BlockType.P


def block_to_block_type(block: str) -> BlockType:
    if block.startswith("#"):
        return heading_level(block)
    elif block.startswith("* ") or block.startswith("- "):
        ol_type = block[0]
        for line in block.split("\n"):
            if not line.startswith(f"{ol_type} "):
                return BlockType.P
        return BlockType.UL
    elif block.startswith("1. "):
        for i, line in enumerate(block.split("\n")):
            if not line.startswith(f"{i + 1}. "):
                return BlockType.P
        return BlockType.OL
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif block.startswith("> "):
        for line in block.split("\n"):
            if not line.startswith(f"> "):
                return BlockType.P
        return BlockType.QUOTE
    else:
        return BlockType.P


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def heading_to_html_node(block: str):
    candidate_h = heading_level(block)
    if candidate_h == BlockType.P:
        return paragraph_to_html_node(block)

    level = candidate_h.value
    tag = f"h{level}"
    children = text_to_children(block[level + 1:])
    return ParentNode(tag, children)


def olist_to_html_node(block: str):
    html_items = []
    for line in block.split("\n"):
        text = line[2:].strip()
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))

    return ParentNode("ol", children=html_items)


def ulist_to_html_node(block: str):
    html_items = []
    for line in block.split("\n"):
        text = line[1:].strip()
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))

    return ParentNode("ul", children=html_items)


def code_to_html_node(block: str):
    code_text = "\n".join(block.split("\n")[1:-1])
    return ParentNode("pre", children=[LeafNode("code", code_text)])


def quote_to_html_node(block: str):
    children = []
    for line in block.split("\n"):
        children.append(LeafNode("p", line[2:]))

    return ParentNode("blockquote", children=children)


def paragraph_to_html_node(block: str):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)