from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from .tasks import sendemail
import requests

# ======================================================================================================================
def send_email(request):
    sendemail.delay()
    return HttpResponse("<h1>NICE MATIN</h1>")

# ======================================================================================================================
@cache_page(60)
def test(request):
    response = requests.get("https://02505983-6e95-4435-a523-127e06cc0410.mock.pstmn.io/test/delay/5")
    return HttpResponse(response)
# ======================================================================================================================
