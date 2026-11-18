
import requests


def check_device(device_url, timeout=3):
    """
    Check whether the ESP32-S3 HTTP server responds.
    """

    try:
        url = device_url.rstrip("/") + "/health"

        response = requests.get(
            url,
            timeout=timeout
        )

        response.raise_for_status()
        return response.json()

    except requests.RequestException as error:
        return {
            "status": "disconnected",
            "error": str(error)
        }

    except ValueError:
        return {
            "status": "error",
            "error": "Invalid JSON response"
        }


def send_text(device_url, text, timeout=10):
    """
    Send text to ESP32-S3 for future on-device processing.
    """

    try:
        url = device_url.rstrip("/") + "/infer"

        response = requests.post(
            url,
            json={"text": text},
            timeout=timeout
        )

        response.raise_for_status()
        return response.json()

    except requests.RequestException as error:
        return {
            "status": "error",
            "error": str(error)
        }

    except ValueError:
        return {
            "status": "error",
            "error": "Invalid JSON response"
        }
