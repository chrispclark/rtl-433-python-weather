from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

# import python smtplib module
import smtplib

# this function will parse the email address first to get email user real name and address.
# then it will encode the user name use utf-8 to avoid encoding error.
# then it will call formataddr function to construct the email address again.

# get sender email, password, receiver email and smtp server ip address.
from_addr = 'chris.p.clark@gmail.com'
to_addr = 'chris.p.clark@gmail.com'
smtp_server = 'localhost'

# create MIMEText object
msg = MIMEText('hello world email from Python', 'plain', 'utf-8')
msg = MIMEText('<html><body><h1>Hello World</h1>' +
'<p>this is hello world from <a href="http://www.python.org">Python</a>...</p>' +
'</body></html>', 'html', 'utf-8')
# add from, to and subject to the MIMEText object.
msg['From'] = from_addr
msg['To'] = to_addr
msg['Subject'] = Header('This email sent from Python code', 'utf-8').encode()

server = smtplib.SMTP(smtp_server, 25)
server.set_debuglevel(1)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()