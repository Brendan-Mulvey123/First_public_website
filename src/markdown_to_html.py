from textnode import TextType, TextNode, text_node_to_html_node
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
import re
from parse_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from blocktype import BlockType, markdown_to_blocks, block_to_block_type


def text_to_children(text):
    leafnode_list = []
    TextNode_list = text_to_textnodes(text)
    for node1 in TextNode_list:
        leafnode_list.append(text_node_to_html_node(node1))
    return leafnode_list



def markdown_to_html_node(markdown):
    if not isinstance(markdown, str):
        raise ValueError("input to markdown to html function is not a string")
    markdown_block_list = markdown_to_blocks(markdown)

    HTMLNode_list = []
    for markdown_block in markdown_block_list:
        leaf_nodes = []
        block_type = block_to_block_type(markdown_block)
        match block_type:
            case BlockType.heading:
                for i in range(0,min(len(markdown_block),7)):
                    if markdown_block[i] == "#":
                        continue
                    else:
                        leaf_nodes = text_to_children(markdown_block[i+1:])
                        HTMLNode_list.append(ParentNode("h" + str(i), leaf_nodes))
                        break
            case BlockType.code:
                node = TextNode(markdown_block[4:-3], TextType.CODE,)
                leaf_node = text_node_to_html_node(node)
                HTMLNode_list.append(ParentNode("code", [leaf_node]))
            case BlockType.quote:
                split_lines = markdown_block.splitlines()
                leaf_nodes = []
                for line in split_lines:
                    leaf_nodes.extend(text_to_children(line[1:].strip()))
                HTMLNode_list.append(ParentNode("quote", leaf_nodes))
            case BlockType.unordered_list:
                split_lines = markdown_block.splitlines()
                leaf_nodes = []
                for line in split_lines:
                    leaf_nodes.append(ParentNode("list", text_to_children(line[2:])))
                HTMLNode_list.append(ParentNode("unordered_list",  leaf_nodes))
            case BlockType.ordered_list:
                split_lines = markdown_block.splitlines()
                leaf_nodes = []
                for line in split_lines:
                    leaf_nodes.append(ParentNode("list", text_to_children(line[3:])))
                HTMLNode_list.append(ParentNode("ordered_list", leaf_nodes))
            case BlockType.paragraph:
                new_string = markdown_block.replace("\n", " ")
                leaf_nodes = text_to_children(new_string)
                HTMLNode_list.append(ParentNode("p", leaf_nodes))

    return (ParentNode("div", HTMLNode_list))
