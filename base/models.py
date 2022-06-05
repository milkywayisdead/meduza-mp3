from datetime import datetime as dt

from django.db import models
from django.conf import settings


_FMT = '%d-%m-%Y %H:%M'


class MeduzaRecord(models.Model):
    """
    Модель записи/новости.
    """

    url = models.SlugField(
        unique=True,
        verbose_name='url новости',
    )

    title = models.CharField(
        max_length=1000,
        verbose_name='Заголовок',
    )

    datetime = models.DateTimeField(
        verbose_name='Дата и время публикации',
    )

    content = models.TextField(
        verbose_name='Текст новости',
    )

    sound = models.CharField(
        default='', 
        max_length=100,
        verbose_name='Имя соответствующего mp3-файла',
    )

    class Meta:
        ordering = ['-datetime', ]

    def __str__(self):
        return self.title

    def as_dict(self):
        """
        В виде словаря.
        """

        return {
            'id': self.id,
            'url': self.url,
            'title': self.title,
            'datetime': self.datetime.strftime(_FMT),
            'datetime_msk': dt.fromtimestamp(self.datetime.timestamp() + 3600*3).strftime(_FMT),
            'content': self.content,
            'sound': self.sound if self.sound else None, 
        }

    def to_sound(self):
        """
        Преобразование текста новости в звук (формата mp3)
        и сохранение его в папку = settings.MEDIA_ROOT.
        """

        from gtts import gTTS
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(self.content, 'html.parser')
        for tag in soup.find_all():
            tag.replace_with(tag.text)

        content = soup.text.replace('\xa0', ' ')
        sound = gTTS(content, lang='ru')
        filename = f'{self.pk}.mp3'
        self.sound = filename
        sound.save(f'{settings.MEDIA_ROOT}{filename}')

        self.save()
