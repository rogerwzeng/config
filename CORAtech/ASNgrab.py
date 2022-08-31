# Get email attachments off of ASN emails from Patagonia
import datetime
import os
import imaplib
import email.header


root_dir = '/mnt/d/CORAtech/'
attach = 'attachments'
attach_dir = root_dir + attach
detach_dir = '.'

# in case save-to dir is not there yet
if attach not in os.listdir(root_dir):
    os.mkdir(attach_dir)

imap_host = 'imap.qiye.aliyun.com'
pop3_host = 'pop3.qiye.aliyun.com'
user = 'impdocs@cora.org.cn'
passwd = 'Cora123456'

# get emails since yesterday
date = (datetime.date.today() - datetime.timedelta(1)).strftime("%d-%b-%Y")

# Your IMAP Settings
host = imap_host
password = passwd

# Connect to the server
print('Connecting to ' + host)
mailBox = imaplib.IMAP4_SSL(host)

# Login to our account
mailBox.login(user, password)

boxList = mailBox.list()

mailBox.select()  # default to Inbox

# WRONG query
by_all = 'ALL'  # no filter
by_subject = 'SUBJECT "ASN info"'
by_from = 'FROM AzureIntegrations@patagonia.com'
searchQuery = by_all  # choose which filter to use
result, ids = mailBox.search(None, searchQuery)
# result, ids = mailBox.search(by_from)
print(f"Found {len(ids[0])-2} emails")

# iterate through each email to get attachments
for latest_email_uid in ids[0].split():

    # fetch the email body (RFC822) for the given ID
    result, email_data = mailBox.uid('fetch', latest_email_uid, '(RFC822)')

    raw_email = email_data[0][1]

    # converts byte literal to string removing b''
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)

    # See if it is the ASN email
    if 'ASN info' not in email_message['Subject']:
        continue

    # downloading attachments
    for part in email_message.walk():
        # this part comes from the snipped I don't understand yet...
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()
        print(f"Attachement found: {fileName}")

        if bool(fileName):
            filePath = os.path.join(attach_dir, fileName)
            with open(filePath, 'wb') as save_att:
                print(f"Saving attachment: {filePath}")
                save_att.write(part.get_payload(decode=True))

mailBox.close()
mailBox.logout()
