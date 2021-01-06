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
        "body": "<br/> #msg <br>",
        "receive_emails": [
            "xx@qq.com"
        ]
}
'''

if __name__ == '__main__':
    elogger.mail_config.sender_email = "xx@163.com"
    elogger.mail_config.sender_email_passwd = "xx"
    elogger.mail_config.sender_email_mailserver = "smtp.163.com"
    elogger.mail_config.sender_email_mailserver_port = "25"
    elogger.mail_config.title = "a log"
    elogger.mail_config.body = "LOG : <br/>#msg<br/>"
    elogger.mail_config.receive_emails = [
        "xx@qq.com",
    ]

    elogger.add('a.log')
    elogger.error('error', email=True)
    elogger.debug('debug')
    elogger.info('info')
    elogger.success('success', email=True)
