from htmlnode import *
from inline_markdown import *
from textnode import *
from block_markdown import BlockType
from page_generator import *

# This file is for quick function testing
markdown_file = './content/index.md'
template_file = './template.html'
dest_path = './public/index.html'
generate_page(from_path=markdown_file,template_path=template_file, dest_path=dest_path)