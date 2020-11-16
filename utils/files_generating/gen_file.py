import os
import os.path
import threading
import logging
import time
import sys
# import pythoncom
# import comtypes.client
from django.conf import settings
from docxtpl import DocxTemplate
from django.template.loader import get_template
from utils.files_generating.gen_watermark import add_watermark_to_pdf


logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'EXAMPLE_AUCTION.log')


def generate_bidding_protocol_for_deal(deal):
    auction_data = deal.bet.auction.get_display_data()
    auction_data['deal'] = deal.get_display_data()
    auction_data['client_company'] = deal.bet.client.get_user_company_data()
    auction_data['seller_company'] = deal.bet.auction.seller.get_user_company_data()

    output_full_path = 'media/bidding_protocols/auctions/pdfs/protocollAuction{auction_id}Deal{deal_id}.pdf'. \
        format(auction_id=deal.bet.auction.id, deal_id=deal.id)

    if not os.path.exists(output_full_path):
        generate_pdf('docx_templates/bidding_protocol.html', auction_data, output_full_path)

    return output_full_path


def generate_word_bidding_protocol(protocol_path, protocol_propertys):
    tpl = DocxTemplate('media/docs_examples/protocol_tmpl.docx')
    tpl.render(protocol_propertys)
    tpl.save(protocol_path)


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
    return path


def generate_pdf(template_path, context, output_full_path):
    '''
    Функция, генерирующая pdf из html шаблона.
    :param template_path: путь до html шаблона
    :param context: контекст для html
    :param output_full_path: полный путь файла, то где он должен будет лежать
    :return:
    '''

    if not settings.LOCAL_SETTINGS:
        from weasyprint import HTML

        html_template = get_template(template_path)
        rendered_html = html_template.render(context).encode(encoding="UTF-8")
        pdf_file = HTML(string=rendered_html, base_url=settings.BASE_URI).write_pdf()
        temp_file_path = '{output_full_path}temp_file.pdf'.format(output_full_path=output_full_path)

        try:
            result_file = open(temp_file_path, "wb+")
            print(result_file)

            result_file.write(pdf_file)
            result_file.close()

            if pdf_file:
                add_watermark_to_pdf('media/docs_examples/kartli_watermark.pdf', temp_file_path, output_full_path)
        except Exception as ex:
            print(ex)
        finally:
            os.remove(temp_file_path)
    else:
        print('...protocol generationg...')
