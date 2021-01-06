#!/usr/bin/env python
# -*- coding:utf-8 -*-


from setuptools import setup, find_packages

with open("README.md", "r", encoding='UTF-8') as fh:
    long_description = fh.read()

setup(
    name="eloger",
    version="0.0.1",
    keywords=("email", "log", '日志邮件'),
    description="带发邮件的loguru包装，支持全部loguru功能和邮件发送功能",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT Licence",
    url="https://github.com/425776024/eloger",
    author="Jiang.XinFa",
    author_email="425776024@qq.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=['loguru', 'pydantic']
)
