from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        pass



    def to_html(self):
        if self.value is None:
            raise ValueError("Error: All leaf nodes must have a value")
        if self.tag is None:
            return self.value
        match self.tag:
            case "p":
                return f"<p>{self.value}</p>"
            case "b":
                return f"<b>{self.value}</b>"
            case "i":
                return f"<i>{self.value}</i>"
            case "code":
                return f"<code>{self.value}</code>"
            case "span":
                return f"<span>{self.value}</span>"
            case "a":
                if self.props is None:
                    return f"<a None>{self.value}</a>"
                else:
                    key = next(iter(self.props))
                    return f"<a {key}=\"{self.props[key]}\">{self.value}</a>"
            case "img":
                if self.props is None:
                    return f"<img None> alt={self.value} />"
                else:
                    key = next(iter(self.props))
                    return f"<img {key}=\"{self.props[key]}\" alt=\"{self.value}\">"
            case _:
                raise ValueError("Error: Unknown tag type")


    def __repr__(self):
        return f"Object is {id(self)}, tag is {self.tag}, value is {self.value} and props is {self.props}"
