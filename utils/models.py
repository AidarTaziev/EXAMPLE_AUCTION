from django.db import models

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=255, unique=True, verbose_name="Заголовок")
    date = models.DateField(verbose_name="Дата статьи")
    write_time = models.DateTimeField(auto_now=True)
    text = models.TextField(verbose_name="Текст статьи")
    link = models.CharField(max_length=255, verbose_name="Ссылка")
