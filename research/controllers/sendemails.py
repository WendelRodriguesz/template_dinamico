import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from config import EMAIL, EMAIL_PASSWORD
from services.structured_data import Output
from services.config_logging import log



class Emails:
    """
        Class for sending email via gmail API.
    """
    def __init__(self, subject, text_body, to_email):
        self.subject = subject
        self.email_origin = EMAIL
        self.password = EMAIL_PASSWORD
        self.text_body = text_body
        self.to_email = to_email
        self.logger = log(__name__)

    def send_anex(self, local, filename):
        """
            Function to send files by email.
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

            self.logger.info('Email sent successfully! to: ' + self.to_email)
            return Output().return_funtion(200, None)

        except Exception as error:
            self.logger.error('Error sending email!! ' + error)
            return Output().return_funtion(400, error)