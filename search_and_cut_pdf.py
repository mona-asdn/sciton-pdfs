import PyPDF2
import os, csv

input_path = "./results/"
output_path = "./results_cut/"

# Search through the pdf files in results.csv
with open('results.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        if row[2]: # if the row has text
            input_pdf = row[1].replace(".txt", "")
            with open(os.path.join(input_path, input_pdf), 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num] # the page object
                    text = page.extract_text().lower() # case insensitive search
                    search_query = row[3].lower()
                    if search_query in text.lower():
                        print("Found '{}' in page {} of {}.".format(search_query, page_num, input_pdf))
                        pdf_writer = PyPDF2.PdfWriter()
                        # Add the page to the writer object
                        pdf_writer.add_page(page)
                        # Open a new PDF file in write-binary mode
                        with open(os.path.join(output_path, input_pdf) , 'wb') as output_file:
                            pdf_writer.write(output_file)
                        break # stop searching after the first instance is found (exits loop)


