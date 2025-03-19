import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq_type(self):
        node = TextNode("This is text node case 2",TextType.CODE)
        node2 = TextNode("This is text node case 2", TextType.LINK)
        self.assertNotEqual(node, node2)
    
    def test_neq_url(self):
        node = TextNode("This is text node case 3",TextType.CODE,None)
        node2 = TextNode("This is text node case 3", TextType.CODE,"yes, this is url")
        self.assertNotEqual(node, node2)

    def test_eq2(self):
        node = TextNode("This is text node case 4",TextType.CODE,None)
        node2 = TextNode("This is text node case 4", TextType.CODE,None)
        self.assertEqual(node, node2)
    
    def test_neq_text(self):
        node = TextNode("This is text node case 3",TextType.CODE,None)
        node2 = TextNode("This is text node case 4", TextType.CODE,None)
        self.assertNotEqual(node, node2)
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        
    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_code_html_node(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_link_textnode(self):
        node = TextNode("This is a text node", TextType.LINK, "example.com")
        html_node = text_node_to_html_node(node) 
        print(html_node) 
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props["href"], "example.com")
        
    def test_img_textnode(self):
        node = TextNode("This is an image of a cat", TextType.IMAGE, "cat.png")
        html_node = text_node_to_html_node(node) 
        print(html_node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props["src"], "cat.png")
        self.assertEqual(html_node.props["alt"], "This is an image of a cat")    
if __name__ == "__main__":
    unittest.main()
