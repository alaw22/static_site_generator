from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED = "unordered_list"
    ORDERED = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = []
    lines = markdown.split("\n")

    temp = []
    for i in range(len(lines)):
        if lines[i] == "" or lines[i].isspace(): # empty line or line with just space or last line
            block = "\n".join(temp).strip()
            if block:
                blocks.append(block)
            temp = []
            continue
        
        temp.append(lines[i])
    
    if len(temp) > 0:
        blocks.append("\n".join(temp).strip())

    
    return blocks

# solution files
"""
def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks
"""

def block_to_block_type(block):
    if not block.strip():
        return BlockType.PARAGRAPH
    
    split_block = block.split("\n")

    if block.startswith("#"):
        hashes = 0
        if len(block) <= 1:
            return BlockType.PARAGRAPH
        
        for char in block:
            if char == "#":
                hashes += 1
            else:
                break
        
        if block[hashes] != " " or hashes > 6:
            return BlockType.PARAGRAPH
        
        elif hashes <= 6 and block[hashes+1:].strip():
            return BlockType.HEADING

                 
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
        
    elif all(line.lstrip().startswith(">") for line in split_block):
        return BlockType.QUOTE
        
    elif all(line.lstrip().startswith(("* ","- ")) for line in split_block):
        return BlockType.UNORDERED
        
    elif all(line.lstrip().startswith(f"{i}. ") for i,line in enumerate(split_block,1)):
        return BlockType.ORDERED

    return BlockType.PARAGRAPH
    
if __name__ == "__main__":
    markdown = """
                #Introduction

                Hello, my name is Alex, and I love Astronomy.

                ## Code

                ```
                This is going to be the longest code block
                in human history...jk

                ####### Testing 7 hashes to see if it is a paragraph                    
                """

    blocks = markdown_to_blocks(markdown)

    print(blocks)
    print(block_to_block_type(blocks[-1]))