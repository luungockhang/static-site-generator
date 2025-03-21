import re
import os
import shutil
import page_generator

# Paths
markdown_folder = './content/'
markdown_file = './content/index.md'
template_file = './template.html'
public_folder = './public/'

def main():
    load_static_files()


def load_static_files(src='static/',dest='public/'):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)
    copy_static_file(src,dest)
    # index_destination_path = './public/index.html'
    # page_generator.generate_page(from_path=markdown_file,template_path=template_file,dest_path=index_destination_path)
    generate_page_content()
    
def generate_page_content(src=markdown_folder,dest=public_folder):
    dir_content = os.listdir(src)
    while len(dir_content) != 0:
        next_file = dir_content.pop()
        # Get the next file in the current folder
        next_file_path = src + next_file
        print('Next file: ', next_file_path)
        # Check if it's a file
        if os.path.isfile(next_file_path):
            # print('Found a file: ', next_file_path)
            # if file (md), generate the page
#             print(f"""Generating page with these informations:
# Source:{next_file}
# Destination:{dest}
# """)
            page_generator.generate_page(from_path=next_file_path,template_path=template_file,dest_path=f"{dest}index.html")
            
        else:
            # if dir, go into that dir and repeat with next_file
            next_src = src + next_file + '/'
            next_dest = dest + next_file + '/'
            if not os.path.exists(next_dest):
                os.mkdir(next_dest)
            generate_page_content(next_src,next_dest)
            
def copy_static_file(source, dest):
    dir_content = os.listdir(source)
    while len(dir_content) != 0:
        next_file = dir_content.pop()
        # Get the next file in the current folder
        next_file_path = source + next_file
        # print('Next file: ', next_file_path)
        # Check if it's a file
        if os.path.isfile(next_file_path):
            # print('Found a file: ', next_file_path)
            # if file, copy
            shutil.copy(next_file_path,dest)
            
        else:
            # if dir, go into that dir and repeat with next_file
            next_src = source + next_file + '/'
            next_dest = dest + next_file + '/'
            if not os.path.exists(next_dest):
                os.mkdir(next_dest)
            copy_static_file(next_src,next_dest)
    
    
main()