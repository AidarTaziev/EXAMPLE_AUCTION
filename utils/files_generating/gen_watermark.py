import math
import logging
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileWriter, PdfFileReader


logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'EXAMPLE_AUCTION.log')


def gen_watermark(image_path, pdf_watermark_path, width=600):
    '''
    Функция, генерирующая шаблон pdf с watermark.

    :param image_path: путь до изображения watermark
    :param pdf_watermark_path: конечный путь до pdf в который нужно добавить watermark
    :param width: ширина картинки
    :return:
    '''

    c = canvas.Canvas(pdf_watermark_path)

    c.drawImage(image_path, 0, 0, width, width * math.sqrt(2), mask='auto')

    c.save()


def add_watermark_to_pdf(pdf_watermark_path, input_pdf_path, output_pdf_path):
    '''
    Функция, добавляющая watermark на каждую страницу входящего pdf файла.
    :param pdf_watermark_path: путь до шаблона pdf с watermark
    :param input_pdf_path: путь до файла на который надо поставить watermark
    :param output_pdf_path: конечный путь до файла, место куда надо сохранить pdf с watermark
    :return:
    '''
    logging.debug('before open watermark')

    watermark = PdfFileReader(open(pdf_watermark_path, "rb"))
    logging.debug('after open watermark')
    output_file = PdfFileWriter()
    logging.debug('before open input file')
    input_file = PdfFileReader(open(input_pdf_path, "rb"))
    logging.debug('after open input file')

    page_count = input_file.getNumPages()

    for page_number in range(page_count):
        # merge the watermark with the page
        input_page = input_file.getPage(page_number)
        input_page.mergePage(watermark.getPage(0))
        # add page from input file to output document
        output_file.addPage(input_page)

    with open(output_pdf_path, "wb") as outputStream:
        output_file.write(outputStream)


