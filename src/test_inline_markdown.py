import unittest
import inline_markdown
from textnode import TextNode, TextType


class TestDelimiter(unittest.TestCase):

    def test_plaintext(self):
        nodes = [
                    TextNode("This is regular text sir", TextType.TEXT),
                    TextNode("This is also regular text", TextType.TEXT)
                ]
        
        self.assertEqual(nodes,inline_markdown.split_nodes_delimiter(nodes,"**",TextType.BOLD))

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
        
        self.assertEqual(inline_markdown.split_nodes_delimiter(nodes,"**",TextType.BOLD),expected)


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

        first_iter = inline_markdown.split_nodes_delimiter(nodes,"**",TextType.BOLD)
        self.assertEqual(first_split,first_iter)
        second_iter = inline_markdown.split_nodes_delimiter(first_iter,"*",TextType.ITALIC)
        self.assertEqual(second_split,second_iter)
        third_iter = inline_markdown.split_nodes_delimiter(second_iter,"`",TextType.CODE)
        self.assertEqual(third_split,third_iter)


    def test_raise(self):
        nodes = [
                    TextNode("This is r`egular text sir", TextType.TEXT),
                    TextNode("`This` is also regular text", TextType.TEXT)
                ]
        
        with self.assertRaises(Exception):
            inline_markdown.split_nodes_delimiter(nodes,"`",TextType.CODE)

    def test_nesting(self):
        nodes = [
                    TextNode("This is **regular `text`** sir", TextType.TEXT),
                ]

        expected = [
                    TextNode("This is ",TextType.TEXT),
                    TextNode("regular `text`",TextType.BOLD),
                    TextNode(" sir",TextType.TEXT),
                    ]

        first = inline_markdown.split_nodes_delimiter(nodes,"**",TextType.BOLD)
        second = inline_markdown.split_nodes_delimiter(first,"`",TextType.CODE)

        self.assertEqual(first,second)
        self.assertEqual(expected,second)

class TestExtractMethods(unittest.TestCase):
    def test_extractimages(self):
        text = "This is an example with an ![image of a cat](https://www.pathtocat.com)"
        text2 = "This is an example of a url [link text](https://www.yourmom.com)"
        text3 = text + text2
        text4 = text + ". This is the other ![image of a dog](https://www.pathtodog.com)."
        expected = [("image of a cat","https://www.pathtocat.com")]
        expected2 = []
        expected3 = [("image of a cat","https://www.pathtocat.com")]
        expected4 = [("image of a cat","https://www.pathtocat.com"),
                     ("image of a dog","https://www.pathtodog.com")]

        self.assertEqual(expected,inline_markdown.extract_markdown_images(text))
        self.assertEqual(expected2,inline_markdown.extract_markdown_images(text2))
        self.assertEqual(expected3,inline_markdown.extract_markdown_images(text3))
        self.assertEqual(expected4,inline_markdown.extract_markdown_images(text4))

    def test_extractlinks(self):
        text = "This is an example with an [image of a cat](https://www.pathtocat.com)"
        text2 = "This is an example of a url [link text](https://www.yourmom.com)"
        text3 = text + text2
        text4 = text + ". This is the other ![image of a dog](https://www.pathtodog.com)."
        expected = [("image of a cat","https://www.pathtocat.com")]
        expected2 = [("link text","https://www.yourmom.com")]
        expected3 = [("image of a cat","https://www.pathtocat.com"),
                     ("link text","https://www.yourmom.com")]
        expected4 = [("image of a cat","https://www.pathtocat.com")]

        self.assertEqual(expected,inline_markdown.extract_markdown_links(text))
        self.assertEqual(expected2,inline_markdown.extract_markdown_links(text2))
        self.assertEqual(expected3,inline_markdown.extract_markdown_links(text3))
        self.assertEqual(expected4,inline_markdown.extract_markdown_links(text4))        

    def test_nested(self):
        text = "This is an example with an"
        text2 = "![image of a ![some other image](haha) cat](https://www.pathtocat.com)"
        expected = [("image of a ![some other image](haha) cat","https://www.pathtocat.com")]
        self.assertNotEqual(inline_markdown.extract_markdown_images(text + text2),expected)

