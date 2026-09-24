import requests
from datetime import datetime
import sys

class SMSNotification:
    def __init__(self):
        self.api_key = '300bb09ebc3054c316b8c1c9b6a9c4cc'
        self.api_url = 'https://api.semaphore.co/api/v4/messages'

    def format_time(self, time_str):
        # Convert time string to datetime object
        time_obj = datetime.strptime(time_str, '%H:%M:%S')
        # Format to show only hour
        return time_obj.strftime('%I:00 %p')

    def send_appointment_notification(self, phone_number, appointment_data, action):
        try:
            # Handle the appointment date
            if isinstance(appointment_data['appointment_date'], datetime):
                date_obj = appointment_data['appointment_date']
            else:
                date_obj = datetime.strptime(str(appointment_data['appointment_date']), '%Y-%m-%d')

            # Handle the appointment time
            time_str = str(appointment_data['appointment_time'])
            formatted_time = self.format_time(time_str)
            
            # Format the date
            formatted_date = date_obj.strftime('%y/%m/%d')  # Updated to match required format
            
            # Get client name
            client_name = appointment_data.get('client_name', 'Dear Client')
            
            # Create appropriate message based on action
            if action == 'confirmed':
                message = (f"Hi {client_name}, your dental appointment has been confirmed for {formatted_date} "
                          f"at {formatted_time}. Service: {appointment_data['service']}")
            elif action == 'cancelled':
                message = (f"Hi {client_name}, your dental appointment for {formatted_date} at {formatted_time} "
                          f"has been cancelled. Please contact us if you have any questions.")
            elif action == 'completed':
                message = (f"Hi {client_name}, thank you for visiting our dental clinic. Your appointment for {formatted_date} "
                          f"at {formatted_time} has been completed. We hope to see you again!")
            else:
                print("❌ Invalid notification type", file=sys.stderr)
                return False, "Invalid notification type"

            # Ensure phone number starts with country code for Philippines
            if phone_number.startswith('09'):
                phone_number = '+63' + phone_number[1:]

            print(f"\n📱 Sending SMS notification to {phone_number}...")
            print(f"📄 Message: {message}")

            # Send SMS using Semaphore API
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'number': phone_number,
                'message': message,
                'sendername': 'DENTAL'
            }

            response = requests.post(self.api_url, json=payload, headers=headers)
            result = response.json()

            if response.status_code == 200:
                print("✅ SMS sent successfully!")
                return True, "SMS notification sent successfully"
            else:
                error_msg = result.get('message', 'Unknown error')
                print(f"❌ SMS failed: {error_msg}", file=sys.stderr)
                return False, error_msg

        except Exception as e:
            error_message = f"Failed to send SMS: {str(e)}"
            print(f"❌ {error_message}", file=sys.stderr)
            return False, error_message

    def get_remaining_texts(self):
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}'
            }
            response = requests.get('https://api.semaphore.co/api/v4/account', headers=headers)
            result = response.json()
            
            if response.status_code == 200:
                quota = result.get('credit_balance', 0)
                print(f"\nℹ️ Remaining SMS credits: {quota}")
                return quota
            else:
                print("❌ Failed to check SMS credits", file=sys.stderr)
                return None
        except Exception as e:
            print(f"❌ Failed to check SMS credits: {str(e)}", file=sys.stderr)
            return None