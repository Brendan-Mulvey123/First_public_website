import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from parse_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from markdown_to_html import markdown_to_html_node

class Test_Markdown_to_html(unittest.TestCase):


    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,"<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",)

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,"<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",)

    def test_lists(self):
        md = "1. First item\n2. This is the second item\n3. Third\n4. I am last"
        md2 = "- car\n- bike\n- A dog\n- Plane\n- boat"
        md3 = "1. CPU\n2. RAM\n3. Graphics Card\n4. case at [case-link](/content/images/case_1.html)\n5. HDD"
        md4 = "- dog\n- cat\n- rabbit\n- cow ![cow_image](/content/images/cow_1.png)\n- pig"

        node = markdown_to_html_node(md)
        node2 = markdown_to_html_node(md2)
        node3 = markdown_to_html_node(md3)
        node4 = markdown_to_html_node(md4)
        html = node.to_html()
        html2 = node2.to_html()
        html3 = node3.to_html()
        html4 = node4.to_html()
        self.assertEqual(html,"<div><ol><li>First item</li><li>This is the second item</li><li>Third</li><li>I am last</li></ol></div>")
        self.assertEqual(html2,"<div><ul><li>car</li><li>bike</li><li>A dog</li><li>Plane</li><li>boat</li></ul></div>")
        self.assertEqual(html3,"<div><ol><li>CPU</li><li>RAM</li><li>Graphics Card</li><li>case at <a href=\"/content/images/case_1.html\">case-link</a></li><li>HDD</li></ol></div>")
        self.assertEqual(html4,"<div><ul><li>dog</li><li>cat</li><li>rabbit</li><li>cow <img src=\"/content/images/cow_1.png\" alt=\"cow_image\"></li><li>pig</li></ul></div>")

    def test_headings(self):
        md = "##### This is a small heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,"<div><h5>This is a small heading</h5></div>")

    def test_links(self):
        md = "This is text with an [google-link](https://google.com)"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,"<div><p>This is text with an <a href=\"https://google.com\">google-link</a></p></div>")

    def test_images(self):
        md = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,"<div><p>This is text with an <img src=\"https://i.imgur.com/zjjcJKZ.png\" alt=\"image\"></p></div>")





