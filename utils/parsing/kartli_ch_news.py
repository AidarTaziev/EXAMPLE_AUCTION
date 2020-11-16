from urllib import request, parse
from bs4 import BeautifulSoup
from utils import models
from datetime import datetime, date, timedelta
import threading


class News():
    """
    Класс, контролирующий "свежесть" новостей
    """
    def __init__(self, host='https://kartli.ch/ru/', link='news/'):
        """
        Проверяем актуальность новостей. Либо просто выдаем новости из БД, либо
        парсим, записываем в БД и выдаем.
        """
        self.host = host
        self.link = link
        # Словарик для преобразования месяца,
        # чтобы создать экземляр объекта datetime.date(), т.к он принимает только целые значения
        self.__python_date_formating = {
            'January': 1,
            'February': 2,
            'March': 3,
            'April': 4,
            'May': 5,
            'June': 6,
            'July': 7,
            'August': 8,
            'September': 9,
            'October': 10,
            'November': 11,
            'December': 12,
        }
        if self.__news_is_exist():
            self.__news = self.__news_preparation()
            if not self.__news_is_actually():
                threading.Thread(target=self.__load_fresh_news).start()
        else:
            self.__news = self.__load_fresh_news()


    def get_news(self):
        return self.__news

    def __load_fresh_news(self):
        """
        Парсим новости с сайта и записываем их в БД без повторов по заголовку
        """

        def news_contains(parsing_news, title):
            contains = False

            for item in parsing_news:
                if item['title'] == title:
                    contains = True

            return contains

        fresh_news = News_parser(self.host, self.link).parse()

        for db_item in models.News.objects.all():
            if not news_contains(fresh_news, db_item.title):
                db_item.delete()

        for item in fresh_news:
            item_date_py = date(
                int(item['date']['year']),
                self.__python_date_formating[item['date']['month']],
                int(item['date']['day']),
                )
            news_in_db = models.News.objects.filter(title=item['title'])
            if not news_in_db:
                news_model = models.News(title=item['title'], date=item_date_py, text=item['text'], link=item['link'])
                news_model.save()
            else:
                update_date_model = news_in_db.update(write_time=datetime.now())
        return self.__news_preparation()

    def __news_preparation(self):
        """
        Преобразуем и отсортируем новости из базы данных по дате в JSON-сериализуемый формат.
        Первыми в списке идут новости, последние по публикации
        """
        news = []
        for item in models.News.objects.all().order_by('date').reverse():
            news.append({
                'title': item.title,
                'date': item.date,
                'text': item.text,
                'link': item.link,
            })
        return news

    def __news_is_exist(self):
        news_exist = models.News.objects.all()
        if news_exist:
            return True
        else:
            return False

    def __news_is_actually(self):
        """
        Проверяем актуальность новостей по дате последнего парсинга с сайта
        """
        now = datetime.now()
        if self.__news_is_exist():
            all_news = models.News.objects.latest('id')
            last_news_writing_date = all_news.write_time
            deltatime = now-last_news_writing_date
            if deltatime.total_seconds() > 4 * 60 * 60:
                return False
            else:
                return True
        else:
            return False


class News_parser():
    """
    Класс по парсингу новостей с сайта http://kartli.ch/ru/news
    """
    def __init__(self, host, link):
        """
        Загрузка html-страницы
        """
        url = parse.quote_plus(host + link, safe="/:", encoding='utf-8')
        response = request.urlopen(url)

        self.host = host
        self.link = link
        self.html = response.read()

    def __get_text(self, link):
        """
        Парсинг текста статьи с адреса, на котором расположен основной текст статьи
        """
        news = News_parser(host=self.host, link=link)
        soup = BeautifulSoup(news.html, 'html.parser')
        text_block = soup.find('div', class_='col-md-12')
        text_with_tags = soup.findAll('p')
        text = ''
        for p in text_with_tags:
            text += p.text
        return text

    def parse(self):
        """
        Парсинг страницы со списком новостей http://kartli.ch/ru/news
        Список содержит в себе заголовок, дату новости и ссылку на страницу
        новости, по которой парсим основной текст статьи в методе self.__get_text()
        """
        soup = BeautifulSoup(self.html)
        news_list = soup.findAll('div', class_='news-block news-small')
        self.news = []

        for news in news_list:
            temp = news.find('a', class_='nb-link')

            data = {
                'date': self.__get_date(news),
                'title': temp['title'],
                'text': self.__get_text(temp['href']),
                'link': self.host + temp['href'],
            }

            self.news.append(data)
        return self.news

    def __get_date(self, news):
        """
        Парсинг даты в JSON формат
        """
        day = news.find('div', class_='nb-date').text
        month = news.find('div', class_='nb-month').text
        year = news.find('div', class_='nb-year').text
        date = {
            'day': day,
            'month': month,
            'year': year,
        }
        return date
