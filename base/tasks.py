from celery import shared_task
from base.models import MeduzaRecord


@shared_task
def create_records():
    from datetime import datetime
    import pytz
    import meduza_news

    for url in meduza_news.get_news_urls():
        try:
            n = meduza_news.get_news(url)
        except Exception as e:
            print(e)
        else:
            rec, created = MeduzaRecord.objects.get_or_create(
                url=url,
                defaults={
                    'url': url,
                    'title': n['title'],
                    'datetime': datetime.fromtimestamp(
                        n['datetime'],
                        tz=pytz.UTC,
                    ),
                    'content': n['content'],
                }
            )

            if created:
                record_to_sound.delay(rec.id)

@shared_task
def record_to_sound(record_id):
    try:
        record = MeduzaRecord.objects.get(id=record_id)
    except MeduzaRecord.DoesNotExist:
        pass
    else:
        record.to_sound()