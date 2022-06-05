from django.shortcuts import render
from django.http import JsonResponse, Http404

from base.models import MeduzaRecord


def index(request):
    """
    Главная.
    """
    return render(request, 'index.html')

def record(request, record_id):
    """
    Страница новости.

    record_id - id новости (экз. MeduzaRecord).
    """

    try:
        r = MeduzaRecord.objects.values('id', 'title').get(id=record_id)
    except MeduzaRecord.DoesNotExist:
        raise Http404
    else:
        context = {'id': r['id'], 'title': r['title']}
        return render(request, 'record.html', context)

def get_record(request, record_id):
    """
    Получение инфы по новости.

    record_id - id новости (экз. MeduzaRecord).
    """

    try:
        record = MeduzaRecord.objects.get(id=record_id)
    except MeduzaRecord.DoesNotExist:
        record = {}
    else:
        record = record.as_dict()

    return JsonResponse(record)

def get_records(request):
    """
    Получение инфы по новостям.

    Параметр page - номер "страницы".
    Новости подтягиваются на фронт по 10 (добавить возможность настройки?).
    Таким образом, page определяет, какой десяток новостей будет запрошен.
    page=0 - первый десяток и т.д. 
    """

    page = request.GET.get('page', 0)
    page = int(page)

    try:
        mrecords = MeduzaRecord.objects.all()[page*10:(page+1)*10]
    except:
        mrecords = MeduzaRecord.objects.none()

    records = [r.as_dict() for r in mrecords]

    return JsonResponse(records, safe=False)

def handler404(request, exception):
    """
    Кастомная страница для 404.
    """
    return render(request, '404.html')