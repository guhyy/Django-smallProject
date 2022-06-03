import smtplib
import ssl

class email:
    def __init__(self,EMAIL_ADDRESS,EMAIL_PASSWORD,receiver,subject,body):
        self.EMAIL_ADDRESS = EMAIL_ADDRESS
        self.EMAIL_PASSWORD = EMAIL_PASSWORD
        self.receiver = receiver
        self.subject = subject
        self.body = body
    def sendemail(self):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.126.com',465,context=context) as smtp:
            smtp.login(self.EMAIL_ADDRESS,self.EMAIL_PASSWORD)
            msg = f"Subject:{self.subject}\n\n{self.body}"
            
            smtp.sendmail(self.EMAIL_ADDRESS,self.receiver,msg)



