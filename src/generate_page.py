import os
from markdown_to_html import markdown_to_html_node
from inline_markdown import extract_title

def generate_page(from_path, template_path, dest_path):
    if not os.path.exists(from_path):
        raise FileNotFoundError(f"source path `{from_path}` doesn't exist")
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"template `{template_path}` doesn't exist")
    
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path,"r") as input_file:
        from_contents = input_file.read()

    with open(template_path,"r") as template_file:
        template_contents = template_file.read()

    html_parent_node = markdown_to_html_node(from_contents)
    content = html_parent_node.to_html()
    # content = html_parent_node.to_html().replace("\n","<br />") doesn't work quite that well should probs do this somewhere else
    title = extract_title(from_contents)

    template_contents = template_contents.replace("{{ Title }}",title)
    template_contents = template_contents.replace("{{ Content }}",content)


    os.makedirs("/".join(dest_path.split("/")[:-1]),exist_ok=True)

    with open(dest_path,"w") as output_file:
        output_file.write(template_contents)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dir_path_content):
        raise Exception(f"Source path `{dir_path_content}` doesn't exist")
    
    for item in os.listdir(dir_path_content):
        temp_path = os.path.join(dir_path_content,item)
        if os.path.isfile(temp_path) and temp_path.endswith(".md"):
            html_filename = item.replace(".md",".html")
            dest_path = os.path.join(dest_dir_path,html_filename)
            generate_page(temp_path,template_path,dest_path)

        elif os.path.isdir(temp_path):
            subdirname = temp_path.split("/")[-1]
            new_dest_dir_path = os.path.join(dest_dir_path,subdirname)
            generate_pages_recursive(temp_path,template_path,new_dest_dir_path)
                    
