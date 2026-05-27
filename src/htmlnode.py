

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props


    def to_html(self):
        raise NotImplementedError("Function not implemented")


    def props_to_html(self):
        self.return_string = ""
        for key in self.props.keys():
            self.return_string = self.return_string + " " + key + "=" + self.props[key]
        return self.return_string


    def __repr__(self):
        return f"Object is {id(self)}, tag is {self.tag}, value is {self.value}, children is {self.children}, and props is {self.props}"

