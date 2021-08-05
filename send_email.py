#!/usr/bin/python3
import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from secret import mail_host, mail_user, mail_pass, sender
class Email:
    def __init__(self):
        # 第三方 SMTP 服务
        self.mail_host = mail_host  # 设置服务器
        self.mail_user = mail_user  # 用户名
        self.mail_pass = mail_pass  # 口令
        self.sender = sender
    def send(self,sendtext, fujian_list,delete_fujian=True, email_from='发送端',email_to='接受端',email_subject='发送端实时信息',receivers = ['626237248@qq.com']):

        # 创建一个带附件的实例
        message = MIMEMultipart()
        message['From'] = Header(email_from, 'utf-8')
        message['To'] = Header(email_to, 'utf-8')
        subject = email_subject
        message['Subject'] = Header(subject, 'utf-8')
        receivers=receivers
        # 邮件正文内容
        message.attach(MIMEText(sendtext, 'plain', 'utf-8'))
        for fujian_path in fujian_list:
            # 构造附件1，传送当前目录下的 test.txt 文件
            att1 = MIMEText(open(fujian_path, 'rb').read(), 'base64', 'utf-8')
            att1["Content-Type"] = 'application/octet-stream'
            if '/' in fujian_path:
                filename=fujian_path.split('/')[-1]
            elif '\\' in fujian_path:
                filename=fujian_path.split('\\')[-1]
            else:
                filename = fujian_path
            # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
            att1["Content-Disposition"] = 'attachment; filename="'+filename+'"'
            message.attach(att1)
            if delete_fujian:
                os.remove(fujian_path)

        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(self.mail_host, 25)  # 25 为 SMTP 端口号
            smtpObj.login(self.mail_user, self.mail_pass)
            smtpObj.sendmail(self.sender, receivers, message.as_string())
            print("发送成功")
            return True
        except smtplib.SMTPException:
            print("Error: 发送失败")
            return False