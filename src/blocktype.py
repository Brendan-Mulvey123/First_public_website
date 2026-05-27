from enum import Enum
import re


class BlockType(Enum):
    paragraph = 1
    heading = 2
    code = 3
    quote = 4
    unordered_list = 5
    ordered_list = 6


def markdown_to_blocks(markdown):
    if not isinstance(markdown, str):
        raise ValueError("input to markdown_to_blocks function is not a string")
    if len(markdown) == 0:
        return []

    split_blocks = markdown.split("\n\n")
    return_blocks = []
    for block in split_blocks:
        if block == "":
            continue
        return_blocks.append(block.strip())
    return return_blocks


def block_to_block_type(markdown):
    if not isinstance(markdown, str):
        raise ValueError("input to markdown_to_blocks function is not a string")
    if re.findall(r"^#{1,6} ", markdown):
        return BlockType.heading
    if re.findall(r"^```\n.*```$", markdown, re.DOTALL):
        return BlockType.code
    if re.findall(r"^>", markdown):
        return BlockType.quote
    split_lines = markdown.splitlines()
    unordered_list = True
    for line in split_lines:
        if not re.findall(r"^- ", line):
            unordered_list = False
    if unordered_list:
        return BlockType.unordered_list
    split_lines2 = markdown.splitlines()
    ordered_list = True
    for i in range(0,len(split_lines2)):
        if not re.findall(fr"^{i+1}\. ", split_lines2[i]):
            ordered_list = False
    if ordered_list:
        return BlockType.ordered_list
    return BlockType.paragraph

