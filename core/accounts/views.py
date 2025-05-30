from django.http import HttpResponse, JsonResponse  # Importing response utilities for HTTP and JSON responses
from django.views.decorators.cache import cache_page  # Importing cache_page for caching views
from .tasks import sendemail  # Importing asynchronous Celery task for sending emails
import requests  # Importing requests to fetch external API data

# ======================================================================================================================
# Send Email View - Handles asynchronous email sending
def send_email(request):
    """
    Asynchronously triggers the `sendemail` Celery task.
    """
    sendemail.delay()  # Calls the Celery task asynchronously to prevent blocking execution
    return HttpResponse("<h1>NICE MATIN</h1>")  # Returns a simple HTML response confirming the action

# ======================================================================================================================
# Test API View - Fetches data from an external API with caching
@cache_page(60)  # Caches the response for 60 seconds to improve performance
def test(request):
    """
    Sends a request to an external API and returns the response.
    """
    response = requests.get("https://02505983-6e95-4435-a523-127e06cc0410.mock.pstmn.io/test/delay/5")  # Fetches API data
    return HttpResponse(response)  # Returns the API response as an HTTP response

# ======================================================================================================================
# Weather API View - Retrieves weather forecast data with caching
@cache_page(20 * 60)  # Caches the response for 20 minutes to reduce API calls and improve efficiency
def weather_view(request):
    """
    Fetches current weather data for Tehran using an external API.
    """
    response = requests.get(
        "https://api.open-meteo.com/v1/forecast?latitude=35.6892&longitude=51.3890&current_weather=true"
    )  # Calls the weather API with coordinates for Tehran
    return JsonResponse(response.json())  # Converts API response to JSON and returns it

# ======================================================================================================================