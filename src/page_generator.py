import block_markdown
import htmlnode


def extract_title(markdown):
    if len(markdown) == 0:
        raise Exception("Markdown document is empty.")
    title_line = markdown.split('\n')[0]
    title_words = title_line.split()
    if title_words[0] != "#":
        raise Exception("Title markdown is not a h1 header")
    
    if len(title_words) < 2:
        raise Exception("Title content not found")
    
    return title_line.lstrip('#').strip()

def generate_page(from_path='', template_path='', dest_path=''):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md_content = ''
    with open(from_path, 'r') as file:
        md_content = file.read()
    
    page_content = ''
    with open(template_path, 'r') as file:
        page_content = file.read()
    
    html_string = block_markdown.markdown_to_html_node(md_content).to_html()
    title = extract_title(md_content)
    page_content = page_content.replace("{{ Content }}", html_string)
    page_content = page_content.replace("{{ Title }}", title)
    
    with open(dest_path, 'w') as file:
        file.write(page_content)
        