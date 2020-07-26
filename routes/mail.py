import cgi
import json
import requests
import smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from falcon import HTTP_200

from constants import DEFAULT_SENDER, DEFAULT_SENDER_PASSWORD, DEFAULT_FILE_NAME
from exceptions.exception_handler import ExceptionHandler
from processes.worker_pool import DEFAULT_WORKER_THREAD

context = ssl.create_default_context()

def send_mail(sender, sender_password, receiver_mail, message):
    try:
        server = smtplib.SMTP("smtp.gmail.com", port=587)
        server.starttls()
        server.login(sender, sender_password)
        server.sendmail(sender, receiver_mail, message)
        server.close()
    except Exception as exc:
        print(exc)

class Mail:
    @ExceptionHandler
    def on_post(self, request, response):
        env = request.env
        env.setdefault('QUERY_STRING', '')
        
        form = cgi.FieldStorage(fp=request.stream, environ=env)
        file_item = form['file'] if 'file' in form else None
        sender = form.getvalue('sender_email', DEFAULT_SENDER)
        receiver_mail = form.getvalue('receiver')
        sender_user = form.getvalue('sender_username', '')
        sender_password = form.getvalue('sender_password', DEFAULT_SENDER_PASSWORD)
        receiver_user = form.getvalue('receiver_username', '')
        attachment = form.getvalue('url')
        file_name = form.getvalue('file_name')

        assert receiver_mail, 'receiver is mandatory argument'

        file_data = file_item.file.read() if file_item and file_item.file else None
        file_name = file_item.filename if file_item and file_item.filename else DEFAULT_FILE_NAME

        if not file_data and attachment:
            file_data = requests.get(attachment).content

        message = MIMEMultipart()
        message["From"] = "{} <{}>".format(sender_user, sender)
        message["To"] = "{} <{}>".format(receiver_user, receiver_mail)
        message["Subject"] = form.getvalue('subject', '')
        message["Bcc"] = form.getvalue('receiver_bcc', '')
        body = form.getvalue('body', '')
        message.attach(MIMEText(body, "plain"))

        if file_data:
            media = MIMEBase("application", "octet-stream")
            media.set_payload(file_data)
            media.add_header(
                "Content-Disposition",
                f"attachment; filename={file_name or file_item.filename}",
            )
            encoders.encode_base64(media)
            message.attach(media)

        DEFAULT_WORKER_THREAD.process_tasks(
            send_mail,
            sender,
            sender_password,
            receiver_mail,
            message.as_string()
        )

        response.body = json.dumps({
            'status': 'Success',
            'message': 'Successfully triggered the mail'
        })
        response.status = HTTP_200
