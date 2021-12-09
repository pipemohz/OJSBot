import smtplib
import datetime as dt
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from os.path import basename
import os


def send_mail():
    
    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = 'felipe.moreno@metabiblioteca.com'
    message['To'] = 'pipemoreno9405@gmail.com'
    message['Subject'] = 'A test mail sent of OJSBot. It has an attachment.'
    # The subject line
    # The body and the attachments for the mail
    mail_content = f'Mensaje de OJSBot:\nReporte of auditoria completo.\n Fecha: {dt.datetime.now().date()}'
    message.attach(MIMEText(mail_content, 'plain'))
    attach_file_name = 'report.csv'
    with open(attach_file_name, mode='rb') as attach_file:
        part = MIMEApplication(attach_file.read(), Name=basename(attach_file_name)
                            )

    # After the file is closed
    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(
        attach_file_name)
    message.attach(part)

    with smtplib.SMTP(host='smtp.gmail.com', port=587) as conn:
        conn.starttls()
        conn.login(user=os.getenv('email_account'),
                password=os.getenv('email_password'))
        conn.sendmail(from_addr='felipe.moreno@metabiblioteca.com',
                    to_addrs=['pipemoreno9405@gmail.com', 'angievargas@metabiblioteca.com'], msg=message.as_string())
