import cgi
import json
import smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from falcon import HTTP_200

from constants import DEFAULT_SENDER, DEFAULT_SENDER_PASSWORD
from exceptions.exception_handler import ExceptionHandler

context = ssl.create_default_context()

class Mail:
    @ExceptionHandler
    def on_post(self, request, response):
        env = request.env
        env.setdefault('QUERY_STRING', '')
        
        form = cgi.FieldStorage(fp=request.stream, environ=env)
        file_item = form['file']
        sender = form.getvalue('sender_email', DEFAULT_SENDER)
        sender_user = form.getvalue('sender_username', '')
        sender_password = form.getvalue('sender_password', DEFAULT_SENDER_PASSWORD)
        receiver_mail = form.getvalue('receiver', '')
        receiver_user = form.getvalue('receiver_username', '')

        message = MIMEMultipart()
        message["From"] = "{} <{}>".format(sender_user, sender)
        message["To"] = "{} <{}>".format(receiver_user, receiver_mail)
        message["Subject"] = form.getvalue('subject', '')
        message["Bcc"] = form.getvalue('receiver_bcc', '')
        body = form.getvalue('body', '')
        message.attach(MIMEText(body, "plain"))

        if file_item.file:
            media = MIMEBase("application", "octet-stream")
            media.set_payload(file_item.file.read())
            encoders.encode_base64(media)
            message.attach(media)

        with smtplib.SMTP("smtp.gmail.com", port=587) as server:
            server.starttls()
            server.login(sender, sender_password)
            server.sendmail(sender, receiver_mail, message.as_string())

        response.body = json.dumps({
            'status': 'Success',
            'message': 'Successfully sent the mail'
        })
        response.status = HTTP_200
