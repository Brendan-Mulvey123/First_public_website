from textnode import TextType, TextNode, text_node_to_html_node
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    #if old_nodes is None or len(old_nodes) == 0:
    if old_nodes is None:
        return ""
    for text_node in old_nodes:
        if text_node.text_type != TextType.TEXT:
            new_nodes.append(text_node)
        else:
            split_string = text_node.text.split(delimiter)
            if len(split_string) % 2 == 0:
                raise TypeError("Unbalanced number of delimiters in input text, invalid Markdown syntax")
            else:
                for i in range(0,len(split_string)):
                    if i % 2 == 0:
                        new_nodes.append(TextNode(split_string[i], TextType.TEXT))
                    else:
                        new_nodes.append(TextNode(split_string[i], text_type))
    return new_nodes

def extract_markdown_images(text):
    match1 = re.findall(r"!\[.*?\]", text)
    match2 = re.findall(r"\(https://.*?\)", text)
    match3 = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)" , text)
    return_match = []
    if len(match1)  == len(match2):
        for i in range(0, len(match1)):
            return_match.append((match1[i][2:-1], match2[i][1:-1]))
    #print(f"match 3 is {match3}")
    return match3

def extract_markdown_links(text):
    match1 = re.findall(r"\[.*?\]", text)
    match2 = re.findall(r"\(https://.*?\)", text)
    match3 = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return_match = []
    if len(match1)  == len(match2):
        for i in range(0, len(match1)):
            return_match.append((match1[i][1:-1], match2[i][1:-1]))

    return match3

def split_nodes_image(old_nodes):
    if old_nodes is None or len(old_nodes) == 0:
        return []
    return_nodes_list = []
    for node in old_nodes:
        if not isinstance(node, TextNode) or len(node.text) == 0:
            continue
        if node.text_type != TextType.TEXT:
            return_nodes_list.append(node)
            continue
        split_string = re.split(r'(?<!\\)!\[', node.text)
        for i in range(0, len(split_string)):
            open_split = 0
            if i == 0 and len(split_string[i]) > 0:
                return_nodes_list.append(TextNode(split_string[i], TextType.TEXT))
                continue
            for j in range(0, len(split_string[i])):
                if split_string[i][j] != ")" and split_string[i][j] != "]":
                    continue
                else:
                    if j == 0:
                        raise ValueError("image name cannot start with a parenthesis or bracket that is not escaped")
                    elif split_string[i][j-1] == "/":
                        continue
                    else:
                        if split_string[i][j] == "]":
                            open_split = j
                        else:
                            return_nodes_list.append(TextNode(split_string[i][0:open_split], TextType.IMAGE, {"src":split_string[i][open_split+2:j]}))
                            if j + 1 < len(split_string[i]):
                                return_nodes_list.append(TextNode(split_string[i][j+1:len(split_string[i])], TextType.TEXT))
                            break

    return return_nodes_list

def split_nodes_link(old_nodes):
    if old_nodes is None or len(old_nodes) == 0:
        return []
    return_nodes_list = []
    for node in old_nodes:
        if not isinstance(node, TextNode) or len(node.text) == 0:
            continue
        if node.text_type != TextType.TEXT:
            return_nodes_list.append(node)
            continue
        split_string = re.split(r'(?<![!\\])\[', node.text)
        if len(split_string) == 1:
            return_nodes_list.append(node)
            continue
        for i in range(0, len(split_string)):
            open_split = 0
            if i == 0 and len(split_string[i]) > 0:
                return_nodes_list.append(TextNode(split_string[i], TextType.TEXT))
                continue
            for j in range(0, len(split_string[i])):
                if split_string[i][j] != ")" and split_string[i][j] != "]":
                    continue
                else:
                    if j == 0:
                        raise ValueError("image name cannot start with a parenthesis or bracket that is not escaped")
                    else:
                        if split_string[i][j] == "]":
                            open_split = j
                        else:
                            return_nodes_list.append(TextNode(split_string[i][0:open_split], TextType.LINKS, {"href":split_string[i][open_split+2:j]}))
                            if j + 1 < len(split_string[i]):
                                return_nodes_list.append(TextNode(split_string[i][j+1:len(split_string[i])], TextType.TEXT))

    return return_nodes_list



def text_to_textnodes(text):
    if not isinstance(text, str):
        raise ValueError("input to text_to_textnodes function is not a string")
    list_of_nodes = []

    first_node = TextNode(text, TextType.TEXT,)

    first_split = split_nodes_image([first_node])
    for node1 in first_split:
        if node1.text_type == TextType.IMAGE:
            list_of_nodes.append(node1)
            continue
        second_split = split_nodes_link([node1])
        for node2 in second_split:
            if node2.text_type == TextType.LINKS:
                list_of_nodes.append(node2)
                continue
            third_split = split_nodes_delimiter([node2], "**", TextType.BOLD)
            for node3 in third_split:
                fourth_split = split_nodes_delimiter([node3], "_", TextType.ITALIC)
                for node4 in fourth_split:
                    list_of_nodes.extend(split_nodes_delimiter([node4], "`", TextType.CODE))
    return list_of_nodes


def extract_title(markdown):
    markdown_lines = markdown.splitlines()
    for line in markdown_lines:
        if re.findall(r"^# ", line):
            return line[2:].strip()
    raise Exception("markdown file does not contain a header")



