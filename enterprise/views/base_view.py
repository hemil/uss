import json
import logging
from django.http import HttpResponse
from rest_framework.decorators import api_view


logger = logging.getLogger("enterprise")


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def ping(request):
    try:
        return HttpResponse("The Wrath of Khan is on.", status=200)
    except Exception as e:
        return HttpResponse(json.dumps({
            'status': 0,
            'message': "Exception: {e}".format(e=e),
            'error_code': 500,
            'data': None
        }), content_type="application/json", status=500)
