import logging
from django.core.mail import send_mail, EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from utils.files_generating.gen_file import generate_bidding_protocol_for_deal

logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'EXAMPLE_AUCTION.log')


#TODO: УБРАТЬ ОТСЮДА
def send_bidding_protocol_for_deal(deal, title_message, html_content):
    protocol_path = generate_bidding_protocol_for_deal(deal)
    #todo: добавить проверку на то не пустые ли emails в списке
    if deal.bet.client.email:
        try:
            emails = [deal.bet.client.email, deal.bet.auction.seller.email, 'info@kartli.ch']
            group_send_file_to_emails(title_message,
                                      html_content,
                                      protocol_path,
                                      emails,
                                      )
        except Exception as ex:
            logging.warning('Send bidding protocol for deal exception: {ex}'.format(ex=ex))


def group_send_file_to_emails(message_subject, html_content, file_path, users_emails):
    '''
    Функция, отправляющая файл на указанные emails.

    :param message_subject: тема сообщения(заголовок)
    :param message: сообщение
    :param users_emails: список email юзеров
    :param file_path: путь до файла
    :return:
    '''
    for email in users_emails:
        try:
            mail = EmailMultiAlternatives(message_subject,
                                          '',
                                          settings.EMAIL_HOST_USER,
                                          [email])

            mail.attach_alternative(html_content, "text/html")
            mail.attach_file(file_path)
            mail.send(fail_silently=False)
        except Exception as ex:
            logging.warning('Send file to {email} exception: {ex}'.format(email=email, ex=ex))


def group_send_html_on_emails(message_subject, message, html_content, users_emails):
    '''
    Функция, отправляющая html файл на указанные emails.
    :param message_subject: тема сообщения(заголовок)
    :param message: сообщение
    :param html_content: html страница
    :param users_emails: список email юзеров
    :return:
    '''

    for email in users_emails:
        try:
            msg = EmailMultiAlternatives(message_subject,
                                         message,
                                         settings.EMAIL_HOST_USER,
                                         [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        except Exception as ex:
            logging.error('Send html to {email} exception: {ex}'.format(email=email, ex=ex))


def group_send_message_on_emails(message_subject, message, users_emails):
    '''
    Функция, отправляющая html файл на указанные emails.

    :param message_subject: тема сообщения(заголовок)
    :param message: сообщение
    :param html_content: html страница
    :param users_emails: список email юзеров
    :return:
    '''

    for email in users_emails:
        try:
            msg = EmailMultiAlternatives(message_subject,
                                         message,
                                         settings.EMAIL_HOST_USER,
                                         [email])
            msg.send()
        except Exception as ex:
            logging.warning('Send html to {email} exception: {ex}'.format(email=email, ex=ex))





