from celery import shared_task
from django.http import HttpResponse
from time import sleep
# ======================================================================================================================
@shared_task
def sendemail():
    sleep(3)
    return HttpResponse("<h1>Email sent!</h1>")
# ======================================================================================================================