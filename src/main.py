from static_copy import static_copy
from generate_page import generate_pages_recursive, generate_page

def main():

     static_copy("static","public")
     generate_pages_recursive("content","template.html","public")


if __name__ == "__main__":
     main()