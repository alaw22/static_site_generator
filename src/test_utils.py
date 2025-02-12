import unittest
import utils
from textnode import TextNode, TextType


class TestDelimiter(unittest.TestCase):

    def test_plaintext(self):
        nodes = [
                    TextNode("This is regular text sir", TextType.TEXT),
                    TextNode("This is also regular text", TextType.TEXT)
                ]
        
        self.assertEqual(nodes,utils.split_nodes_delimiter(nodes,"**",TextType.BOLD))

    def test_oned_multiplespots(self):
        nodes = [
                    TextNode("This is **regular** text **sir**", TextType.TEXT),
                    TextNode("**This** is also **regular text**", TextType.TEXT),
                    TextNode("**This is **also regular text 2", TextType.TEXT)
                ]

        expected = [
                    TextNode("This is ", TextType.TEXT),
                    TextNode("regular", TextType.BOLD),
                    TextNode(" text ", TextType.TEXT),
                    TextNode("sir", TextType.BOLD),
                    TextNode("This", TextType.BOLD),
                    TextNode(" is also ", TextType.TEXT),
                    TextNode("regular text", TextType.BOLD),
                    TextNode("This is ", TextType.BOLD),
                    TextNode("also regular text 2", TextType.TEXT)
                    ]
        
        self.assertEqual(utils.split_nodes_delimiter(nodes,"**",TextType.BOLD),expected)


    def test_multiple_delimiters(self):
        nodes = [
                    TextNode("This is **regular** `tex`t **sir**", TextType.TEXT),
                    TextNode("*This* is also **regular text**", TextType.TEXT),
                ]

        first_split = [
                        TextNode("This is ", TextType.TEXT),
                        TextNode("regular", TextType.BOLD),
                        TextNode(" `tex`t ", TextType.TEXT),
                        TextNode("sir", TextType.BOLD),
                        TextNode("*This* is also ", TextType.TEXT),
                        TextNode("regular text", TextType.BOLD),
                      ]
        
        second_split = [
                        TextNode("This is ", TextType.TEXT),
                        TextNode("regular", TextType.BOLD),
                        TextNode(" `tex`t ", TextType.TEXT),
                        TextNode("sir", TextType.BOLD),
                        TextNode("This", TextType.ITALIC),
                        TextNode(" is also ", TextType.TEXT),
                        TextNode("regular text", TextType.BOLD),
                      ]

        third_split = [
                        TextNode("This is ", TextType.TEXT),
                        TextNode("regular", TextType.BOLD),
                        TextNode(" ", TextType.TEXT),
                        TextNode("tex", TextType.CODE),
                        TextNode("t ", TextType.TEXT),
                        TextNode("sir", TextType.BOLD),
                        TextNode("This", TextType.ITALIC),
                        TextNode(" is also ", TextType.TEXT),
                        TextNode("regular text", TextType.BOLD),
                      ]

        first_iter = utils.split_nodes_delimiter(nodes,"**",TextType.BOLD)
        self.assertEqual(first_split,first_iter)
        second_iter = utils.split_nodes_delimiter(first_iter,"*",TextType.ITALIC)
        self.assertEqual(second_split,second_iter)
        third_iter = utils.split_nodes_delimiter(second_iter,"`",TextType.CODE)
        self.assertEqual(third_split,third_iter)


    def test_raise(self):
        nodes = [
                    TextNode("This is r`egular text sir", TextType.TEXT),
                    TextNode("`This` is also regular text", TextType.TEXT)
                ]
        
        with self.assertRaises(Exception):
            utils.split_nodes_delimiter(nodes,"`",TextType.CODE)

    def test_nesting(self):
        nodes = [
                    TextNode("This is **regular `text`** sir", TextType.TEXT),
                ]

        expected = [
                    TextNode("This is ",TextType.TEXT),
                    TextNode("regular `text`",TextType.BOLD),
                    TextNode(" sir",TextType.TEXT),
                    ]

        first = utils.split_nodes_delimiter(nodes,"**",TextType.BOLD)
        second = utils.split_nodes_delimiter(first,"`",TextType.CODE)

        self.assertEqual(first,second)
        self.assertEqual(expected,second)