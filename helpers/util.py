#here we will have utility functions for the tests
import time
import pyotp
from helpers.config import WEINFUSE_OTP_SECRET


def get_otp_code():
    """Generates OTP, enters it, and submits the form."""            
    # Generate a fresh OTP
    totp = pyotp.TOTP(WEINFUSE_OTP_SECRET.get_secret_value())
    current_otp = totp.now()
    
    # Check how much time left for this OTP
    remaining_seconds = 30 - (int(time.time()) % 30)
    print(f"Current OTP: {current_otp}, valid for {remaining_seconds} seconds")
