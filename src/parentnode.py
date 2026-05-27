from htmlnode import HTMLNode
from leafnode import LeafNode
import string

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        pass


    def to_html(self):
        if self.tag is None:
            raise ValueError("tag was not set")
        #if self.children is None or not isinstance(self.children, list):
        if self.children is None :
            raise ValueError("children was not set")

        return_string = ""
        match self.tag:
            case "p":
                return_string += "<p>"
            case "span":
                return_string += "<span>"
            case "div":
                return_string += "<div>"
            case "h1":
                return_string += "<h1>"
            case "h2":
                return_string += "<h2>"
            case "h3":
                return_string += "<h3>"
            case "h4":
                return_string += "<h4>"
            case "h5":
                return_string += "<h5>"
            case "h6":
                return_string += "<h6>"
            case "code":
                return_string += "<pre>"
            case "quote":
                return_string += "<blockquote>"
            case "unordered_list":
                return_string += "<ul>"
            case "ordered_list":
                return_string += "<ol>"
            case "list":
                return_string += "<li>"



            case _:
                raise ValueError("Unknown tag or tag not implemented")

        for leaf in self.children:
            if isinstance(leaf, LeafNode) or isinstance(leaf, ParentNode):
                return_string += leaf.to_html()
            else:
                print(f"leaf type is {type(leaf)} and it contains {leaf} and children is {self.children}")
                raise ValueError("Unknown or malformed child in children")

        match self.tag:
            case "p":
                return_string += "</p>"
            case "span":
                return_string += "</span>"
            case "div":
                return_string += "</div>"
            case "h1":
                return_string += "</h1>"
            case "h2":
                return_string += "</h2>"
            case "h3":
                return_string += "</h3>"
            case "h4":
                return_string += "</h4>"
            case "h5":
                return_string += "</h5>"
            case "h6":
                return_string += "</h6>"
            case "code":
                return_string += "</pre>"
            case "quote":
                return_string += "</blockquote>"
            case "unordered_list":
                return_string += "</ul>"
            case "ordered_list":
                return_string += "</ol>"
            case "list":
                return_string += "</li>"

        return return_string

    def __repr__(self):
        return f"Object is {id(self)}, tag is {self.tag}, children is {self.children} and props is {self.props}"
