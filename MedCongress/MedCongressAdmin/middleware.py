import json
from django.http import JsonResponse,HttpResponse
from django.core.exceptions import RequestDataTooBig


class CheckSize(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        try:
            body = request.body
        except RequestDataTooBig:
           
            data = json.dumps({"msg": "The file provided is too large. Please reduce its size and try again."})
            mimetype = "application/json"
            return HttpResponse(data, mimetype)
        response = self.get_response(request)
        return response