from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
import logging

logger = logging.getLogger(__name__)


def send_registration_otp(request, otp_number, username, email):
    try:
        send_mail(
            subject="Aviato Registration System - OTP Verification",
            message=(
                f"Hello,{username}\n\n"
                f"Thank you for signing up at Aviato Store!\n\n"
                f"Your One-Time Password (OTP) is: {otp_number}\n\n"
                f"⚠️ Do NOT share this code with anyone. "
                f"If you did not sign up, please ignore this email.\n\n"
                f"Best regards,\n"
                f"Aviato Team"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        return HttpResponse('Email sent successfully!')
    except Exception as e:
        logger.error(f'Error sending email: {e}')
        return HttpResponse(f'Error sending email: {e}')