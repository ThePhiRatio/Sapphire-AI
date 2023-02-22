import email, smtplib, ssl
from providers import PROVIDERS
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import imaplib
from email.header import decode_header
import html2text
import os
from os.path import basename


#Guide from: https://www.alfredosequeida.com/blog/how-to-send-text-messages-for-free-using-python-use-python-to-send-text-messages-via-email/
def send_mms_via_email(
    number: str,
    message: str,
    file_path: str,
    mime_maintype: str,
    mime_subtype: str,
    provider: str,
    sender_credentials: tuple = ("sapphire.ai.server@gmail.com", "xfguuqekyiwijesw"),
    subject: str = "Sapphire AI Response",
    smtp_server: str = "smtp.gmail.com",
    smtp_port: int = 465,
):

    sender_email, email_password = sender_credentials
    if "." in provider:
        receiver_email = f'{number}@{provider}'
    else:
        receiver_email = f'{number}@{PROVIDERS.get(provider).get("sms")}'

    email_message=MIMEMultipart()
    email_message["Subject"] = subject
    email_message["From"] = sender_email
    email_message["To"] = receiver_email

    email_message.attach(MIMEText(message, "plain"))

    with open(file_path, "rb") as attachment:
        part = MIMEBase(mime_maintype, mime_subtype)
        part.set_payload(attachment.read())

        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={basename(file_path)}",
        )

        email_message.attach(part)

    text = email_message.as_string()

    with smtplib.SMTP_SSL(
        smtp_server, smtp_port, context=ssl.create_default_context()
    ) as email:
        email.login(sender_email, email_password)
        email.sendmail(sender_email, receiver_email, text)

def send_sms_via_email(
    number: str,
    message: str,
    provider: str,
    sender_credentials: tuple = ("sapphire.ai.server@gmail.com", "xfguuqekyiwijesw"),
    subject: str = "Sapphire AI Response",
    smtp_server: str = "smtp.gmail.com",
    smtp_port: int = 465,
):
    sender_email, email_password = sender_credentials
    if "." in provider:
        receiver_email = f'{number}@{provider}'
    else:
        receiver_email = f'{number}@{PROVIDERS.get(provider).get("sms")}'

    email_message = f"Subject:{subject}\nTo:{receiver_email}\n{message}"

    with smtplib.SMTP_SSL(
        smtp_server, smtp_port, context=ssl.create_default_context()
    ) as email_text:
        email_text.login(sender_email, email_password)
        email_text.sendmail(sender_email, receiver_email, email_message)



def has_email():
    # create an IMAP4 class with SSL
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    # authenticate
    imap.login("sapphire.ai.server@gmail.com", "xfguuqekyiwijesw")

    status, messages = imap.select("Inbox")
    # print(status)
    # print(messages)
    # number of top emails to fetch
    # total number of emails
    messages = int(messages[0])
    # print(messages)
    imap.close()
    imap.logout()
    if messages > 0:
        return True
    else:
        return False



#Guide Followed From https://www.thepythoncode.com/article/reading-emails-in-python
def read_email(Delete_Mails = True):
    # create an IMAP4 class with SSL
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    # authenticate
    imap.login("sapphire.ai.server@gmail.com", "xfguuqekyiwijesw")

    status, messages = imap.select("Inbox")
    # number of top emails to fetch
    # total number of emails
    messages = int(messages[0])
    message_results = [[] for _ in range(messages)]

    for i in range(1,messages+1):
        # fetch the email message by ID
        res, msg = imap.fetch(str(i), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                # parse a bytes email into a message object
                msg = email.message_from_bytes(response[1])
                # decode the email subject
                # subject, encoding = decode_header(msg["Subject"])[0]
                # if isinstance(subject, bytes):
                #     # if it's a bytes, decode to str
                #     subject = subject.decode(encoding)
                # decode email sender
                From, encoding = decode_header(msg.get("From"))[0]
                if isinstance(From, bytes):
                    From = From.decode(encoding)
                # if the email message is multipart
                if msg.is_multipart():
                    # iterate over email parts
                    for part in msg.walk():
                        # extract content type of email
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                            # get the email body
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            # print text/plain emails and skip attachments
                            pass
                        # elif "attachment" in content_disposition:
                        try:
                            # download attachment
                            filename = part.get_filename()
                            if filename:
                                folder_name = 'temp'
                                if not os.path.isdir(folder_name):
                                    # make a folder for this email (named after the subject)
                                    os.mkdir(folder_name)
                                filepath = os.path.join(folder_name, filename)
                                if filepath is not None:
                                    master_filepath = filepath
                                # download attachment and save it
                                open(filepath, "wb").write(part.get_payload(decode=True))
                                # print(part.get_payload(decode=True))
                                # body = part.get_payload(decode=True)
                        except:
                            pass
                else:
                    # extract content type of email
                    content_type = msg.get_content_type()
                    # get the email body
                    body = msg.get_payload(decode=True).decode()
                    if content_type == "text/plain":
                        # print only text email parts
                        pass
                if content_type == "text/html":
                    # Convert html to text
                    h = html2text.HTML2Text()
                    h.ignore_links = True
                    results = h.handle(str(body))
                    body = results.strip()

        if "+" in From:
            From = From[2:]
        From = From.split('@')
        numb = From[0]
        provid = From[1]
        # message_results[i-1] = [body.strip(), numb, provid]
        if(len(os.listdir('C:/Users/nicho/Desktop/Sapphire_Smart_Home_Project/temp'))==0):
            message_results[i - 1] = [body.strip("/").replace('\\',' '), numb, provid]
        else:
            if '.txt' in master_filepath:
                print(str(master_filepath))
                f = open(master_filepath, 'r')
                body = f.read().strip("/").replace('\\',' ')
                f.close()
                os.remove(master_filepath)
                message_results[i - 1] = [body.strip("/").replace('\\',' '), numb, provid]
            else:
                for file in os.listdir('C:/Users/nicho/Desktop/Sapphire_Smart_Home_Project/temp'):
                    if file.endswith(".txt"):
                        path = (os.path.join('C:/Users/nicho/Desktop/Sapphire_Smart_Home_Project/temp/', file))
                f = open(path, 'r')
                body = f.read().strip("/").replace('\\',' ')
                f.close()
                for file in os.listdir('C:/Users/nicho/Desktop/Sapphire_Smart_Home_Project/temp'):
                    os.remove(os.path.join('C:/Users/nicho/Desktop/Sapphire_Smart_Home_Project/temp/', file))
                message_results[i - 1] = [body.strip("/").replace('\\',' '), numb, provid]
        if(Delete_Mails):
            imap.store(str(i), "+FLAGS", "\\Deleted")

    #Close email readers
    imap.close()
    imap.logout()
    #return responces
    return(message_results)


