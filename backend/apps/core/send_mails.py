
import threading
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.sites.models import Site
from django.conf import settings


def get_host():
    return Site.objects.get_current().domain


class EmailThread(threading.Thread):
    def __init__(self, subject, html_template, recipient_list, params: dict or None = None,
                 attachments: list or None = None):
        self.subject: str = subject
        self.recipient_list: list[str] = recipient_list
        self.html_template: str = 'mails/{template}'.format(template=html_template)
        self.params: dict = params
        self.attachments: list = attachments
        threading.Thread.__init__(self)

    def run(self):
        html_content = render_to_string(self.html_template, self.params)
        subject = self.subject
        from_email = '%s <%s>' % (settings.SITE_NAME, settings.DEFAULT_FROM_EMAIL)
        to = self.recipient_list
        text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.
        # create the email, and attach the HTML version as well.
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        if self.attachments:
            for file in self.attachments:
                if file:
                    msg.attach_file(file.path)
        msg.send()


def send_html_mail(subject: str, html_template: str, recipient_list: list[str], params: dict or None = None,
                   attachments: list or None = None):
    EmailThread(subject, html_template, recipient_list, params, attachments).start()
