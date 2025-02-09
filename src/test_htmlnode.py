import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(value="context")
        node2 = HTMLNode(value="context")
        self.assertEqual(node,node2)
    
    def test_props_to_html(self):
        node = HTMLNode(props={"href":"www.google.com",
                               "img":"hello.jpeg",
                               "alt":"an image that says hello"})
        comp_str = ' href="www.google.com" img="hello.jpeg" alt="an image that says hello"'
        self.assertEqual(comp_str,node.props_to_html())

    def test_noteq(self):
        node = HTMLNode(tag="div",value="Insert text here")
        node2 = HTMLNode(tag="div",value="Insert text here",props={"href":"www.google.com"})
        self.assertNotEqual(node,node2)


class TestLeafNode(unittest.TestCase):
    def test_no_value(self):
        with self.assertRaises(ValueError):
            node = LeafNode("p",None)

    def test_tag_emtpy(self):
        with self.assertRaises(ValueError):
            node = LeafNode("","some text here")

    def test_to_html(self):
        node = LeafNode("a","Use this search engine",props={"href":"www.google.com"})
        output = '<a href="www.google.com">Use this search engine</a>'
        self.assertEqual(node.to_html(),output)

class TestParentNode(unittest.TestCase):
    def test_tag_isempty(self):
        with self.assertRaises(ValueError):
            leaf = LeafNode("b","This is bold text")
            leaf2 = LeafNode("p","This is a paragraph")
            children = [leaf,leaf2]
            node = ParentNode("",children)
    
    def test_tag_isNone(self):
        with self.assertRaises(ValueError):
            leaf = LeafNode("b","This is bold text")
            leaf2 = LeafNode("p","This is a paragraph")
            children = [leaf,leaf2]
            node = ParentNode(None,children)

    def test_children_isNone(self):
        with self.assertRaises(ValueError):
            node = ParentNode("html",None)

    def test_children_isNone(self):
        with self.assertRaises(TypeError):
            leaf = LeafNode("b","This is bold text")
            leaf2 = LeafNode("p","This is a paragraph")
            children = (leaf,leaf2)
            node = ParentNode("html",children)    

    def test_non_html_node(self):
        with self.assertRaises(TypeError):
            node = ParentNode("body")
            node2 = LeafNode("b","This is bold text")
            node3 = LeafNode("div")
            children = [node2,node3,5]
            node4 = ParentNode("html",children=children)

    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        result = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(),result)

    def test_multiple_parents(self):
        node = ParentNode(
            "div",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
                ParentNode(
                           "p",
                           [
                               LeafNode("a","This link",props={"href":"www.google.com"}),
                               LeafNode("b","some bold text")
                           ]
                           )
            ],
        )
        
        output = '<div><b>Bold text</b>Normal text<i>italic text</i>Normal text<p><a href="www.google.com">This link</a><b>some bold text</b></p></div>'
        self.assertEqual(output,node.to_html())

