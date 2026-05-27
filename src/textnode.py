from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
    TEXT = 1   #text (plain)
    BOLD = 2    #**Bold text**
    ITALIC = 3  #_Italic text_
    CODE = 4    #`Code text`
    LINKS = 5        #[anchor text](url)
    IMAGE = 6       #![alt text](url)



class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        else:
            return False


    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"






def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINKS:
            return LeafNode("a", text_node.text, text_node.url)
        case TextType.IMAGE:
            return LeafNode("img", text_node.text, text_node.url)
        case _:
            raise ValueError("Unknown TextType Enum")
