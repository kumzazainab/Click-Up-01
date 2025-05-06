from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from todolist.models import Comment
from django.conf import settings

@receiver(m2m_changed, sender=Comment.to_users.through)
def send_email_on_comment(sender, instance, action, **kwargs):
    if action == "post_add" and instance.is_email:
        subject = instance.subject or "New Comment"
        message = instance.content
        from_email = settings.DEFAULT_FROM_EMAIL
        recipients = instance.to_users.values_list('email', flat=True)

        for email in recipients:
            send_mail(subject, message, from_email, [email])
