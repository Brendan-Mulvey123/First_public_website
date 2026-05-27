import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode()
        node2 = HTMLNode("Tag A", children="car")
        node3 = HTMLNode("Tag B")
        node4 = HTMLNode("Tag A", "value A", "child1", {"bold": "yes"})
        node5 = HTMLNode("Tag C", "value B", "child2", {"bold": "yes", "Italics": "6", "Code": "2"})
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node2, node3)
        self.assertEqual(node2.tag, "Tag A")
        self.assertEqual(node3.value, None)
        self.assertEqual(node2.children, "car")
        self.assertEqual(node4.__repr__(), f"Object is {id(node4)}, tag is Tag A, value is value A, children is child1, and props is {{\'bold\': \'yes\'}}")
        self.assertEqual(node3.__repr__(), f"Object is {id(node3)}, tag is Tag B, value is None, children is None, and props is None")
        self.assertEqual(node5.props_to_html(), f" bold=yes Italics=6 Code=2")





if __name__ == "__main__":
    unittest.main()
