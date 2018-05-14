import smtplib
import subprocess
import socket
import netifaces as ni

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

SMTP = "smtp.live.com" ##SMTP Server
PORT = 587 #Port may differ from provider to provider

FROM = "[FROM E-MAIL]"
TO = "[TO E-MAIL"
PW = "[PASSWORT]"

print("connecting Server..");
server = smtplib.SMTP(SMTP,PORT)
print("connected")
server.ehlo()
server.starttls()
print("tls started")
server.ehlo()
server.login(FROM,PW)
print("logged in")

##set up message

msg = MIMEMultipart()
msg['FROM'] = FROM
msg['TO'] = TO
msg['Subject'] = "IP-Adress of my fucking pi"

ni.ifaddresses('wlan0')
ip =  ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
body = "IP Adresse "  + ip
msg.attach(MIMEText(body,'plain'))
text = msg.as_string()
server.sendmail(FROM,TO,text)
print("mail sent")
server.quit()
