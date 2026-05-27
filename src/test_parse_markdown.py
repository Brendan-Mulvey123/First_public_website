import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from parse_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, extract_title

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("This is text with _multiple_ italics in the _sentance_!", TextType.TEXT)
        node3 = TextNode("This is some **bold** text", TextType.TEXT)
        node4 = TextNode("This is also some **bold** text", TextType.BOLD)
        node5 = TextNode("This is unbalanced _italics text", TextType.TEXT)


        new_nodes1 = split_nodes_delimiter([node1], "`", TextType.CODE)
        new_nodes2 = split_nodes_delimiter([node2], "_", TextType.ITALIC)
        new_nodes3 = split_nodes_delimiter([node3], "**", TextType.BOLD)
        new_nodes4 = split_nodes_delimiter([node4], "**", TextType.BOLD)


        self.assertEqual(new_nodes1, list([TextNode("This is text with a ", TextType.TEXT, None), TextNode("code block", TextType.CODE, None), TextNode(" word", TextType.TEXT, None)]))
        self.assertEqual(new_nodes2, list([TextNode("This is text with ", TextType.TEXT, None), TextNode("multiple", TextType.ITALIC, None), TextNode(" italics in the ", TextType.TEXT, None), TextNode("sentance", TextType.ITALIC, None), TextNode("!", TextType.TEXT, None)]))
        self.assertEqual(new_nodes3, list([TextNode("This is some ", TextType.TEXT, None), TextNode("bold", TextType.BOLD, None), TextNode(" text", TextType.TEXT, None)]))
        self.assertEqual(new_nodes4, list([TextNode("This is also some **bold** text", TextType.BOLD, None)]))

        with self.assertRaises(TypeError):
            new_nodes5 = split_nodes_delimiter([node5], "_", TextType.ITALIC)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        matches2 = extract_markdown_images("This is text with an [image](https://i.imgur.com/zjjcJKZ.png)")
        matches3 = extract_markdown_images("First image ![image](https://i.imgur.com/zjjcJKZ.png) and second image ![image2](https://i.imgur.com/zjjcJKZf.png)")


        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        self.assertListEqual([], matches2)
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("image2", "https://i.imgur.com/zjjcJKZf.png")], matches3)


    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with an [Link1](https://boot.dev)")
        matches2 = extract_markdown_links("This is text with an ![link2](https://i.imgur.com/zjjcJKZ.png)")
        matches3 = extract_markdown_links("First imagen [Link3](https://boot.dev/learn) and second image [Link4](https://google.com)")

        self.assertListEqual([("Link1", "https://boot.dev")], matches)
        self.assertListEqual([], matches2)
        self.assertListEqual([("Link3", "https://boot.dev/learn"), ("Link4", "https://google.com")], matches3)

    def test_split_images(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT,)
        node2 = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT,)
        node3 = TextNode(" and another ![second image](https://i.imgur.com/3elNhQu.png) is cool", TextType.TEXT,)
        node4 = None
        node5 = TextNode("I like my cat and it is cool", TextType.TEXT,)
        node6 = TextNode("This is text with an [Link1](https://boot.dev)", TextType.TEXT,)
        node7 = TextNode("[second image](https://i.imgur.com/3elNhQu.png)", TextType.IMAGE,)
        new_nodes = split_nodes_image([node])
        new_nodes2 = split_nodes_image([node2, node3])
        new_nodes3 = split_nodes_image([node2, node4, node3])
        new_nodes4 = split_nodes_image([node5])
        new_nodes5 = split_nodes_image([node6])
        new_nodes6 = split_nodes_image([node2, node6])
        new_nodes7 = split_nodes_link([node7])
        self.assertListEqual([TextNode("This is text with an ", TextType.TEXT), TextNode("image", TextType.IMAGE, {"src":"https://i.imgur.com/zjjcJKZ.png"}), TextNode(" and another ", TextType.TEXT),  TextNode("second image", TextType.IMAGE, {"src":"https://i.imgur.com/3elNhQu.png"}),], new_nodes,)
        self.assertListEqual([TextNode("This is text with an ", TextType.TEXT), TextNode("image", TextType.IMAGE, {"src":"https://i.imgur.com/zjjcJKZ.png"}), TextNode(" and another ", TextType.TEXT),  TextNode("second image", TextType.IMAGE, {"src":"https://i.imgur.com/3elNhQu.png"}),TextNode(" is cool", TextType.TEXT)], new_nodes2,)
        self.assertListEqual([TextNode("This is text with an ", TextType.TEXT), TextNode("image", TextType.IMAGE, {"src":"https://i.imgur.com/zjjcJKZ.png"}), TextNode(" and another ", TextType.TEXT),  TextNode("second image", TextType.IMAGE, {"src":"https://i.imgur.com/3elNhQu.png"}),TextNode(" is cool", TextType.TEXT)], new_nodes3,)
        self.assertListEqual([TextNode("I like my cat and it is cool", TextType.TEXT)], new_nodes4,)
        self.assertListEqual([TextNode("This is text with an [Link1](https://boot.dev)", TextType.TEXT)], new_nodes5,)
        self.assertListEqual([TextNode("This is text with an ", TextType.TEXT), TextNode("image", TextType.IMAGE, {"src":"https://i.imgur.com/zjjcJKZ.png"}), TextNode("This is text with an [Link1](https://boot.dev)", TextType.TEXT)], new_nodes6,)
        self.assertListEqual([TextNode("[second image](https://i.imgur.com/3elNhQu.png)", TextType.IMAGE,)], new_nodes7,)

    def test_split_links(self):
        node = TextNode("This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT,)
        node2 = TextNode("This is text with an [image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT,)
        node3 = TextNode(" and another [second image](https://i.imgur.com/3elNhQu.png) is cool", TextType.TEXT,)
        node4 = None
        node5 = TextNode("I like my cat and it is cool", TextType.TEXT,)
        node6 = TextNode("This is text with an ![Link1](https://boot.dev)", TextType.TEXT,)
        node7 = TextNode("[second image](https://i.imgur.com/3elNhQu.png)", TextType.LINKS,)
        new_nodes = split_nodes_link([node])
        new_nodes2 = split_nodes_link([node2, node3])
        new_nodes3 = split_nodes_link([node2, node4, node3])
        new_nodes4 = split_nodes_link([node5])
        new_nodes5 = split_nodes_link([node6])
        new_nodes6 = split_nodes_link([node3, node6])
        new_nodes7 = split_nodes_link([node7])
        self.assertListEqual([TextNode("This is text with an ", TextType.TEXT), TextNode("image", TextType.LINKS, {"href":"https://i.imgur.com/zjjcJKZ.png"}), TextNode(" and another ", TextType.TEXT),  TextNode("second image", TextType.LINKS, {"href":"https://i.imgur.com/3elNhQu.png"}),], new_nodes,)
        self.assertListEqual([TextNode("This is text with an ", TextType.TEXT), TextNode("image", TextType.LINKS, {"href":"https://i.imgur.com/zjjcJKZ.png"}), TextNode(" and another ", TextType.TEXT),  TextNode("second image", TextType.LINKS, {"href":"https://i.imgur.com/3elNhQu.png"}),TextNode(" is cool", TextType.TEXT)], new_nodes2,)
        self.assertListEqual([TextNode("This is text with an ", TextType.TEXT), TextNode("image", TextType.LINKS, {"href":"https://i.imgur.com/zjjcJKZ.png"}), TextNode(" and another ", TextType.TEXT),  TextNode("second image", TextType.LINKS, {"href":"https://i.imgur.com/3elNhQu.png"}),TextNode(" is cool", TextType.TEXT)], new_nodes3,)
        self.assertListEqual([TextNode("I like my cat and it is cool", TextType.TEXT)], new_nodes4,)
        self.assertListEqual([TextNode("This is text with an ![Link1](https://boot.dev)", TextType.TEXT)], new_nodes5,)
        self.assertListEqual([TextNode(" and another ", TextType.TEXT),  TextNode("second image", TextType.LINKS, {"href":"https://i.imgur.com/3elNhQu.png"}),TextNode(" is cool", TextType.TEXT), TextNode("This is text with an ![Link1](https://boot.dev)", TextType.TEXT)], new_nodes6,)
        self.assertListEqual([TextNode("[second image](https://i.imgur.com/3elNhQu.png)", TextType.LINKS,)], new_nodes7,)

    def test_text_to_textnodes(self):
        text1 = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        text2 = "Some **text** with a lot of _italics_ and **bold** sections to **highlight**. "
        text3 = "Some **bold text with _italic_ inside** to see what happens."
        text4 = ""

        result1 = text_to_textnodes(text1)
        result2 = text_to_textnodes(text2)
        result3 = text_to_textnodes(text3)
        result4 = text_to_textnodes(text4)

        self.assertListEqual(result1, [
        TextNode("This is ", TextType.TEXT),
        TextNode("text", TextType.BOLD),
        TextNode(" with an ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word and a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" and an ", TextType.TEXT),
        TextNode("obi wan image", TextType.IMAGE, {"src":"https://i.imgur.com/fJRm4Vk.jpeg"}),
        TextNode(" and a ", TextType.TEXT),
        TextNode("link", TextType.LINKS, {"href":"https://boot.dev"}),
        ])

        self.assertListEqual(result2, [TextNode("Some ", TextType.TEXT), TextNode("text", TextType.BOLD), TextNode(" with a lot of ", TextType.TEXT), TextNode("italics", TextType.ITALIC), TextNode(" and ", TextType.TEXT), TextNode("bold", TextType.BOLD), TextNode(" sections to ", TextType.TEXT), TextNode("highlight", TextType.BOLD), TextNode(". ", TextType.TEXT)])

        self.assertListEqual(result3, [TextNode("Some ", TextType.TEXT, None), TextNode("bold text with _italic_ inside", TextType.BOLD, None), TextNode(" to see what happens.", TextType.TEXT, None)])

        self.assertListEqual(result4, [])
        with self.assertRaises(ValueError):
            result5 = text_to_textnodes(None)

    def test_extract_title(self):
        md1 = "#  welcome \n## Hello2"
        md2 = "##  welcome \n# Hello2"
        md3 = "#welcome \n## Hello2"

        result1 = extract_title(md1)
        result2 = extract_title(md2)
        self.assertEqual(result1, "welcome")
        self.assertEqual(result2, "Hello2")

        with self.assertRaises(Exception):
            result3 = extract_title(md3)




