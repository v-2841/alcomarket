from celery import shared_task, Task
from django.core.mail import send_mail


class BaseTaskWithRetry(Task):
    autoretry_for = (Exception, KeyError)
    retry_kwargs = {'max_retries': 5}
    retry_backoff = True
    retry_jitter = True


@shared_task(bind=True, base=BaseTaskWithRetry)
def async_send_mail(
    self,
    subject,
    message,
    from_email,
    recipient_list,
    html_message=None,
):
    return send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        html_message=html_message,
        fail_silently=False,
    )
