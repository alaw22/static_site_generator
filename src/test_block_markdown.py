from block_markdown import block_to_block_type, markdown_to_blocks, BlockType
import unittest



class TestBlocktoBlockType(unittest.TestCase):
    def test_empty_block(self):
        self.assertEqual(BlockType.PARAGRAPH,block_to_block_type(""))

    def test_full_quote(self):
        markdown = """
                    # Introduction

                    Hello, my name is Alex, and I love Astronomy.

                    ## Quotation

                    > Don't ever let your grits run dry
                    > and don't ever let your wits get the best of you    
                    """
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(BlockType.QUOTE,block_to_block_type(blocks[-1]))

    def test_incomplete_quote(self):
        markdown = """
                    # Introduction

                    Hello, my name is Alex, and I love Astronomy.

                    ## Quotation

                    > Don't ever let your grits run dry
                    and don't ever let your wits get the best of you    
                    """
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(BlockType.PARAGRAPH,block_to_block_type(blocks[-1]))
    
    def test_unordered_list(self):
        markdown = """
                    # Introduction

                    Hello, my name is Alex, and I love Astronomy.

                    ## Unordered List

                    * Don't ever let your grits run dry
                    - and don't ever let your wits get the best of you    
                    """
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(BlockType.UNORDERED,block_to_block_type(blocks[-1]))

    def test_incomplete_unordered_list(self):
        markdown = """
                    # Introduction

                    Hello, my name is Alex, and I love Astronomy.

                    ## Unordered List

                    * Don't ever let your grits run dry
                    and don't ever let your wits get the best of you    
                    """
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(BlockType.PARAGRAPH,block_to_block_type(blocks[-1]))

    def test_long_code(self):
        markdown = """
                    # Introduction

                    Hello, my name is Alex, and I love Astronomy.

                    ## Code

                    ```
                    This is going to be the longest code block
                    in human history...jk
                    ```
                    
                    """
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(BlockType.CODE,block_to_block_type(blocks[-1]))

    def test_incomplete_code(self):
        markdown = """
                    # Introduction

                    Hello, my name is Alex, and I love Astronomy.

                    ## Code

                    ```
                    This is going to be the longest code block
                    in human history...jk
                    
                    """
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(BlockType.PARAGRAPH,block_to_block_type(blocks[-1]))
            
    def test_headings(self):
        markdown = """
                    # Introduction

                    Hello, my name is Alex, and I love Astronomy.

                    ## Code

                    ```
                    This is going to be the longest code block
                    in human history...jk
                    
                    """
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(BlockType.HEADING,block_to_block_type(blocks[2]))
        self.assertEqual(BlockType.HEADING,block_to_block_type(blocks[0]))

    def test_bad_headings(self):
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
        self.assertEqual(BlockType.HEADING,block_to_block_type(blocks[2]))
        self.assertNotEqual(BlockType.HEADING,block_to_block_type(blocks[0]))
        self.assertNotEqual(BlockType.HEADING,block_to_block_type(blocks[-1]))

class TestTextToBlock(unittest.TestCase):
    def test_leading_and_trailing_whitespace(self):
        markdown = '''  Hello there sir,
This is your captain speaking

* I would like to raise a toast
* A toast to my lovely bride
* For being the fairest of them all

        '''

        expected = ["Hello there sir,\nThis is your captain speaking",
                    "* I would like to raise a toast\n* A toast to my lovely bride\n* For being the fairest of them all"]
        
        result = markdown_to_blocks(markdown)
        self.assertEqual(result,expected)

    def test_bootdev_example(self):
        markdown = """# This is a heading

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

        * This is the first list item in a list block
        * This is a list item
        * This is another list item"""

        expected = ["# This is a heading",
                    "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                    "* This is the first list item in a list block\n        * This is a list item\n        * This is another list item"]
    
        result = markdown_to_blocks(markdown)
    
        self.assertEqual(result,expected)