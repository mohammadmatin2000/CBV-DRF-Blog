from django.http import HttpResponse, JsonResponse
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
@cache_page(20 * 60)
def weather_view(request):
    response = requests.get(
        "https://api.open-meteo.com/v1/forecast?latitude=35.6892&longitude=51.3890&current_weather=true")
    return JsonResponse(response.json())
# ======================================================================================================================
