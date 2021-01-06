#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/4 下午4:09
# @File    : logers.py
from eloger import elogger

'''
{
        "sender_email": "xxx@163.com",
        "sender_email_passwd": "xxxx",
        "sender_email_mailserver": "smtp.163.com",
        "sender_email_mailserver_port": "25",
        "title": "来自log的信息",
        "body": "<br/><img src=\"cid:image\"><br>",
        "receive_emails": [
            "xx@qq.com"
        ]
}
'''

if __name__ == '__main__':
    elogger.mail_config.sender_email = "Your email"
    elogger.mail_config.sender_email_passwd = "Your email Authorization code"
    elogger.mail_config.sender_email_mailserver = "Your email server, like: smtp.163.com"
    elogger.mail_config.sender_email_mailserver_port = "Your email server's port , like : 25"
    elogger.mail_config.title = "Your email message title , like : this is a log message title"
    elogger.mail_config.body = "Your email message content template , like : <br/>#msg<br/> (#msg Will be replaced by log message)"
    elogger.mail_config.receive_emails = [
        "xxx@qq.com"
    ]
    elogger.add('a.log', email=True)
    elogger.error('error')
    elogger.debug('debug')
    elogger.info('info')
    elogger.success('success')
