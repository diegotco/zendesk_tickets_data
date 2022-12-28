import yagmail
import os


# Load the Gmail account password from the .env file.
with open(".env") as f:
    for line in f:
        key, value = line.strip().split("=")
        os.environ[key] = value

# Access the Gmail account user.
gmail_user = os.getenv("GMAIL_USER")

# Access the Gmail account password.
gmail_password = os.getenv("GMAIL_PASS")

# Creating a connection to your Gmail account.
yag = yagmail.SMTP(gmail_user, gmail_password) # Don't use your Gmail password, instead, activate the 2FA for your Google account and create a password for apps. See more here https://support.google.com/accounts/answer/185833

# Introduce the next values as strings.
destination_email = "" # Indicate the email where you want to send the mail. Can be anyone, for example, an Slack channel email.
subject = "" # You can set any subject.
body = '<h1>Last Wordcloud image</h1>' # Yes! It will be recognized as HTML.
imagen = yagmail.inline("wordcloud.png") # Use inline for include the image in the body. Everything else will be attached. Also, make sure the image is in the same folder as this Python file.
contents=[body, imagen]

yag.send(
    to=destination_email,
    subject=subject,
    contents=contents
)
