from textnode import TextNode, TextType

def main():
     node = TextNode("Some text here",TextType.ITALIC,"https://www.boot.dev")
     print(node)
     
main()