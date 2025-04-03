import os
from pathlib import Path
import glob
from svglib.svglib import svg2rlg, Drawing, register_font
from reportlab.graphics import renderPDF

FILE_IN_PATH = "files/2024-03-28_Sponsorpakketten_JFO_tickets_no-guides.svg"
FILE_OUT_PATH = "edit/2024-03-28_Sponsorpakketten_JFO_tickets_no-guides_EDITED.pdf"

# Replace strings with other strings
REPLACEMENTS :dict[str, str] = {"#2025_000111222333": "#2025_1234567890123"}

#################################################################
# WARNING: MAKE SURE YOUR SVG INCLUDES AND SUBSETS *ALL* FONTS! #
#################################################################

# Take in raw file, edit text, and save as temp file:
def _replace_text_in_fontembedded_svg(input_path :str, replacements :dict[str,str], output_path :str):
    text :str
    with open(input_path, 'r') as f:
        text = f.read()
    
    for k,v in replacements.items():
        text = text.replace(k, v)

    with open(output_path, 'w') as f:
        f.write(text)

def _render_svg_to_pdf(input_path :str, output_path :str):
    drawing : Drawing = svg2rlg(FILE_IN_PATH)
    renderPDF.drawToFile(drawing, FILE_OUT_PATH)

def replace_svg_and_convert_to_pdf():
    for item in glob.glob('./fonts/**/*.*[tT][fF]'):
        normal_path_str = os.path.normpath(item)
        normal_path = Path(normal_path_str)
        
        
        # if path contains a dash, we'll take that as the separator of its weight:
        weight = 'normal'
        if '-' in normal_path_str:
            weight = normal_path_str.split('-')[-1].split('.')[0].lower()

        register_font(normal_path.stem, str(normal_path), weight=weight)



    temp_file = FILE_IN_PATH + ".temp"
    _replace_text_in_fontembedded_svg(FILE_IN_PATH, REPLACEMENTS, temp_file)
    _render_svg_to_pdf(temp_file, FILE_OUT_PATH)

    if os.path.exists(temp_file):
        os.remove(temp_file)
    else:
        err_msg = f"File {temp_file} doesn't exist??? This script is doing something wrong."
        print(err_msg)
        raise RuntimeError(err_msg)

if __name__ == "__main__":
    replace_svg_and_convert_to_pdf()

