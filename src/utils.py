import re
from textnode import TextNode, TextType

# This function does not support multple nesting so italic
# inside of bold for example. I would like to extend 
# The functionality of this eventually
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    n_delimiter = len(delimiter)
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        opening = None
        closing = None
        for i in range(len(node.text)):
            if node.text[i:i+n_delimiter] == delimiter:
                if opening is None:
                    opening = i
                elif closing is None:
                    closing = i
                    break
        
        if closing is None and opening is None:
            new_nodes.append(node)
            continue           

        if (closing is not None and opening is None) or \
            (opening is not None and closing is None):
            raise Exception("Invalid markdown: delimiter not closed")
        
        if node.text[:opening]:
            new_nodes.append(TextNode(node.text[:opening],TextType.TEXT))
        if node.text[opening+n_delimiter:closing]:
            new_nodes.append(TextNode(node.text[opening+n_delimiter:closing],text_type))
        if node.text[closing+n_delimiter:]:
            last_node = TextNode(node.text[closing+n_delimiter:],TextType.TEXT)
            recursive_nodes = split_nodes_delimiter([last_node],delimiter,text_type)
            new_nodes.extend(recursive_nodes)

    return new_nodes 


def extract_markdown_images(text):
    regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(regex,text)

def extract_markdown_links(text):
    # This first part of this regex is to say
    # Throw away any matches that start with a !
    regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(regex,text)

