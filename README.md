# PDF OCR and Text Extraction

The following scripts are used to extract text from PDF files and search for a specific term in the extracted text. If the term is found, the script cuts the PDF file and saves the page that contains the term in a new PDF file.

## Prerequisites

1. Preferably, use a virtual environment to install the required libraries. To do that, run the following commands:
    - `conda create --name env-pdf python=3.8`
    - `conda activate env-pdf`

2. Install `ocrmypdf` on your machine. [documentation](https://ocrmypdf.readthedocs.io/en/latest/installation.html)
   - For linux, use the following command to install ocrmdf:
     pip3 install ocrmypdf
     (apt install  ocrmypdf wouldn't install all the necessary libraries for our purpose)

4. Clone the repository:
    - `git clone https://github.com/noghte/ocrpdf.git`

5. Install the required libraries using the following command:
    - `pip install -r requirements.txt`

6. Create the following folders in the root directory:
    - `files`: contains the PDF files. Copy all the PDF files that you want to process in this folder.
    - `results`: contains the text files that are extracted from the PDF files. At the beginning, this folder is empty.
    - `results_cut`: contains the cut PDF files. At the beginning, this folder is empty.

## Files

### Pdf to text: `convertpdf2txt.py`

This script uses the `ocrmypdf` library to extract text from PDF files. It iterates over all the PDF files in the `files` folder and produces a text file for each PDF file in the `results` folder.

- It also creates the `ocr.log` file that contains the logs of the OCR process.

### Preprocessing: `preprocess.py`

This script iterates over all the text files in the `results` folder and searched for a query (e.g., `final efficiency`). It produces a CSV file, `result.csv`, with the following columns:
- `index`: row number
- `file`: the processed text file name 
- `matched line`: the line that containes the `search_term`. If the `search_term` is not found, the column is empty.
- `matched search term`: the `search_term` that is found in the text file. If the `search_term` is not found, the column is empty.


### Cut the PDF file: `search_and_cut_pdf.py`

This script iterates over all the text files listed in `result.csv` if the third column (`matched line`) is not empty. Then, it creates a new PDF file that has only one page that contains the `search_term`. The output PDF files are saved in the `cut_files` folder.

- `logs.txt`: This file contains the logs of the `search_and_cut_pdf.py` script. It contains the search term, the page number, and the PDF file name for each PDF file that contains the search term.

> NOTE: the `logs.txt` file is created manually by copying the logs from the terminal.

### Convert PDFs to images: `convertpdf2image.py`

This script converts the PDF files in the `cut_files` folder to images. The images are saved in the `images` folder.

- To convert PDFs to images (before the final OCR):
    - On Mac: `brew install poppler`
    - Otherwise: see https://pypi.org/project/pdf2image/

 ### Screenshot a section of the images: `crop_images.py`

 This script crops a section of the images based on the certain search queries (i.e., final efficiency). 
 Since the pdfs have different formats, 3 different queries are defined to search for final efficiency and the results are saved in the `cropped_images` folder.  
