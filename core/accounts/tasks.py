from celery import shared_task  # Importing Celery for asynchronous task execution
from django.http import HttpResponse  # Importing HttpResponse to return an HTML response
from time import sleep  # Importing sleep to simulate delay

# ======================================================================================================================
# Defining an asynchronous task for sending emails
@shared_task  # Marks this function as a Celery task
def sendemail():
    """
    Simulates sending an email asynchronously with a 3-second delay.
    """
    sleep(3)  # Simulating processing delay before sending the email
    return HttpResponse("<h1>Email sent!</h1>")  # Returning an HTML response upon completion

# ======================================================================================================================