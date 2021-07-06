from django.shortcuts import render
from .func import DataPageAnalytic, GetDateFile
from django.http import HttpResponse
import json


def analytic_page(request):
    """
    Формирует страницу с аналитической информацией.
    :param request:
    :return:
    """
    data_page = DataPageAnalytic()
    return render(request, 'analytic_page.html', {'content': data_page()})


def pars_file_xml(request):
    """
    Получает файл в теле запроса и передает его в парсер.
    Возвращает пользователю информацию о результате обработки.
    :param request:
    :return:
    """
    return_dict = {'status': 200, 'text': 'Успешно!'}
    data_file = GetDateFile(request.FILES['file-xml'])
    return HttpResponse(json.dumps(return_dict), content_type="application/json")
    # if form.is_valid():
    #     AddDataFact(form.cleaned_data)
    #     return HttpResponse(json.dumps(return_dict), content_type="application/json")
    # else:
    #     return_dict['status'] = 401
    #     return_dict['text'] = 'Ошибки заполнения формы!'
    #     return_dict['errors'] = form.errors
    #
