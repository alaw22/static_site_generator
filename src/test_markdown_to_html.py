from markdown_to_html import markdown_to_html
import unittest

class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_html(self):
        
        with open("src/sample_markdown.md","r") as markdown_file:
            markdown_contents = markdown_file.read()

        with open("src/sample_html.html","r") as answer_file:
            answer = answer_file.read()
        
        self.maxDiff = None
        parent_node = markdown_to_html(markdown_contents)
        self.assertEqual(answer,parent_node.to_html())

        # print(parent_node.to_html())



if __name__ == "__main__":

    TestMarkdownToHTML.test_markdown_to_html()