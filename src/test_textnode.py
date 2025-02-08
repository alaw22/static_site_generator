import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()
