#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/6 11:09 上午
# @File    : mail_config.py
from typing import List
from pydantic import BaseModel, Field


class MailConfig(BaseModel):
    sender_email: str = Field(default="jxf@163.com", )
    sender_email_passwd: str = Field(default="CMOJH.......", )
    sender_email_mailserver: str = Field(default="smtp.163.com", )
    sender_email_mailserver_port: str = Field(default="25", )
    title: str = Field(default="来自log的信息", )
    body: str = Field(default="<br/>#msg<br/>", )
    receive_emails: List[str] = Field(default=["4xxx24@qq.com"], )


mail_config = MailConfig()
