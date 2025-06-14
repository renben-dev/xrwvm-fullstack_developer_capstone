# Uncomment the imports below before you add the function code
# import requests
import os
from dotenv import load_dotenv
import requests
import urllib.parse
from django.http import JsonResponse


load_dotenv()

backend_url = os.getenv(
    'backend_url', default="http://localhost:3030").strip()

if backend_url.endswith("/"):
    backend_url = backend_url[:-1]

sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/")

if not sentiment_analyzer_url.endswith("/"):
    sentiment_analyzer_url += "/"


# def get_request(endpoint, **kwargs):
# Add code for get requests to back end
def get_request(endpoint, **kwargs):
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params = params+key + "=" + value + "&"

    request_url = backend_url+endpoint+"?"+params
    print("GET from {} ".format(request_url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        return response.json()
    except Exception:
        # If any error occurs
        print("Network exception occurred")
        return JsonResponse({
            "status": 500,
            "message": "Network exception occurred"
        })


# def analyze_review_sentiments(text):
# request_url = sentiment_analyzer_url+"analyze/"+text
# Add code for retrieving sentiments
def analyze_review_sentiments(text):
    # Renzo: Encode special chars here: it wa not working before
    encoded_text = urllib.parse.quote(text)
    print(encoded_text)
    request_url = sentiment_analyzer_url+"analyze/"+encoded_text
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        sentiment = ""
        try:
            data = response.json()
            sentiment = data.get("sentiment")
        except ValueError:
            print("Response not valid JSON:", response.text)
        return sentiment
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return "neutral"
        # return JsonResponse({
        #     "status": 500,
        #     "message": f"Unexpected {err=}, {type(err)=}"
        # })


# def post_review(data_dict):
def post_review(data_dict):
    request_url = backend_url+"/insert_review"
    try:
        response = requests.post(request_url, json=data_dict)
        print(response.json())
        return response.json()
    except Exception:
        print("Network exception occurred")
        return JsonResponse({
            "status": 500,
            "message": "Network exception occurred"
        })

# Add code for posting review
