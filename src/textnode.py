from enum import Enum
import htmlnode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    
class TextNode():
    def __init__(self,text,text_type,url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return (self.text == other.text 
                and self.text_type == other.text_type 
                and self.url == other.url)
    
    def __repr__(self):
        return f"TextNode({self.text},{self.text_type.value},{self.url})"


def text_node_to_html_node(text_node):
    match (text_node.text_type):
        case TextType.TEXT:
            return htmlnode.LeafNode(None,text_node.text)
        case TextType.BOLD:
            return htmlnode.LeafNode("b",text_node.text)
        case TextType.ITALIC:
            return htmlnode.LeafNode("i",text_node.text)
        case TextType.CODE:
            return htmlnode.LeafNode("code",text_node.text)
        case TextType.LINK:
            properties = {"href":text_node.url}
            print(f"Creating LeafNode: tag=a, value={text_node.text}, props={properties}")
            return htmlnode.LeafNode("a", text_node.text, properties)
        case TextType.IMAGE:
            return htmlnode.LeafNode("img","",props={"src":text_node.url,"alt":text_node.text})
        case _:
            raise Exception("Invalid TextNode type")
