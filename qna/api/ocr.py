import os
import dotenv
import requests
dotenv.load_dotenv()


APP_ID = os.getenv("MATHPIX_APP_ID")
APP_KEY = os.getenv("MATHPIX_APP_KEY")


def call_ocr_api(file):
    response = requests.post("https://api.mathpix.com/v3/text",
        files = {
            "file": file
        },
        headers = {
            "app_id": APP_ID,
            "app_key": APP_KEY,
        },
    )
    data = response.json()

    if response.status_code == 200:
        return {
            "status": response.status_code,
            "confidence": data["confidence"],
            "confidence_rate": data["confidence_rate"],
            "text": data["text"],
        }

    else:
        return {
            "status": response.status_code,
            "confidence": 0,
            "confidence_rate": 0,
            "error": data["error"],
        }