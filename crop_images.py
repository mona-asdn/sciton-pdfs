import os
import io
import csv
import re
from pathlib import Path
from PIL import Image
import pytesseract

configs = [
    {
        "report_type": 1,
        "search_queries": [">15", "finalefficiency"],
        "left_margin": 250,
        "width_margin": 170,
        "top_margin": -30,
        "height_margin": 70
    },
    {
        "report_type": 2, # system initialization
        "search_queries": [">15", "finalefficiency"],
        "left_margin": -100,
        "width_margin": 50,
        "top_margin": -20,
        "height_margin": 30
    },
    {
        "report_type": 3,  #bbl final
        "search_queries": ["695nm","696nm"], ## The word Sys: Efficieny is usually not found in the text, so we use another row then adjust the margins
        "left_margin": 180,
        "width_margin": 80,
        "top_margin": 170,
        "height_margin": 40
    }
]

def match_search_query(word, search_queries):
    # At least a part of the search query should match the word
    for query in search_queries:
        query_regex = re.escape(query)
        if re.search(query_regex, word, re.IGNORECASE):
            return True

    return False


def get_report_type(extracted_data):
    report_type = None
    text = " ".join(extracted_data["text"]).lower().replace(" ", "")   # remove all spaces in text
  
    if "bblfinal" in text:
        report_type = 3
    elif "systeminitialization" in text:
        report_type = 2
    else:  # "device history record" in text:
        report_type = 1


    return report_type

def get_margins(report_type):
    for c in configs:
        if c["report_type"] == report_type:
            return c
    return None

def search_and_crop_text(image_path, output_path):
    # Load the image
    image = Image.open(image_path)

    # Convert the image to grayscale for better OCR accuracy
    image = image.convert("L")

    # Perform OCR on the image to extract text and bounding box coordinates
    extracted_data = pytesseract.image_to_data(
        image, output_type=pytesseract.Output.DICT)
    report_type = get_report_type(extracted_data)
    config = get_margins(report_type)
    if config is None or report_type !=3:
        print(f"Unknown report type for {image_path}")
        return ""
    # Find the bounding box coordinates that enclose the search text
    search_box = None
    for i, word in enumerate(extracted_data["text"]):
        wl = word.lower().replace(" ", "")
        if len(wl) > 0:
            word_window = extracted_data["text"][i-1] + word + \
                extracted_data["text"][i+1] if i + \
                1 < len(extracted_data["text"]) else ""
            word_window = word_window.lower().replace(" ", "")
            search_queries = config["search_queries"]
            if match_search_query(wl, search_queries) or match_search_query(word_window, search_queries):
                left = extracted_data["left"][i] + config["left_margin"]
                top = extracted_data["top"][i] + config["top_margin"]
                width = extracted_data["width"][i] + config["width_margin"]
                height = extracted_data["height"][i] + config["height_margin"]
                search_box = (left, top, left + width, top + height)
                break

    if search_box is not None:
        # Crop the image based on the bounding box
        cropped_image = image.crop(search_box)

        # Save the cropped image to the output path
        cropped_image.save(output_path)
        print(f"Cropped image saved to {output_path}")
        return output_path
    else:
        print(f"Search text not found in the image: {image_path}")
        return ""


if __name__ == "__main__":
    script_dir = Path(__file__)
    images_dir = Path(os.path.join(script_dir.parent, "images"))
    rows = []
    index = 0
    for image_path in images_dir.glob("**/*.jpg"):
        index += 1
        # if not image_path.name.endswith("50597 s2022-01-24.pdf.jpg"):
        #      continue
        output_path = os.path.join(
            script_dir.parent, "cropped_images", image_path.name.replace(".pdf.jpg", "_cropped.jpg"))

        # Search for the text and crop the image
        saved_path = search_and_crop_text(image_path, output_path)
        row = [index, image_path, saved_path]
        rows.append(row)

    # Write the results to a CSV file
    csv_header = ['Index', 'Input_Path', 'Cropped_Path']
    report_path = os.path.join(
        script_dir.parent, "cropped_images", "report.csv")

    with open(report_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(csv_header)
        writer.writerows(rows)
