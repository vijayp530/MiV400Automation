import smtplib
import os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

class EmailHandler():
    
    @staticmethod
    def send_mail(send_from,sender_password, send_to, subject, text, files=[], server="relay.shoretel.com"):
        assert type(send_to) == list
        assert type(files) == list
    
        msg = MIMEMultipart()
        msg['From'] = send_from
        msg['To'] = COMMASPACE.join(send_to)
        # msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject
    
        msg.attach(MIMEText(text))
    
        for f in files:
            part = MIMEBase('application', "octet-stream")
            part.set_payload( open(f, "rb").read() )
            Encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
            msg.attach(part)
        
        try:
            smtp = smtplib.SMTP(server, 587)
            smtp.starttls()
            smtp.login(send_from, sender_password)
            #msg=str(msg)
            smtp.sendmail(send_from, send_to,msg.as_string())
            #smtp.close()
            smtp.quit()
        except smtplib.SMTPException:
            print("Error: unable to send email")
            raise
        except Exception as error:
            print("Error: unable to send email :  {err}".format(err=error))

        print("Success: Email sent ")

        
#test driver
#EmailHandler().send_mail("nextgenarc@shoretel.com", ['mkr@shoretel.com'], "NextGenArc Execution Report", "Automated mail, please find report attached", ['Report.xlsx'],"outlook.shoretel.com")
