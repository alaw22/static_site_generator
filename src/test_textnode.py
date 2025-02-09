import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = TextNode("This is a text node", TextType.IMAGE)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
        
    def test_rep(self):
        node = TextNode("Testing the repr", TextType.ITALIC, "www.google.com")
        self.assertEqual("TextNode(Testing the repr, italic, www.google.com)",node.__repr__())

    def test_url(self):
        node = TextNode("Standards",TextType.BOLD)
        node2 = TextNode("Excuses",TextType.IMAGE)
        self.assertEqual(node.url,node2.url)

    def test_texttype(self):
        node = TextNode("Standards",TextType.BOLD)
        node2 = TextNode("Excuses",TextType.BOLD)
        self.assertEqual(node.text_type,node2.text_type)

    def test_text(self):
        node = TextNode("Standards",TextType.BOLD)
        node2 = TextNode("Standards",TextType.IMAGE)
        self.assertEqual(node.text,node2.text)

class TestToHTML(unittest.TestCase):
    def test_normal(self):
        textnode = TextNode("Normal text",TextType.TEXT)
        leafnode = text_node_to_html_node(textnode)
        self.assertEqual(textnode.text,leafnode.to_html())

    def test_bold(self):
        textnode = TextNode("Bold text",TextType.BOLD)
        leafnode = text_node_to_html_node(textnode)
        output = f"<b>{textnode.text}</b>"
        self.assertEqual(output,leafnode.to_html())

    def test_italic(self):
        textnode = TextNode("Italic text",TextType.ITALIC)
        leafnode = text_node_to_html_node(textnode)
        output = f"<i>{textnode.text}</i>"
        self.assertEqual(output,leafnode.to_html())

    def test_code(self):
        textnode = TextNode("Code",TextType.CODE)
        leafnode = text_node_to_html_node(textnode)
        output = f"<code>{textnode.text}</code>"
        self.assertEqual(output,leafnode.to_html())

    def test_link(self):
        textnode = TextNode("Link",TextType.LINK,"www.pathtolink.com")
        leafnode = text_node_to_html_node(textnode)
        output = f'<a href="{textnode.url}">{textnode.text}</a>'
        self.assertEqual(output,leafnode.to_html())

    def test_image(self):
        textnode = TextNode("Random image of the sun",TextType.IMAGE,"www.linktoimage.com")
        leafnode = text_node_to_html_node(textnode)
        output = f'<img src="{textnode.url}" alt="{textnode.text}"></img>'
        self.assertEqual(output,leafnode.to_html())
    
    def test_raise(self):
        with self.assertRaises(TypeError):
            textnode = TextNode("Link",int)
            leafnode = text_node_to_html_node(textnode)

if __name__ == "__main__":
    unittest.main()
