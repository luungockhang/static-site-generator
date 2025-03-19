import re
import os
import shutil
import page_generator

# Paths
markdown_file = './content/index.md'
template_file = './template.html'

def main():
    # grandchild_node = LeafNode("b", "grandchild")
    # print(grandchild_node)
    # child_node = ParentNode("span", [grandchild_node])
    # print(child_node)
    # parent_node = ParentNode("div", [child_node])
    # print(parent_node)
    # # print(parent_node.to_html())
    # text = "I'm a little teapot, short and stout. Here is my handle, here is my spout."
    # matches = re.findall(r"teapot", text)
    # print(matches) # ['teapot']

    # text = "My email is lane@example.com and my friend's email is hunter@example.com"
    # matches = re.findall(r"(\w+)@(\w+\.\w+)", text)
    # print(matches)  # [('lane', 'example.com'), ('hunter', 'example.com')]
    
    # load_static_files()
    # when copy, if dir not exists, have to create dir before copying
    load_static_files()
    
    
def load_static_files(src='static/',dest='public/'):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)
    copy_file(src,dest)
    index_destination_path = './public/index.html'
    page_generator.generate_page(from_path=markdown_file,template_path=template_file,dest_path=index_destination_path)
    
def copy_file(source, dest):
    dir_content = os.listdir(source)
    while len(dir_content) != 0:
        next_file = dir_content.pop()
        # Get the next file in the current folder
        next_file_path = source + next_file
        print('Next file: ', next_file_path)
        # Check if it's a file
        if os.path.isfile(next_file_path):
            print('Found a file: ', next_file_path)
            # if file, copy
            shutil.copy(next_file_path,dest)
            
        else:
            # if dir, go into that dir and repeat with next_file
            next_src = source + next_file + '/'
            next_dest = dest + next_file + '/'
            if not os.path.exists(next_dest):
                os.mkdir(next_dest)
            copy_file(next_src,next_dest)
    
    
main()