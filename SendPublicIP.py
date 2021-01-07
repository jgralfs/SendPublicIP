# this script checks the public ip address and safes it in a file named 'lastIP'
# if the public ip address is different from the one in the 'lastIP' file it
# will notify you by mail telling you the new public ip address.

# import required packages
import requests
import re
import smtplib
import os

# import credentials and config for your mail server from the 'MailConfig' file
from MailConfig import *

# setup where from to receive the public ip address
url = 'http://checkip.dyndns.org'

# open the url and get the content
request = requests.get(url).text

# extract only the ip from the request
ipFromRequest = re.findall("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", request)

# remove [''] from IP
publicIP = str(".".join(ipFromRequest))
print ("Your public IP address is", publicIP)

# defining the funtion to send the mail with the new public ip address
def sendMail(publicIP):
    # body of the mail
    bodyText = 'Your new public IP address is ' + publicIP
    message = '\r\n'.join(['To: %s' % recipent, 'From: %s' % sender, 
              'Subject: %s' % subject, '', bodyText])
    # you need to uncomment either the starttls or the ssl part depending
    # on what your mail server accepts
    
    # sending mail using starttls authentication
    # server = smtplib.SMTP(smtpServer)
    # server.starttls()
    # sending mail using ssl authentication    
    # server = smtplib.SMTP_SSL(smtpServer)
    server.login(username,password)
    server.sendmail(sender, recipent, message)
    server.quit()
    print ("Mail has been sent")

# check if the lastIP file exists and create it if not
if os.path.isfile('lastIP'):
    print ("The lastIP file exists ")
else:
    f = open('lastIP', 'w+')
    print ("The lastIP file was missing and is now created")

# open the lastIP file and extract the IP address
with open('lastIP') as lastIP:
    lastIP = lastIP.read()

# check if the public IP address has changed
if lastIP == publicIP:
    print ("Public IP has not changed.")
else:
    print ("You have a new public IP address")
    with open('lastIP', 'w') as lastIP:
        lastIP.write(publicIP)
    print ("New public IP has been saved within the lastIP file")
    sendMail(publicIP)
