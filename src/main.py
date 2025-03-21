import re
import os
import shutil
import page_generator

# Paths
markdown_folder = './content/'
static_folder = "./static/"
markdown_file = './content/index.md'
template_file_path = './template.html'
public_folder = './public/'

def main():
    load_static_files()

# Wrapping function for loading static files and generating pages.
def directory_traversal(func):
    def wrapper(src, dest):
        dir_content = os.listdir(src)
        while len(dir_content) != 0:
            next_file = dir_content.pop()
            next_file_path = src + next_file
            if os.path.isfile(next_file_path):
                func(next_file_path,dest)
                
            else:
                next_src = src + next_file + '/'
                next_dest = dest + next_file + '/'
                if not os.path.exists(next_dest):
                    os.mkdir(next_dest)
                wrapper(next_src,next_dest)
    return wrapper

@directory_traversal
def copy_static_file(file_path,dest):
    shutil.copy(file_path,dest)
    
@directory_traversal
def generate_page_content(file_path,dest):
    page_generator.generate_page(
        from_path=file_path,
        template_path=template_file_path,
        dest_path=f"{dest}index.html"
    )

def load_static_files():
    if os.path.exists(public_folder):
        shutil.rmtree(public_folder)
    os.mkdir(public_folder)
    copy_static_file(static_folder,public_folder)
    generate_page_content(markdown_folder,public_folder)
    
    
main()