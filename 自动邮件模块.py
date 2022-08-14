import smtplib
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header

def content(mail,sender_qq,mail_title):
    #邮件内容
    message = mail
    msg_ = MIMEText(message, "html", 'utf-8')
    msg_["Subject"] = Header(mail_title,'utf-8')
    msg_["From"] = sender_qq
    msg_["To"] = Header("内测账号V1.0","utf-8")
    return msg_

def sendbyqq(content,account,host_server,sender_qq,pwd):
    msg = content
    try:
        smtp = SMTP_SSL(host_server) # ssl登录连接到邮件服务器
        smtp.set_debuglevel(1) # 0是关闭，1是开启debug
        smtp.ehlo(host_server) # 跟服务器打招呼，告诉它我们准备连接，最好加上这行代码
        smtp.login(sender_qq,pwd)
        smtp.sendmail(sender_qq,account,msg.as_string())
        smtp.quit()
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("无法发送邮件")