import unittest

from htmlnode import HTMLNode, LeafNode,ParentNode
from textnode import TextNode, TextType
from inline_markdown import *
from block_markdown import *

class TestInlineMarkdown(unittest.TestCase):
    def test_inline_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node],"`",TextType.CODE) 
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])
        
    def test_inline_bold(self):
        node = TextNode("This is text with a **code block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node],"**",TextType.BOLD) 
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ])
    
    def test_inline_bold(self):
        node = TextNode("This is text with a **code block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node],"**",TextType.BOLD) 
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ])
    
    def test_inline_italic(self):
        node = TextNode("This is text with a _code block_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node],"_",TextType.ITALIC) 
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ])
    
    def test_inline_italic_last(self):
        node = TextNode("This is text with a _code block word_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node],"_",TextType.ITALIC) 
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block word", TextType.ITALIC)])
    
    def test_inline_none(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node],"_",TextType.ITALIC) 
        self.assertEqual(new_nodes, [])
        
    def test_invalid_delimiter_exception(self):
        node = TextNode("Text without closing delimiter`", TextType.TEXT)
        
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    def test_extract_markdown_images_blank_alt(self):
        matches = extract_markdown_images(
            "This is text with an ![](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    def test_extract_markdown_images_blank_link(self):
        matches = extract_markdown_images(
            "This is text with an ![]()"
        )
        self.assertListEqual([("", "")], matches)
        
    def test_extract_regular_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"

        matches = extract_regular_links(text)
        self.assertListEqual([("to boot dev","https://www.boot.dev"),("to youtube", "https://www.youtube.com/@bootdotdev")], matches)
        
    def test_extract_regular_links_blank_case(self):
        text = "This is text with a link [to boot dev]() and [](https://www.youtube.com/@bootdotdev)"

        matches = extract_regular_links(text)
        self.assertListEqual([("to boot dev",""),("", "https://www.youtube.com/@bootdotdev")], matches)
        
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        
    def test_split_links(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another [second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)
            ],
            new_nodes,
        )
    
    def test_split_links_empty_input(self):

        new_nodes = split_images([])
        self.assertListEqual(
            [],
            new_nodes,
        )
        
    def test_split_images_same_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) ![image](https://i.imgur.com/zjjcJKZ.png) and another",
            TextType.TEXT,
        )
        new_nodes = split_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(
                    " ", TextType.TEXT),
                TextNode(
                    "image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"
                ),                
                TextNode(" and another", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = r"This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes
        )
if __name__ == "__main__":
    unittest.main()
