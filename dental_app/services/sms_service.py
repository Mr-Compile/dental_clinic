"""SMS notifications via the Semaphore API."""
import logging
from datetime import datetime

import requests

from dental_app.core.config import (
    SEMAPHORE_API_KEY,
    SEMAPHORE_API_URL,
    SEMAPHORE_SENDER_NAME,
)
from dental_app.utils.formatting import format_time

log = logging.getLogger(__name__)


class SMSService:
    def __init__(self):
        self.api_key = SEMAPHORE_API_KEY

    def send_appointment_notification(self, phone_number, appointment_data, action):
        """Returns (ok, message)."""
        if not self.api_key:
            return False, "SMS service not configured (SEMAPHORE_API_KEY missing)"

        try:
            date_value = appointment_data["appointment_date"]
            if isinstance(date_value, datetime):
                date_obj = date_value
            else:
                date_obj = datetime.strptime(str(date_value), "%Y-%m-%d")

            formatted_time = format_time(str(appointment_data["appointment_time"]))
            formatted_date = date_obj.strftime("%y/%m/%d")
            client_name = appointment_data.get("client_name", "Dear Client")
            service = appointment_data["service"]

            if action == "confirmed":
                message = (
                    f"Hi {client_name}, your dental appointment has been confirmed for "
                    f"{formatted_date} at {formatted_time}. Service: {service}"
                )
            elif action == "cancelled":
                message = (
                    f"Hi {client_name}, your dental appointment for {formatted_date} "
                    f"at {formatted_time} has been cancelled. "
                    f"Please contact us if you have any questions."
                )
            elif action == "completed":
                message = (
                    f"Hi {client_name}, thank you for visiting our dental clinic. "
                    f"Your appointment for {formatted_date} at {formatted_time} "
                    f"has been completed. We hope to see you again!"
                )
            else:
                return False, "Invalid notification type"

            if phone_number.startswith("09"):
                phone_number = "+63" + phone_number[1:]

            log.info("Sending SMS notification to %s", phone_number)

            response = requests.post(
                SEMAPHORE_API_URL,
                json={"number": phone_number, "message": message,
                      "sendername": SEMAPHORE_SENDER_NAME},
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=15,
            )
            result = response.json()

            if response.status_code == 200:
                return True, "SMS notification sent successfully"
            error_msg = result.get("message", "Unknown error")
            log.error("SMS failed: %s", error_msg)
            return False, error_msg

        except Exception as err:
            log.error("Failed to send SMS: %s", err)
            return False, f"Failed to send SMS: {err}"
