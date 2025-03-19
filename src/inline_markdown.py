from htmlnode import *
from textnode import TextNode,TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        if len(old_node.text) == 0:
            continue
        sections = old_node.text.split(delimiter) 
        no_closing_delimiter = len(sections) % 2 == 0
        if no_closing_delimiter:
            raise Exception("Markdown error: Closing delimiter not found.")
        #0 left 1 mid 2 right
        split_nodes = []
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if len(old_node.text) == 0:
            continue
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        link_props = extract_regular_links(old_node.text)
        if len(link_props) == 0:
            new_nodes.append(old_node)
            continue
        new_nodes.extend(split_text_for_link(link_props, old_node.text, []))
    return new_nodes

# Receive list of tuples of link properties and recursively split the text and add nodes
def split_text_for_link(link_props, text, split_nodes):
    # Just in case.
    if len(link_props) == 0:
        return split_nodes
    
    copy_list = link_props.copy()
    markdown_element = copy_list[0] # (alt text, url)
    split_texts = text.split(f"[{markdown_element[0]}]({markdown_element[1]})",1)
    
    # Append left part and link
    if split_texts[0] != "":
        split_nodes.append(TextNode(split_texts[0],TextType.TEXT))
    split_nodes.append(TextNode(markdown_element[0],TextType.LINK,markdown_element[1]))
    
    # Append right part if there is only one link left
    if len(link_props) == 1:
        split_nodes.append(TextNode(split_texts[1],TextType.TEXT))
        return split_nodes
    return split_text_for_link(copy_list[1:],split_texts[1],split_nodes)
        
def split_images(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text == "":
            continue
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        image_props = extract_markdown_images(old_node.text)
        if len(image_props) == 0:
            new_nodes.append(old_node)
            continue
        new_nodes.extend(split_text_for_images(image_props, old_node.text, []))
    return new_nodes

def split_text_for_images(image_props, text, split_nodes):
    # print("Debug: Image props: ", image_props, " - Text: ", text, " - Current split_nodes: ", split_nodes, "\n")
    # Just in case.
    if len(image_props) == 0:
        return split_nodes
    
    copy_list = image_props.copy()
    markdown_element = copy_list[0] # (alt text, url)
    split_texts = text.split(f"![{markdown_element[0]}]({markdown_element[1]})",1)
    
    # Append left part and link
    if split_texts[0] != "":
        split_nodes.append(TextNode(split_texts[0],TextType.TEXT))
    split_nodes.append(TextNode(markdown_element[0],TextType.IMAGE,markdown_element[1]))
    
    # Append right part if there is only one link left
    if len(image_props) == 1:
        if split_texts[1] != "":
            split_nodes.append(TextNode(split_texts[1],TextType.TEXT))
        return split_nodes
    return split_text_for_images(copy_list[1:],split_texts[1],split_nodes)
    
def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)

def extract_regular_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)

def text_to_textnodes(text):
    text_nodes = [TextNode(text,TextType.TEXT)]
    text_nodes = split_link(text_nodes)
    text_nodes = split_images(text_nodes)
    types = {TextType.BOLD : "**", TextType.ITALIC: "_", TextType.CODE: "`"}
    for type in types:
        text_nodes = split_nodes_delimiter(text_nodes,types[type],type)
    return text_nodes
