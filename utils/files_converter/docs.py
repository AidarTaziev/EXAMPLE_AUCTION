import os
import comtypes.client

def convert_doc_to_pdf(in_file_path, output_file_path):
    wdFormatPDF = 17

    in_file = os.path.abspath(in_file_path)
    out_file = os.path.abspath(output_file_path)

    word = comtypes.client.CreateObject('Word.Application')
    doc = word.Documents.Open(in_file)
    doc.SaveAs(out_file, FileFormat=wdFormatPDF)
    doc.Close()
    word.Quit()
