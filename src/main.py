import re
import os
import shutil
import page_generator
import sys
from pathlib import Path

# Configurable root path on local folder
basepath = './'
if not sys.argv:
    basepath = Path('/')
else:
    basepath = Path(sys.argv[0])

# Folder paths
markdown_folder = basepath / Path('./content/')
static_folder = basepath / Path("./static/")
markdown_file = basepath / Path('./content/index.md')
template_file_path = basepath / Path('./template.html')
public_folder = basepath / Path('./docs/')

def main():
    load_static_files()
    

def load_static_files():
    if os.path.exists(public_folder):
        shutil.rmtree(public_folder)
    os.mkdir(public_folder)
    copy_static_file(static_folder, public_folder)
    generate_page_content(markdown_folder,public_folder)
    
# Wrapping function for loading static files and generating pages.
def directory_traversal(func):
    def wrapper(src, dest):
        # Convert paths to Path objects
        src_path = Path(src)
        dest_path = Path(dest)
        
        dir_content = os.listdir(src_path)
        while len(dir_content) != 0:
            next_file = dir_content.pop()
            next_file_path = src_path / next_file # Using the / operator of Path object
            if next_file_path.is_file(): # Path method to check if it's file
                func(next_file_path,dest_path)
                
            else:
                next_src = src_path / next_file
                next_dest = dest_path / next_file

                # Create dir if not exist
                next_dest.mkdir(exist_ok=True) # Path method to create dir
                
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
        dest_path= dest / "index.html"
    )


def generate_page_recursive(src_dir_path, template_path, dest_dir_path,basepath=basepath):
    for entry in os.listdir(src_dir_path):
        source_path = os.path.join(src_dir_path, entry)
        dest_path = os.path.join(dest_dir_path, entry)
        
        if os.path.isfile(source_path) and source_path.endswith(".md"):
            # Generate HTML for markdown files
            html_dest = os.path.join(dest_dir_path,entry.replace(".md",".html"))
            page_generator.generate_page(source_path, template_file_path,dest_path,BASEPATH=basepath)
        elif os.path.isdir(source_path):
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)
            generate_page_recursive(source_path, template_path, dest_path)

    
main()