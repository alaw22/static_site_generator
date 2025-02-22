import re
from textnode import TextNode, TextType

# Extraction methods
def extract_markdown_images(text):
    regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(regex,text)

def extract_markdown_links(text):
    # This first part of this regex is to say
    # Throw away any matches that start with a !
    regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(regex,text)

# split methods

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

    # Get rid of all empty strings if they exist
    final_nodes = []
    for node in new_nodes:
        if node.text == "":
            continue
        final_nodes.append(node)

    return final_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        # If there is an empty string node don't append
        if node.text == "":
            continue

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # Extract images 
        extracted = extract_markdown_images(node.text)

        # If there is no image then append node and continue
        if len(extracted) == 0:
            new_nodes.append(node)
            continue
        
        # This logic assumes re extracted images in order
        temp_text = node.text
        for alt_text, uri in extracted:
            text_split = temp_text.split(f"![{alt_text}]({uri})", 1)
            cutoff_index = len(text_split[0]) + len(alt_text) + len(uri) + 5  

            if alt_text == "":
                new_nodes.append(TextNode(temp_text[:cutoff_index],TextType.TEXT))
            else:
                if text_split[0] != "":
                    new_nodes.append(TextNode(text_split[0],TextType.TEXT))

                new_nodes.append(TextNode(alt_text,TextType.IMAGE,uri))

            temp_text = temp_text[cutoff_index:]
        
        if len(text_split[1]) > 0:
            new_nodes.append(TextNode(text_split[1],TextType.TEXT))

    # combine any consecutive text nodes
    final_nodes = []
    for node in new_nodes:
        if len(final_nodes) != 0 and node.text_type == TextType.TEXT and \
            final_nodes[-1].text_type == TextType.TEXT:
            final_nodes[-1].text += node.text
        else:
            final_nodes.append(node)

    return final_nodes

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        # If there is an empty string node don't append
        if node.text == "":
            continue

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # Extract links 
        extracted = extract_markdown_links(node.text)

        # If there is no link then append node and continue
        if len(extracted) == 0:
            new_nodes.append(node)
            continue
        
        # This logic assumes re extracted links in order
        temp_text = node.text
        for ltext, link in extracted:
            text_split = temp_text.split(f"[{ltext}]({link})", 1)
            cutoff_index = len(text_split[0]) + len(ltext) + len(link) + 4      

            if ltext == "":
                new_nodes.append(TextNode(temp_text[:cutoff_index],TextType.TEXT))
            else:
                if text_split[0] != "":
                    new_nodes.append(TextNode(text_split[0],TextType.TEXT))

                new_nodes.append(TextNode(ltext,TextType.LINK,link))

            temp_text = temp_text[cutoff_index:]
        
        if len(text_split[1]) > 0:
            new_nodes.append(TextNode(text_split[1],TextType.TEXT))

    # combine any consecutive text nodes
    final_nodes = []
    for node in new_nodes:
        if len(final_nodes) != 0 and node.text_type == TextType.TEXT and \
            final_nodes[-1].text_type == TextType.TEXT:
            final_nodes[-1].text += node.text
        else:
            final_nodes.append(node)

    return final_nodes

# This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)
def text_to_textnodes(text):
    # Create node list to pass down the line
    original_nodes = [TextNode(text,TextType.TEXT)]
    # Find bolded text
    id_bold_nodes = split_nodes_delimiter(original_nodes,"**",TextType.BOLD)
    # Find italic text
    id_italic_nodes = split_nodes_delimiter(id_bold_nodes,"*",TextType.ITALIC)
    # Find code text
    id_code_nodes = split_nodes_delimiter(id_italic_nodes,"`",TextType.CODE)
    # Find images
    id_image_nodes = split_nodes_image(id_code_nodes)
    # Find links
    id_link_nodes = split_nodes_link(id_image_nodes)

    return id_link_nodes