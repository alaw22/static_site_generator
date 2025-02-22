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
def list_block_to_nodes(split_block,list_type):
    match list_type:
        case BlockType.UNORDERED:
            chars = "*- "
        case BlockType.ORDERED:
            chars = "123456789. "
        case _:
            raise Exception(f"Got unexpected block type {list_type}")
        
    list_items = []
    for item in split_block:
        stripped = item.lstrip(chars) # this may be a problem if there is bold or italic text to start
        list_items.append(HTMLNode("li",stripped))

    return list_items


def block_to_html_node(block,block_type):
    split_block = block.split("\n")

    match block_type:
        case BlockType.PARAGRAPH:
            return HTMLNode("p",block)
        case BlockType.HEADING:
            return HTMLNode(header_block_to_tag(block),block.lstrip("# "))
        case BlockType.CODE:
            return HTMLNode("code",block)
        case BlockType.QUOTE:
            
            return HTMLNode("blockquote")
        case BlockType.UNORDERED:
            list_items = list_block_to_nodes(split_block,BlockType.UNORDERED)
            parent = HTMLNode("ul",children=list_items)
            return parent 
        case BlockType.ORDERED:
            list_items = list_block_to_nodes(split_block,BlockType.ORDERED)
            parent = HTMLNode("ol",children=list_items)
            return parent 
        case _:
            raise Exception("Block type doesn't exist")


def markdown_to_html(markdown):
    # convert to blocks
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_type = block_to_block_type(block)

        HTMLNode()




    