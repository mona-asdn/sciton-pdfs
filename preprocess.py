from pathlib import Path
import os
import csv

# search_term = "final efficiency"
search_queries = ["final efficiency", "> 15", ">15", "burn-in shots"]

def process_text(text):
    if text:
        lines = text.splitlines()
        allow_start = False
        for line in lines:
            # if "final efficiency" in line.lower():
            #     allow_start = True
            # if allow_start and line.lower().startswith("syst"):
            #     return line
            for search_term in search_queries:
                if search_term in line.lower():
                    return line,search_term
    return None, None

if __name__ == "__main__":
    script_dir = Path(__file__)
    results_dir = Path(os.path.join(script_dir.parent, "results"))
    rows = []
    index = 0
    for filename in results_dir.glob("**/*.txt"):
        print(filename)
        with open(filename, 'r') as f:
            text = f.read()
        processed_text, search_term = process_text(text)
        # if processed_text:
        rows.append([index, filename.name, processed_text, search_term])
        index += 1
        if index % 100 == 0:
            print("Processed {} files.".format(index))

    # Save rows to CSV
    with open('results.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    
    print("Done.")