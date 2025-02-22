import os
import shutil

def static_copy(src, dest):
    # Can't copy anything if the source doesn't exist
    if not os.path.exists(src):
        raise FileNotFoundError("source directory doesn't exist")

    # Only if the destination directory exists do I want to delete it's contents
    if os.path.exists(dest):
        shutil.rmtree(dest)
    
    # Create directory because if it did exist it should be gone now
    os.makedirs(dest)

    # Recursively call function until entire structure of source is copied to dest
    for item in os.listdir(src):
        temp_path = os.path.join(src,item)
        if os.path.isfile(temp_path):
            print(f"Copying {temp_path} to {dest}")
            shutil.copy(temp_path,dest)
        else:
            new_dest = os.path.join(dest,item)
            static_copy(temp_path,new_dest)

if __name__ == "__main__":
    static_copy("this","test_public")
