import mimetypes
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.http import JsonResponse as JSON


def create_response_object(error, data):
    return JSON({'error': error, 'data': data})


def get_file_page(request, full_path_way):
    try:
        fp = open(full_path_way, "rb")
        response = HttpResponse(fp.read())
        fp.close()

        file_type = mimetypes.guess_type(full_path_way)
        print('file type - ', file_type)
        if file_type is None:
            file_type = 'application/octet-stream'
        # response['Content-Type'] = 'application/pdf'
        response['Content-Type'] = file_type[0]

    except IOError:
        response = HttpResponseNotFound('<h1>Данного файла не существует!</h1>')

    return response