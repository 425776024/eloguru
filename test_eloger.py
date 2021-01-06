#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/4 下午4:09
# @File    : logers.py
from eloguru import eloguru

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
    eloguru.mail_config.sender_email = "xx@163.com"
    eloguru.mail_config.sender_email_passwd = "xx"
    eloguru.mail_config.sender_email_mailserver = "smtp.163.com"
    eloguru.mail_config.sender_email_mailserver_port = "25"
    eloguru.mail_config.title = "a log"
    eloguru.mail_config.body = "LOG : <br/>#msg<br/>"
    eloguru.mail_config.receive_emails = [
        "xx@qq.com",
    ]

    eloguru.add('a.log')
    eloguru.error('error', email=True)
    eloguru.debug('debug')
    eloguru.info('info')
    eloguru.success('success', email=True)
