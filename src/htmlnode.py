import textnode
from block_markdown import *
import inline_markdown

class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    
    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props == None:
            return ""
        s = ""
        for key in self.props:
            s += f" {key}=\"{self.props[key]}\""
        return s


    def __repr__(self):
        return f"HTMLNode({self.tag},{self.value},{self.children},{self.props})"

    
    
#     def __repr__(self):
#         return f"""--- HTML Node Print ---
# Tag = {self.tag}
# Value = {self.value}
# Children = {self.children}
# Props = {self.props_to_html()}    
#     """
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag,value,props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Error: Leaf node must have a value.")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag},{self.value},{self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag,children=children,props=props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("Error: Parent node must have a tag.")
        if self.children is None:
            raise ValueError("Error: Parent node must have children")
        child_html = ""
        for child in self.children:
            #print("Child: ",child)
            child_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{child_html}</{self.tag}>"

    