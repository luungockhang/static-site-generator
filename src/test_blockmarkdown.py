import unittest

from htmlnode import HTMLNode, LeafNode,ParentNode
from textnode import TextNode, TextType
from inline_markdown import *
from block_markdown import *

class TestInlineMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
     This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line


    - This is a list
    - with items 
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_blank_case(self):
        md = """
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
            ],
        )
    
    def test_markdown_to_blocks_one_block_case(self):
        md = """aaaaa
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["aaaaa"
            ],
        )
    
    def test_block_to_blocktype_heading(self):
        block = "## a"
        self.assertEqual(block_to_block_type_func(block),BlockType.HEADING)
        
    def test_block_to_blocktype_not_heading(self):
        block = "##a a a"
        self.assertNotEqual(block_to_block_type_func(block),BlockType.HEADING)
        
    def test_block_to_blocktype_not_heading(self):
        block = "##a a a"
        self.assertNotEqual(block_to_block_type_func(block),BlockType.HEADING)
    
    def test_block_to_blocktype_code(self):
        block = "```##a a a```"
        self.assertEqual(block_to_block_type_func(block),BlockType.CODE)
     
    def test_block_to_blocktype_not_code(self):
        block = "```aa``"
        self.assertNotEqual(block_to_block_type_func(block),BlockType.CODE)
        
    def test_block_to_blocktype_quote(self):
        block = ">this\n>is\n>a\n>quote"
        self.assertEqual(block_to_block_type_func(block),BlockType.QUOTE)
     
    def test_block_to_blocktype_not_quote(self):
        block = ">this\n>is\n>not\na\n>quote"
        self.assertNotEqual(block_to_block_type_func(block),BlockType.QUOTE)
     
    def test_block_to_blocktype_unordered_list(self):
        block = "- this\n- is\n- not\n- a\n- quote"
        self.assertEqual(block_to_block_type_func(block),BlockType.UNORDERED_LIST)
        
    def test_block_to_blocktype_not_unordered_list_1(self):
        block = "- this\nis\n>- not\n- a\n- quote"
        self.assertNotEqual(block_to_block_type_func(block),BlockType.UNORDERED_LIST)     
    
    def test_block_to_blocktype_not_unordered_list_2(self):
        block = "- this\n-is\n>- not\n- a\n>- quote"
        self.assertNotEqual(block_to_block_type_func(block),BlockType.UNORDERED_LIST)  

    def test_block_to_blocktype_ordered_list(self):
        block = "1. this\n2. is\n3. not\n4. a\n5. quote"
        self.assertEqual(block_to_block_type_func(block),BlockType.ORDERED_LIST)
        
    def test_block_to_blocktype_not_ordered_list_1(self):
        block = "1. this\n2. is\n>3. not\n3. a\n5. quote"
        self.assertNotEqual(block_to_block_type_func(block),BlockType.ORDERED_LIST)     
    
    def test_block_to_blocktype_not_ordered_list_2(self):
        block = "1. this\n2. is\n>- not\n4. a\n>5. quote"
        self.assertNotEqual(block_to_block_type_func(block),BlockType.ORDERED_LIST)   
        
    def test_block_to_blocktype_not_ordered_list_3(self):
        block = "1. this\n2. is\n>3. not\n4. a\n>quote"
        self.assertNotEqual(block_to_block_type_func(block),BlockType.ORDERED_LIST)
    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>\nThis is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
        



if __name__ == "__main__":
    unittest.main()
