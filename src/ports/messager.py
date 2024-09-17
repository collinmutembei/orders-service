from abc import ABC, abstractmethod


class SMSMessager(ABC):
    @abstractmethod
    def send_sms(self, phone_number: str, message: str) -> dict:
        """Send an SMS to the specified phone number"""
        pass
