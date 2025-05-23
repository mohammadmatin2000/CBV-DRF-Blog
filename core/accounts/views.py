from django.http import HttpResponse
from .tasks import sendemail
# ======================================================================================================================
def send_email(request):
    sendemail.delay()
    return  HttpResponse("<h1>NICE MATIN</h1>")
# ======================================================================================================================
