import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

# 直接在代码中定义电子邮件地址和密码
from_email = "itsupport@10over10.com.tw"
password = "P@ssword123"

def send_email(to_email, file_path, summary):
    subject = "音訊轉文字結果"
    body = f"以下是您的音訊轉文字結果摘要：\n\n{summary}" if summary else "生成摘要时出错，结果请见附件。"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    attachment = MIMEBase('application', 'octet-stream')
    with open(file_path, "rb") as attachment_file:
        attachment.set_payload(attachment_file.read())

    encoders.encode_base64(attachment)
    attachment.add_header(
        "Content-Disposition",
        f"attachment; filename= {os.path.basename(file_path)}",
    )
    msg.attach(attachment)

    server = smtplib.SMTP('smtp.office365.com', 587)
    server.starttls()
    server.login(from_email, password)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()
