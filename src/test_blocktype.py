import unittest

from blocktype import *

class TestBlockType(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

        md2 = "This is the first line\n\n\n\n\nAnd this is the second line"
        blocks2 = markdown_to_blocks(md2)
        self.assertEqual(blocks2, ["This is the first line", "And this is the second line"],)

    def test_block_to_block_type(self):
        md1 = "This is **bolded** paragraph"
        md2 = "### I am a heading"
        md3 = "#####I am not a heading"
        md4 = "```\nThis is a code block\n```"
        md5 = "````\nNot a code block```"
        md6 = "> This is a quote"
        md7 = ">This is also a quote"
        md8 = "- This is an \n- unordered list\n- with several lines of\n- text"
        md9 = "- This is not a \n- valid unordered list \n-because a space is \n- missing"
        md10 = "1. This is a\n2. ordered list.\n3. It has many \n4. bullet points.\n5. Cats\n6. Dogs"
        md11 = "1. This is not a\n2. valid ordered list\n3.More dogs"

        block_type1 = block_to_block_type(md1)
        block_type2 = block_to_block_type(md2)
        block_type3 = block_to_block_type(md3)
        block_type4 = block_to_block_type(md4)
        block_type5 = block_to_block_type(md5)
        block_type6 = block_to_block_type(md6)
        block_type7 = block_to_block_type(md7)
        block_type8 = block_to_block_type(md8)
        block_type9 = block_to_block_type(md9)
        block_type10 = block_to_block_type(md10)
        block_type11 = block_to_block_type(md11)

        self.assertEqual(block_type1, BlockType.paragraph)
        self.assertEqual(block_type2, BlockType.heading)
        self.assertEqual(block_type3, BlockType.paragraph)
        self.assertEqual(block_type4, BlockType.code)
        self.assertEqual(block_type5, BlockType.paragraph)
        self.assertEqual(block_type6, BlockType.quote)
        self.assertEqual(block_type7, BlockType.quote)
        self.assertEqual(block_type8, BlockType.unordered_list)
        self.assertEqual(block_type9, BlockType.paragraph)
        self.assertEqual(block_type10, BlockType.ordered_list)
        self.assertEqual(block_type11, BlockType.paragraph)

        with self.assertRaises(ValueError):
            block_type_fail = block_to_block_type(77)

