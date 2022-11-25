import smtplib, ssl

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "mallie.dagmawi@gmail.com"  # Enter your address
receiver_email = "abebeTurku@gmail.com"  # Enter receiver address
password = "lyhy umpx mjjr ffdf"
message = """\
Subject: Hi there
Today Monday14th of Novemeber looks grim and cold. But glad to send this message with automated email.
This message is sent from Python."""

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)