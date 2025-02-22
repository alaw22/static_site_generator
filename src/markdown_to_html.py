from block_markdown import *
from textnode import *
from inline_markdown import *
from htmlnode import *


def header_block_to_tag(header_block):
    hashes = 0
    for char in header_block:
        if char == "#":
            hashes += 1
        else:
            break

    return f"h{hashes}"

# Make this a more general purpose function like taking multiple lines 
# stripping specific characters and returning the stripped list of lines
def list_block_to_leafnodes(split_block, block_type):
    match block_type:
        case BlockType.UNORDERED:
            chars = "*- "
        case BlockType.ORDERED:
            chars = "123456789. "
        case _:
            raise Exception(f"Got unexpected block type {block_type}")
        
    list_items = []
    for item in split_block:
        stripped = item.lstrip(chars) # this may be a problem if there is bold or italic text to start
        list_items.append(LeafNode("li",stripped))

    return list_items


def markdown_block_to_html_node(block,block_type):
    split_block = block.split("\n")

    match block_type:
        case BlockType.PARAGRAPH:
            return LeafNode("p",block)
        case BlockType.HEADING:
            return LeafNode(header_block_to_tag(block),block.lstrip("# "))
        case BlockType.CODE:
            return LeafNode("code",block.strip("`"))
        case BlockType.QUOTE:
            list_items = []
            for item in split_block:
                list_items.append(item.lstrip("> "))
            return LeafNode("blockquote","\n".join(list_items))
        case BlockType.UNORDERED:
            list_items = list_block_to_leafnodes(split_block,block_type)
            parent = ParentNode("ul",children=list_items)
            return parent 
        case BlockType.ORDERED:
            list_items = list_block_to_leafnodes(split_block,block_type)
            parent = ParentNode("ol",children=list_items)
            return parent 
        case _:
            raise Exception("Block type doesn't exist")

def text_to_children(text):
    children = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))

    return children


def markdown_to_html(markdown):

    # convert to blocks
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        html_node = markdown_block_to_html_node(block,block_type)

        temp = []
        if html_node.children:
            for child in html_node:
                grandchildren = text_to_children(child.value)
                temp.append(ParentNode(child.tag,grandchildren))
        elif html_node.value:
            temp.extend(text_to_children(html_node.value))

        children.append(ParentNode(html_node.tag,temp))

    return ParentNode("div",children)
            



    # return ParentNode("div",children=children)

    