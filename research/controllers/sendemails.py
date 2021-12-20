import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from research.config import EMAIL, EMAIL_PASSWORD
from research.services.structured_data import Output


class Emails:
    """
        Classe para enviar e-mail pela API do gmail.
    """
    def __init__(self, subject, text_body, to_email):
        self.subject = subject
        self.email_origin = EMAIL
        self.password = EMAIL_PASSWORD
        self.text_body = text_body
        self.to_email = to_email

    def send_anex(self, local, filename):
        """
            Função para enviar arquivos por e-mail.
        """
        try:
            msg = MIMEMultipart()

            msg['Subject'] = self.subject
            msg['From'] = self.email_origin
            msg['To'] = self.to_email
            password = self.password

            msg.attach(MIMEText(self.text_body, 'plain'))

            attachment = open(local+filename, 'rb')

            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

            msg.attach(part)

            attachment.close()

            server = smtplib.SMTP('smtp.gmail.com: 587')
            server.starttls()
            server.login(self.email_origin, password)
            text = msg.as_string()
            server.sendmail(self.email_origin, self.to_email, text)
            server.quit()

            print('Email enviado com sucesso! para:', self.to_email)
            return Output().return_funtion(200, None)

        except Exception as error:
            print('Error ao enviar e-mail!!', error)
            return Output().return_funtion(400, error)