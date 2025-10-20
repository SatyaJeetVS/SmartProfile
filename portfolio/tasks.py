from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger('portfolio.tasks')


@shared_task(bind=True)
def send_contact_email(self, name, email, message):
    """Send contact form email asynchronously."""
    subject = f'New Contact Form Submission from {name}'
    body = f'Name: {name}\nEmail: {email}\nMessage: {message}'

    logger.info('send_contact_email task started for %s <%s>', name, email)

    

    # Use profile email if available, otherwise fall back to DEFAULT_FROM_EMAIL
    recipient_list = [settings.DEFAULT_FROM_EMAIL]

    if not recipient_list:
        logger.warning('No recipient configured for contact email; aborting')
        return {'status': 'no_recipient'}

    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            fail_silently=False,
        )
        logger.info('Contact email sent to %s', recipient_list)
    except Exception:
        logger.exception('Failed to send contact email')
        raise

    return {'status': 'sent', 'recipients': recipient_list}
