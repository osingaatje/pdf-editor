from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import DecodedStreamObject, EncodedStreamObject, NameObject


def replace_text(content :str, replacements = dict()):
    lines = content.splitlines()

    result :list[str] = []
    in_text :bool = False

    for line in lines:
        if line == "BT": # denotes whether we're in text (presumably)
            in_text = True

        elif line == "ET": # exiting text (presumably)
            in_text = False
        
        if in_text:
            cmd = line[-2:]
            if cmd.lower() == 'tj':
                replaced_line = line
                for k, v in replacements.items():
                    replaced_line = replaced_line.replace(k, v)
                result.append(replaced_line)
            else:
                result.append(line)
            continue

        result.append(line)

    return "\n".join(result)


def process_data(object :DecodedStreamObject | EncodedStreamObject, replacements):
    data = object.get_data()
    decoded_data = data.decode('utf-8')

    replaced_data = replace_text(decoded_data, replacements)

    encoded_data = replaced_data.encode('utf-8')
    if object.decoded_self is not None:
        object.decoded_self.set_data(encoded_data)
    else:
        object.set_data(encoded_data)

FILE_IN_PATH = "files/2024-03-26_Sponsorpakketten_JFO_tickets.pdf"
FILE_OUT_PATH = "edit/2024-03-26_Sponsorpakketten_JFO_tickets-EDITED.pdf"


# Replace strings with other strings
# NOTE: MAKE SURE THE PDF INCLUDES ALL FONTS, SO WE CAN EDIT THE TEXT LATER WITHOUT GETTING WEIRD FONT ISSUES!!!
REPLACEMENTS :dict[str, str] = {"#2025_000111222333": "#2025_1234567890123"}

def replace_strings_in_pdf(file_in_path :str, file_out_path :str, replacements :dict[str,str]):
    """
        KNOWN BUG: SHOWS ALL HIDDEN LAYERS.
    """
    
    pdf = PdfReader(file_in_path)
    writer = PdfWriter()

    writer.add_metadata(pdf.metadata)

    for page in pdf.pages:
        contents = page.get_contents()

        if isinstance(contents, DecodedStreamObject) or isinstance(contents, EncodedStreamObject):
            process_data(contents, replacements)
        elif len(contents) > 0:
            for obj in contents:
                if isinstance(obj, DecodedStreamObject) or isinstance(obj, EncodedStreamObject):
                    streamObj = obj.get_object()
                    process_data(streamObj, replacements)

        # Force content replacement
        # page[NameObject("/Contents")] = contents.decoded_self
        page[NameObject("/Contents")] = contents
        writer.add_page(page)

    with open(file_out_path, 'wb') as out_file:
        writer.write(out_file)


if __name__ == "__main__":
    replace_strings_in_pdf(FILE_IN_PATH, FILE_OUT_PATH, REPLACEMENTS)
