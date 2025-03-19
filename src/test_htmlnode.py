import unittest

from htmlnode import HTMLNode, LeafNode,ParentNode
from textnode import TextNode, TextType

class TestHTMLNode(unittest.TestCase):

    def test_1(self):
        props = {}
        props["href"] = "google.com"
        props["target"] = "blank"
        node = HTMLNode("p", "This is a paragraph", HTMLNode("a","blank"), props)
        print(node)
        
    def test_2(self):
        node = HTMLNode(None,"something")
        print(node)
    
    def test_3(self):
        props = {}
        props["href"] = "google.com"
        props["target"] = "blank"
        node = HTMLNode("a","This is link", None, props)
        print(node)
        
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
        
    def test_to_html_with_grandchildren_and_props(self):        
        props = {}
        props["class"] = "test"
        
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node],props)
        
        self.assertEqual(
            parent_node.to_html(),
            '<div class="test"><span><b>grandchild</b></span></div>',
        )
    
    def test_to_html_with_multiple_children(self):
        child1 = LeafNode("span", "first")
        child2 = LeafNode("span", "second")
        parent = ParentNode("div", [child1, child2])
        self.assertEqual(parent.to_html(), "<div><span>first</span><span>second</span></div>")

    def test_with_missing_tag(self):
        with self.assertRaises(ValueError):
            node = ParentNode(None, [LeafNode("b", "text")])
            node.to_html()
    
    def test_with_blank_children_list(self):
        parent = ParentNode("div", [])
        self.assertEqual(parent.to_html(),"<div></div>")
if __name__ == "__main__":
    unittest.main()
