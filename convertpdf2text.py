from __future__ import annotations

import logging
import sys
from pathlib import Path

import ocrmypdf
import os
import subprocess

# pylint: disable=logging-format-interpolation
# pylint: disable=logging-not-lazy


def post_process_text(text):
    if not text:
        return None

    collapsed_spaces = re.sub(r"([^\S\r\n]+)", " ", text)
    no_leading_whitespace = re.sub(
        r"([\n\r]+)([^\S\n\r]+)", '\\1', collapsed_spaces)
    no_trailing_whitespace = re.sub(
        r"([^\S\n\r]+)$", '', no_leading_whitespace)

    return no_trailing_whitespace.strip().replace("\0", " ")


def parse(self, document_path, mime_type, file_name=None):
    # This forces tesseract to use one core per page.
    os.environ['OMP_THREAD_LIMIT'] = "1"

    if mime_type == "application/pdf":
        text_original = self.extract_text(None, document_path)
        original_has_text = text_original and len(text_original) > 50
    else:
        text_original = None
        original_has_text = False

    print(text_original)

if __name__ == "__main__":
    script_dir = Path(__file__)
    start_dir = Path(os.path.join(script_dir.parent, "files"))
    results_dir = Path(os.path.join(script_dir.parent, "results"))

    log_file = script_dir.with_name('ocr.log')

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(message)s',
        filename=log_file,
        filemode='a',
    )

    ocrmypdf.configure_logging(ocrmypdf.Verbosity.default)

    ignore_list = []#[f.name for f in results_dir.glob("**/*.pdf")]

    for filename in start_dir.glob("**/*.pdf"):
        if filename.name in ignore_list:
            print(filename.name + " ignored.\n")
            continue
        logging.info(f"Processing {filename}")
        args = {
            'input_file': filename,
            'output_file': "./results/" + filename.name,
            'sidecar_file': "./results/" + filename.name + ".txt",
            'use_threads': True,
            'jobs': 16,
            # 'language': "eng",
            'output_type': "pdfa",
            'progress_bar': True
        }
        # result = ocrmypdf.ocr(**args)

        subprocess.run(['ocrmypdf', '--force-ocr', '--sidecar', args['sidecar_file'], args['input_file'], args['output_file']])



    