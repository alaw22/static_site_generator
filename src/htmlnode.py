import functools

class HTMLNode:
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, other):
        return self.tag == other.tag and \
               self.value == other.value and \
               self.children == other.children and \
               self.props == other.props

    def __repr__(self):
        return f"HTMLNode({self.tag},{self.value},{self.children},{self.props})"

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""
        
        return functools.reduce(lambda x,y: x + f' {y[0]}="{y[1]}"',self.props.items(),"")
    
# Child class of HTMLNode with no children of itself
class LeafNode(HTMLNode):
    def __init__(self,tag,value,props=None):
        if value is None or not isinstance(value,str) or value == "":
            raise ValueError("All LeafNode must have a value")
        if tag is not None and (not isinstance(tag, str) or tag == ""):
            raise ValueError("Tag must be None or a non-empty string")
        
        super().__init__(tag=tag, value=value,props=props)


    def to_html(self):
        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if tag is None or not isinstance(tag, str) or tag == "":
            raise ValueError("Tag must be a non-empty string")
        if children is None:
            raise ValueError("ParentNode must have children")
        if not isinstance(children,list):
            raise TypeError("children should be a list")
        
        for child in children:
            if not isinstance(child,HTMLNode):
                raise TypeError("Each item in children should be of type HTMLNode")
            
        super().__init__(tag=tag,children=children,props=props)

    def to_html(self):
        return f"<{self.tag}>" + functools.reduce(lambda x,y: x + y.to_html(),self.children,"") + f"</{self.tag}>"