class TestSplitLink(unittest.TestCase):
    def test_empty_link_text(self):
        node1 = TextNode("Here is an empty link [](https://example.com)", TextType.TEXT)
        expected = [
                    TextNode("Here is an empty link [](https://example.com)",TextType.TEXT)
        ]
        self.assertEqual(inline_markdown.split_nodes_link([node1]),expected)

    def test_malformed_links(self):
        node2 = TextNode("Bad link [missing](", TextType.TEXT)
        node3 = TextNode("Another bad [link]no-parens", TextType.TEXT)
        expected = [TextNode("Bad link [missing](Another bad [link]no-parens", TextType.TEXT)]
        self.assertEqual(inline_markdown.split_nodes_link([node2,node3]),expected)

    def test_special_characters(self):
        node4 = TextNode("Link with [spaces and $pecial ch@rs](https://example.com/path?q=1)", TextType.TEXT)
        expected = [
                    TextNode("Link with ",TextType.TEXT),
                    TextNode("spaces and $pecial ch@rs",TextType.LINK,"https://example.com/path?q=1")
        ]
        self.assertEqual(inline_markdown.split_nodes_link([node4]),expected)

    def test_combined_edge_cases(self):
        node5 = TextNode("Here's [](empty) and [valid link](url) and [broken](", TextType.TEXT)
        expected = [
                    TextNode("Here's [](empty) and ",TextType.TEXT),
                    TextNode("valid link",TextType.LINK,"url"),
                    TextNode(" and [broken](",TextType.TEXT)
        ]
        self.assertEqual(inline_markdown.split_nodes_link([node5]),expected)

    def test_multiple_consecutive_links(self):
        node6 = TextNode("Here is an empty link [some other link](https://www.yourmom.com)[some link](https://example.com) some other text", TextType.TEXT)
        expected = [
                    TextNode("Here is an empty link ",TextType.TEXT),
                    TextNode("some other link",TextType.LINK,"https://www.yourmom.com"),
                    TextNode("some link",TextType.LINK,"https://example.com"),
                    TextNode(" some other text", TextType.TEXT)
        ]   
        self.assertEqual(inline_markdown.split_nodes_link([node6]),expected)

    def test_links_at_start_and_end(self):
        node7 = TextNode("[start link](https://start.com)middle text[end link](https://end.com)", TextType.TEXT)
        expected = [
                    TextNode("start link",TextType.LINK,"https://start.com"),
                    TextNode("middle text",TextType.TEXT),
                    TextNode("end link",TextType.LINK,"https://end.com")
        ]
        self.assertEqual(inline_markdown.split_nodes_link([node7]),expected)

    def test_space_between_text_and_link(self):
        node8 = TextNode("[some other link](https://www.yourmom.com)[some link] this would be in between the links (https://example.com)", TextType.TEXT)
        expected = [
                    TextNode("some other link",TextType.LINK,"https://www.yourmom.com"),
                    TextNode("[some link] this would be in between the links (https://example.com)",TextType.TEXT)
        ]
        self.assertEqual(inline_markdown.split_nodes_link([node8]),expected)



