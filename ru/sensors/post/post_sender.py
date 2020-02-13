import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class SendEmail:
    def __init__(self, 
                 title,
                 content,
                 addr_from,
                 addr_to,
                 passwd):
        
        self.title = title
        self.content = content
        self.addr_from = addr_from
        self.addr_to = addr_to
        self.passwd = passwd

    def send_email(self):
        msg = MIMEMultipart()
        msg['From'] = self.addr_from
        msg['To'] = self.addr_to
        msg['Subject'] = self.title
        msg.attach(MIMEText(self.content, 'html', 'utf-8'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.set_debuglevel(True)
        server.starttls()
        server.login(self.addr_from, self.passwd)
        server.send_message(msg)
        server.quit()