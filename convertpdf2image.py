from pdf2image import convert_from_path
from pathlib import Path
import os

def main():
    script_dir = Path(__file__)
    start_dir = Path(os.path.join(script_dir.parent, "results_cut"))

    for filename in start_dir.glob("**/*.pdf"):
        pages = convert_from_path(filename, single_file=True)
        pages[0].save(os.path.join("images", f"{filename}.jpg") , quality=90)

if __name__ == "__main__":
    main()