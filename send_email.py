#!/usr/bin/python3
import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
import base64
from secret import mail_host, mail_user, mail_pass, sender
class Email:
    def __init__(self):
        # 第三方 SMTP 服务
        self.mail_host = mail_host  # 设置服务器
        self.mail_user = mail_user  # 用户名
        self.mail_pass = mail_pass  # 口令
        self.sender = sender
    def send(self,sendtext_list, fujian_list,delete_fujian=True, email_from='发送端',email_to='接受端',email_subject='发送端实时信息',receivers = ['626237248@qq.com']):

        # 创建一个带附件的实例
        msgRoot = MIMEMultipart('related')
        msgRoot['From'] = Header(email_from, 'utf-8')
        msgRoot['To'] = Header(email_to, 'utf-8')
        subject = email_subject
        msgRoot['Subject'] = Header(subject, 'utf-8')

        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)
        # 邮件正文内容

        mail_msg = ''
        for sendtext in sendtext_list:
            mail_msg += '<p>%s</p>' % (str(sendtext))

        #html中加入图片
        for index, fujian_path in enumerate(fujian_list):
            if '/' in fujian_path:
                filename=fujian_path.split('/')[-1]
            elif '\\' in fujian_path:
                filename=fujian_path.split('\\')[-1]
            else:
                filename = fujian_path

            msgImage = MIMEText(open(fujian_path, 'rb').read(), 'plane', 'utf-8')
            # 定义图片 ID，在 HTML 文本中引用
            msgImage.add_header('Content-ID', '<image%s>'%(str(index)))
            msgImage["Content-Disposition"] = 'attachment; filename="' + filename + '"'
            msgRoot.attach(msgImage)
            mail_msg+='<img src="cid:image%s" alt="image1">'%(str(index))
        msgAlternative.attach(MIMEText(mail_msg, 'html', 'utf-8'))

        if delete_fujian:
            for fujian_path in fujian_list:
                os.remove(fujian_path)

        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(self.mail_host, 25)  # 25 为 SMTP 端口号
            smtpObj.login(self.mail_user, self.mail_pass)
            smtpObj.sendmail(self.sender, receivers, msgRoot.as_string())
            print("发送成功")
            return True
        except:
            print("Error: 发送失败")
            return False