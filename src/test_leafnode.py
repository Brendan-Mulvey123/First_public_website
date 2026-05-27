import unittest

from htmlnode import HTMLNode
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("p", "Hello, world!")
        node2 = LeafNode("b", "big cars")
        node3 = LeafNode("i", "This is good")
        #node4 = LeafNode("Tag A", "value A", "child1", {"bold": "yes"})
        node5 = LeafNode("a", "google website", {"href": "https://www.google.com"})
        node6 = LeafNode("Tag B", None)
        node7 = LeafNode("img", "Description of image", {"src": "url/of/image.jpg"})
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        self.assertEqual(node2.to_html(), "<b>big cars</b>")
        self.assertEqual(node3.to_html(), "<i>This is good</i>")
        self.assertEqual(node5.to_html(), "<a href=\"https://www.google.com\">google website</a>")
        self.assertEqual(node7.to_html(), "<img src=\"url/of/image.jpg\" alt=\"Description of image\">")
        with self.assertRaises(TypeError):
            LeafNode("Tag B").to_html()
            LeafNode("Tag A", "value A", "child1", {"bold": "yes"}).to_html()
        with self.assertRaises(ValueError):
            node6.to_html()







if __name__ == "__main__":
    unittest.main()
