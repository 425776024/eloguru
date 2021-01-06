#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/5 5:28 下午
# @File    : email.py
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from .mail_config import MailConfig, mail_config


class __MailSend:
    config: MailConfig = mail_config
    server = None
    msg_tag = '#msg'

    @classmethod
    def init(cls):
        cls.server = smtplib.SMTP(mail_config.sender_email_mailserver, mail_config.sender_email_mailserver_port)
        cls.server.login(cls.config.sender_email, mail_config.sender_email_passwd)

    @classmethod
    def send_one(cls, receive, say: str):
        try:
            msg = MIMEMultipart('related')
            msg['From'] = formataddr(["发件人：", cls.config.sender_email])  # 发件人邮箱昵称、发件人邮箱账号
            msg['To'] = formataddr(["收件人：", receive])  # 收件人邮箱昵称、收件人邮箱账号
            msg['Subject'] = cls.config.title
            if cls.msg_tag in cls.config.body:
                say = cls.config.body.replace(cls.msg_tag, say)
            text = MIMEText(say, 'html', 'utf-8')
            msg.attach(text)
            return msg
        except Exception as e:
            cls.init()

    @classmethod
    def send(cls, say: str):
        if cls.server is None:
            cls.init()
        for friend in cls.config.receive_emails:
            try:
                msg = cls.send_one(friend, say)
                cls.server.sendmail(cls.config.sender_email, friend, msg.as_string())
            except Exception as e:
                cls.init()
                try:
                    msg = cls.send_one(friend, say)
                    cls.server.sendmail(cls.config.sender_email, friend, msg.as_string())
                except Exception as e2:
                    print(e2)
