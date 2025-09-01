from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


def send_email(subject: str, email_to: list[str], html_template, context,):
    msg = EmailMultiAlternatives(#we can pass a couple of auguments to the email
        subject=subject, from_email="nonreplay@talentbase.com", to=email_to,
    )
    html_template = get_template(html_template)
    html_alternative = html_template.render(context)
    msg.attach_alternative(html_alternative, "text/html")
    msg.send(fail_silently=False)
    
    
# from typing import Any
# from django.conf import settings
# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import get_template


# def send_email(
#     subject: str,
#     email_to: list[str],
#     template_name: str,
#     context: dict[str, Any],
#     *,
#     from_email: str | None = None,
#     fail_silently: bool = False,
#     reply_to: list[str] | None = None,
# ) -> None:
#     """
#     Send an HTML email using a Django template.
#     Renders `template_name` with `context` and attaches it as text/html.
#     """
#     # Use DEFAULT_FROM_EMAIL if not provided
#     sender = from_email or getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@example.com")

#     # Optional: render a plaintext fallback if you keep a .txt twin
#     # (e.g., 'emails/welcome.html' -> 'emails/welcome.txt')
#     txt_body = None
#     if template_name.endswith(".html"):
#         txt_candidate = template_name[:-5] + ".txt"
#         try:
#             txt_body = get_template(txt_candidate).render(context)
#         except Exception:
#             txt_body = None

#     # Render HTML body
#     html_template = get_template(template_name)
#     html_body = html_template.render(context)

#     # Build message
#     msg = EmailMultiAlternatives(
#         subject=subject,
#         body=txt_body or "",  # Plaintext part (empty if none)
#         from_email=sender,
#         to=email_to,
#         reply_to=reply_to or None,
#     )
#     msg.attach_alternative(html_body, "text/html")
#     msg.send(fail_silently=fail_silently)
