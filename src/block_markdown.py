from enum import Enum
import htmlnode
import textnode
import inline_markdown
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(text):
    result = []
    blocks = text.split('\n\n')
    for i in range(len(blocks)):
        block = blocks[i].strip()
        #print(f"Block {i} before: ",block)
        if block == "":
            continue
        lines = block.split('\n')
        if len(lines) > 1:
            lines = list(map(lambda x: x.strip(),lines))
            block = '\n'.join(lines)
        result.append(block)
    return result # one string of multiple \n

# Block type check:
# Block is a string of multiple lines, and no empty string.
# def block_to_block_type(block):
#     this_block_type = BlockType.PARAGRAPH
#     this_block_type = check_heading(block)
#     if this_block_type is not BlockType.PARAGRAPH:
#         return this_block_type
#     this_block_type = check_code(block)
#     if this_block_type is not BlockType.PARAGRAPH:
#         return this_block_type
#     this_block_type = check_quote(block)
#     if this_block_type is not BlockType.PARAGRAPH:
#         return this_block_type
#     this_block_type = check_unordered_list(block)
#     if this_block_type is not BlockType.PARAGRAPH:
#         return this_block_type
#     this_block_type = check_ordered_list(block)
#     return this_block_type
# func_list = [check_heading,check_code,check_quote,check_ordered_list,check_unordered_list]
# this_block_type = BlockType.PARAGRAPH
# for func in func_list:
#     this_block_type = func(block)
#     if this_block_type is not BlockType.PARAGRAPH:
#         return this_block_type
# return this_block_type

def is_heading(block):
    if not block.startswith('#'):
        return False
    hash_count = 0
    for char in block:
        if char == '#':
            hash_count += 1
        else:
            break
    if 1 <= hash_count <= 6 and block[hash_count] == ' ':
        return True
    return False
    
    
def is_code(block):
    return len(block) >= 6 and block.startswith('```') and block.endswith('```')

def is_quote(block):
    lines = block.split('\n')
    for line in lines:
        if not line or line[0] != ">":
            return False
    return True

def is_unordered_list(block):
    lines = block.split('\n')
    for line in lines:
        if not line or not line.startswith('- '):
            return False
    return True

def is_ordered_list(block):
    lines = block.split('\n')
    for i in range(len(lines)):
        if not lines[i] or not lines[i].startswith(f'{i+1}. '):
            return False
    return True

def block_to_block_type_func(block):
    if is_heading(block):
        return BlockType.HEADING
    elif is_code(block):
        return BlockType.CODE
    elif is_quote(block):
        return BlockType.QUOTE
    elif is_unordered_list(block):
        return BlockType.UNORDERED_LIST
    elif is_ordered_list(block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


# Turn text to text nodes then add them as child nodes in child blocks
def text_to_children(text):
    text_nodes = inline_markdown.text_to_textnodes(text)
    children = []
    for node in text_nodes:
        children.append(textnode.text_node_to_html_node(node))
    #print(children)
    return children

# Create HTMLNode for heading block
def create_heading_node(block):
    
    hash_count = 0
    for char in block:
        if char != '#':
            break
        hash_count+=1
    text = ' '.join(block.split()[1:]) # removing the markdowns
    block_children = text_to_children(text)
    return htmlnode.ParentNode(tag=f"h{hash_count}",children=block_children)

# Create HTMLNode for code block
def create_code_node(block):
    parts = block.split("```")
    
    code_content = parts[1]
    
    #print('Code content:',code_content)
    text_node = textnode.TextNode(code_content,textnode.TextType.TEXT)
    code_content_node = textnode.text_node_to_html_node(text_node)
    code_node = htmlnode.ParentNode(tag="code",children=[code_content_node])
    return htmlnode.ParentNode(tag='pre',children=[code_node])

# Create HTMLNode for quote block
def create_quote_node(block):
    lines = block.split('\n')
    for i in range(len(lines)):
        lines[i] = lines[i].lstrip('> ').rstrip('\n').strip()
    text = ' '.join(lines)
    block_children = text_to_children(text)
    return htmlnode.ParentNode(tag="blockquote",children=block_children)

# Create HTMLNode for unordered list block
def create_ul_node(block):
    list_items = block.split('\n')
    list_item_nodes = []
    for i in range(len(list_items)):
        list_item_text = list_items[i].lstrip('- ')
        list_item_children = text_to_children(list_item_text)
        list_item_node = htmlnode.ParentNode('li',children=list_item_children)
        list_item_nodes.append(list_item_node)
    return htmlnode.ParentNode(tag="ul",children=list_item_nodes)

# Create HTMLNode for ordered list block
def create_ol_node(block):
    list_items = block.split('\n')
    list_item_nodes = []
    for i in range(len(list_items)):
        list_item_text = list_items[i].lstrip(f'{i+1}. ')
        list_item_children = text_to_children(list_item_text)
        list_item_node = htmlnode.ParentNode('li',children=list_item_children)
        list_item_nodes.append(list_item_node)
    return htmlnode.ParentNode(tag="ol",children=list_item_nodes)

# Create HTMLNode for paragraph block
def create_p_node(block):
    content = block.rstrip("\n")
    content = content.replace("\n"," ")
    paragraph_children = text_to_children(content)
    return htmlnode.ParentNode(tag="p",children=paragraph_children)
    
# Handle block type for child block nodes
def create_block_node_child(block, block_type):
    match block_type:
        case BlockType.HEADING:
            return create_heading_node(block)
        case BlockType.CODE:
            return create_code_node(block)
        case BlockType.QUOTE:
            return create_quote_node(block)
        case BlockType.UNORDERED_LIST:
            return create_ul_node(block)
        case BlockType.ORDERED_LIST:
            return create_ol_node(block) # implement
        case BlockType.PARAGRAPH:
            return create_p_node(block) # implement this too
        case _:
            raise Exception("Invalid block type when creating new block nodes.")

# Turn markdown document into a big div block with child block of different block types
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        this_block_type = block_to_block_type_func(block)
        block_nodes.append(create_block_node_child(block, this_block_type))
    return htmlnode.ParentNode(tag='div',children=block_nodes)