class TestSplitImage(unittest.TestCase):
    def test_basic_image(self):
        node1 = TextNode("Here is an image ![dog photo](dog.jpg)", TextType.TEXT)
        expected = [TextNode("Here is an image ",TextType.TEXT),
                    TextNode("dog photo",TextType.IMAGE,"dog.jpg")]

        self.assertEqual(inline_markdown.split_nodes_image([node1]),expected)

    def test_empty_alt_text(self):
        node2 = TextNode("Empty alt text ![](empty.jpg)", TextType.TEXT)
        expected = [TextNode("Empty alt text ![](empty.jpg)",TextType.TEXT)]

        self.assertEqual(inline_markdown.split_nodes_image([node2]),expected)

    def test_malformed_images(self):
        node3 = TextNode("Bad image ![missing](", TextType.TEXT)
        node4 = TextNode("Another bad ![image]no-parens", TextType.TEXT)
        expected = [TextNode("Bad image ![missing](Another bad ![image]no-parens",TextType.TEXT)]

        self.assertEqual(inline_markdown.split_nodes_image([node3,node4]),expected)

    def test_special_characters_in_alt_text(self):
        node5 = TextNode("Image with ![spaces & $pecial ch@rs](special.png)", TextType.TEXT)
        expected = [TextNode("Image with ",TextType.TEXT),
                    TextNode("spaces & $pecial ch@rs",TextType.IMAGE,"special.png")]
        
        self.assertEqual(inline_markdown.split_nodes_image([node5]),expected)

    def test_multiple_consecutive_images(self):
        node6 = TextNode("Start ![img1](url1.jpg)![img2](url2.jpg) end", TextType.TEXT)
        expected = [
                    TextNode("Start ",TextType.TEXT),
                    TextNode("img1",TextType.IMAGE,"url1.jpg"),
                    TextNode("img2",TextType.IMAGE,"url2.jpg"),
                    TextNode(" end",TextType.TEXT)
        ]
        self.assertEqual(inline_markdown.split_nodes_image([node6]),expected)

    def test_image_at_start(self):
        node7 = TextNode("![first](start.jpg)some text", TextType.TEXT)
        expected = [
                    TextNode("first",TextType.IMAGE,"start.jpg"),
                    TextNode("some text",TextType.TEXT)
        ]
        self.assertEqual(inline_markdown.split_nodes_image([node7]),expected)

    def test_mix_of_valid_and_invalid(self):
        node8 = TextNode("![valid](good.jpg) and ![broken](", TextType.TEXT)
        expected = [
                    TextNode("valid",TextType.IMAGE,"good.jpg"),
                    TextNode(" and ![broken](",TextType.TEXT)
        ]
        self.assertEqual(inline_markdown.split_nodes_image([node8]),expected)

    def test_combined_edge_cases(self):
        node9 = TextNode("Here's ![](empty) and ![valid image](dog.png) and ![broken](",TextType.TEXT)
        expected = [
                    TextNode("Here's ![](empty) and ",TextType.TEXT),
                    TextNode("valid image",TextType.IMAGE,"dog.png"),
                    TextNode(" and ![broken](",TextType.TEXT)
        ]
        self.assertEqual(inline_markdown.split_nodes_image([node9]),expected)


class TestTextToNodes(unittest.TestCase):
    def test_case1(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
                    TextNode("This is ", TextType.TEXT),
                    TextNode("text", TextType.BOLD),
                    TextNode(" with an ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" word and a ", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode(" and an ", TextType.TEXT),
                    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode(" and a ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "https://boot.dev"),
                ]
        
        self.assertEqual(inline_markdown.text_to_textnodes(text),expected)

    def test_case2(self):
        text = "This is going to be interesting **bold *italic*** I feel like what I expect `is exactly` what I want to happen"
        # This should throw an exception because after finding the bold text I 
        # try to find the italic text which would throw an exception if there
        # was an unclosed italic delimiter which there is below!
        expected = [
                    TextNode("This is going to be interesting ",TextType.TEXT),
                    TextNode("bold *italic", TextType.BOLD),
                    TextNode("* I feel like what I expect ",TextType.TEXT),
                    TextNode("is exactly",TextType.CODE),
                    TextNode(" what I want to happen",TextType.TEXT),
        ]

        # This should raise an exception because I attempt to 
        with self.assertRaises(Exception):
            inline_markdown.text_to_textnodes(text)

    def test_case3(self):
        text = "![here is an image](puppy.jpg) what is up pookies she is **sleepy [link](https://toyourmom.com)** *this is going to be italics* haha"
        expected = [
                    TextNode("here is an image",TextType.IMAGE,"puppy.jpg"),
                    TextNode(" what is up pookies she is ",TextType.TEXT),
                    TextNode("sleepy [link](https://toyourmom.com)",TextType.BOLD),
                    TextNode(" ",TextType.TEXT),
                    TextNode("this is going to be italics",TextType.ITALIC),
                    TextNode(" haha",TextType.TEXT),
        ]
        self.assertEqual(inline_markdown.text_to_textnodes(text),expected)

    def test_case4(self):
        text = "![](puppy.jpg)**bold** `this is some code for you to render `[`link with code`](www.haha.com)"
        expected = [TextNode("![](puppy.jpg)", TextType.TEXT),
                     TextNode("bold", TextType.BOLD),
                     TextNode(" ", TextType.TEXT),
                     TextNode("this is some code for you to render ", TextType.CODE),
                     TextNode("[", TextType.TEXT),
                     TextNode("link with code", TextType.CODE),
                     TextNode("](www.haha.com)", TextType.TEXT)]
        self.assertEqual(inline_markdown.text_to_textnodes(text),expected)