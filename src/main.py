from textnode import TextType, TextNode, text_node_to_html_node
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
import re
import os
import sys
import shutil
from parse_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, extract_title
from blocktype import BlockType, markdown_to_blocks, block_to_block_type
from markdown_to_html import markdown_to_html_node


def main():
    if len(sys.argv) <= 1:
        print("Folder path to project root not given, using default path \"/\"")
        basepath = "./"
    else:
        basepath = sys.argv[1]
    if not os.path.isdir(basepath):
        print("ERROR: the basepath folder \"{basepath}\" does not exist or is not a folder")
        exit(1)
    else:
        if basepath[-1] != "/":
            basepath = basepath + "/"

    public_dir = os.path.join(basepath,"docs")
    static_dir = os.path.join(basepath,"static")
    content_dir = os.path.join(basepath,"content")
    copy_static_to_public(static_dir, public_dir)
    #generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive(content_dir, os.path.join(basepath, "template.html"), public_dir, basepath)


def copy_static_to_public(source_dir, dest_dir):

    if os.path.exists(dest_dir):
        if not os.path.isdir(dest_dir):
            raise Exception("file public exists but is not a directory")
        else:
            shutil.rmtree(dest_dir)
    os.mkdir(dest_dir, 0o775)
    File_list = os.listdir(source_dir)
    for file1 in File_list:
        if os.path.isdir(os.path.join(source_dir, file1)):
            folder_dist = os.path.join(dest_dir, file1)
            folder_source = os.path.join(source_dir, file1)
            copy_static_to_public(folder_source, folder_dist)

        else:
            file_source = os.path.join(source_dir, file1)
            file_dest = os.path.join(dest_dir, file1)
            print(f"Copying file from location\n{file_source}\n to location\n{file_dest}\n")
            shutil.copy(file_source, file_dest, follow_symlinks=False)

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    file_contents = ""
    template_contents = ""
    try:
        with open(from_path) as f:
            file_contents = f.read()
    except FileNotFoundError:
        print(f"Error: The file {from_path} was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    try:
        with open(template_path) as f:
            template_contents = f.read()
    except FileNotFoundError:
        print(f"Error: The file {template_path} was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    html_string = markdown_to_html_node(file_contents).to_html()
    Title = extract_title(file_contents)
    temp_html1 = template_contents.replace("{{ Title }}", Title )
    temp_html2 = temp_html1.replace("{{ Content }}", html_string )
    temp_html3 = temp_html2.replace("href=\"/",f"href=\"{basepath}")
    temp_html4 = temp_html3.replace("src=\"/",f"src=\"{basepath}")
    if os.path.exists(dest_path):
        raise Exception("Error cannot overwrite file, should have been cleared by a previous step.")
        exit(1)
    print(f"Directory name is {os.path.dirname(dest_path)}")
    os.makedirs(os.path.dirname(dest_path), 0o775, exist_ok=True)
    try:
        with open(dest_path, 'w') as f:
            f.write(temp_html2)
    except IOError as e:
        print(f"An error occurred: {e}")


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    file_list = os.listdir(dir_path_content)
    for file1 in file_list:
        if os.path.isdir(os.path.join(dir_path_content, file1)):
            folder_scan = os.path.join(dir_path_content, file1)
            folder_output = os.path.join(dest_dir_path, file1)
            generate_pages_recursive(folder_scan, template_path, folder_output, basepath)
        else:
            #check if file ends in .md.  If yes convert to html and save to public output folder.  If not ignore the file.
            if  re.findall(r"\.md$", file1):
                generate_page(os.path.join(dir_path_content, file1), template_path, os.path.join(dest_dir_path, (file1[:-2] + "html")), basepath)




main()
