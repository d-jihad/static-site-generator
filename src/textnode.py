from src.htmlnode import LeafNode


class TextNode:
    def __init__(self, text, text_type, url=None) -> None:
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


def text_node_to_html_node(text_node):
    if text_node.text_type == "bold":
        return LeafNode("b", text_node.text)
    elif text_node.text_type == "italic":
        return LeafNode("i", text_node.text)
    elif text_node.text_type == "link":
        return LeafNode("a", text_node.text, props={"href": text_node.url})
    elif text_node.text_type == "image":
        return LeafNode("img", props={"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError("Invalid text type")