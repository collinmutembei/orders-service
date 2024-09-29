import africastalking
from src.config import settings


class SMSMessager:
    def __init__(self):
        africastalking.initialize(
            settings.AFRICASTALKING_USERNAME, settings.AFRICASTALKING_API_KEY
        )
        self.sms = africastalking.SMS

    def send_sms(self, phone_number: str, message: str):
        response = self.sms.send(message, [phone_number])
        return response
