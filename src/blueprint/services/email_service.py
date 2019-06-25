from google.appengine.api import mail, app_identity
import logging
from datetime import datetime


def send(recipients, subject, body):
    isHTML=True
    # print("recep: "+recipients)
    logging.debug(u'Sending mail {} to {}'.format(subject, unicode(recipients)).encode(u'utf-8'))

    message = mail.EmailMessage(
        sender=u'Admin VeggsProno <noreply@{}.appspotmail.com>'.format(app_identity.get_application_id()),
        subject=subject,
        to=recipients
    )

    if isHTML:
        message.html = body
    else:
        message.body = body

    message.check_initialized()
    message.send()