import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a different text node", TextType.LINKS, "https://www.boot.dev")
        self.assertEqual(node, node2)
        self.assertNotEqual(node2, node3)
        self.assertEqual(node.url, None)
        self.assertEqual(node3.url, "https://www.boot.dev")
        self.assertNotEqual(node.text_type, node3.text_type)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is Important", TextType.BOLD)
        node3 = TextNode("This is special", TextType.ITALIC)
        node4 = TextNode("This is some code", TextType.CODE)
        node5 = TextNode("This is a link to  duckduckgo", TextType.LINKS, {"href": "https://duckduckgo.com/"})
        node6 = TextNode("This is a dud link", TextType.LINKS)
        node7 = TextNode("This is a image", TextType.IMAGE,  {"src": "/src/images/dog2.png"})

        html_node = text_node_to_html_node(node)
        html_node2 = text_node_to_html_node(node2)
        html_node3 = text_node_to_html_node(node3)
        html_node4 = text_node_to_html_node(node4)
        html_node5 = text_node_to_html_node(node5)
        html_node6 = text_node_to_html_node(node6)
        html_node7 = text_node_to_html_node(node7)

        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node2.tag, "b")
        self.assertEqual(html_node3.to_html(), "<i>This is special</i>")
        self.assertEqual(html_node4.to_html(), "<code>This is some code</code>")
        self.assertEqual(html_node5.to_html(), "<a href=\"https://duckduckgo.com/\">This is a link to  duckduckgo</a>")
        self.assertEqual(html_node6.to_html(), "<a None>This is a dud link</a>")
        self.assertEqual(html_node6.props, None)
        self.assertEqual(html_node7.to_html(), "<img src=\"/src/images/dog2.png\" alt=\"This is a image\">")



        with self.assertRaises(AttributeError):
            node9 = TextNode("What is this tag?", TextType.YELLOW)
            html_node9 = text_node_to_html_node(node9)


if __name__ == "__main__":
    unittest.main()
