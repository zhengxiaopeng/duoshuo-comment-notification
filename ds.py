#! /usr/bin/env python
# -*- coding: utf-8 -*-

from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
# http://requests-docs-cn.readthedocs.org/zh_CN/latest/user/quickstart.html
import requests
import smtplib
import time
import ConfigParser
import os, sys

debug = True

def log(msg):
    if debug:
        print msg

def monitor():
    # 加载配置文件信息
    log(u'\n>>>>>>>>>> 脚本开始运行 <<<<<<<<<<\n')
    config = ConfigParser.ConfigParser()
    dirname, filename = os.path.split(os.path.abspath(sys.argv[0])) # 获取绝对目录
    config.read(dirname + '/ds.config') # 当前目录下的ds.config

    # 初始化配置信息
    duoshuo_account = {}
    email_info = {}
    period_time = {}
    items2dict(duoshuo_account, config.items('duoshuo_account'))
    items2dict(email_info, config.items('email_info'))
    items2dict(period_time, config.items('period_time'))

    name = duoshuo_account.get('name')
    account_id = duoshuo_account.get('id')
    period = int(period_time.get('period'))
    secret = duoshuo_account.get('secret')

    # 多说后台获取 log 数据的接口
    duoshuo_log_url = 'http://api.duoshuo.com/log/list.json?' \
          + 'short_name=' + name \
          + '&secret=' + secret \
          + '&limit=5000'

    # 第一次获取账户后台的初始信息
    current_count, meta = get_duoshuo_log(duoshuo_log_url)
    last_count = current_count
    log(u'账号初始加载数据条数：' + str(last_count))

    while True: # 轮询检查
        log(u'\n----->> get_duoshuo_log')
        try:  # 防止get_duoshuo_log和send_email挂掉
            current_count, meta = get_duoshuo_log(duoshuo_log_url)
            # send_email(email_info, name, current_count, (current_count - last_count), meta)
            log(u'当前数据条数：' + str(current_count))
            	#print u'meta --->  ' + str(meta)
            if (len(meta)) > 0 and (current_count > last_count) and (account_id != meta.get('author_id')):
                send_email(email_info, name, current_count, (current_count - last_count), meta)
                last_count = current_count

        except Exception, e:
            log(u'Error :    ', str(e))
        
        time.sleep(period)


# 把option的items映射到dict中
def items2dict(options_dict, items_list):
    for item in items_list:
        options_dict[item[0]] = item[1]


# 获取多说账户的后台信息log
def get_duoshuo_log(url):
    # print url
    r = requests.get(url)
    resp = r.json()

    if (resp['code'] == 0):  # code为0时才是正常的log的json信息
        length = len(resp['response'])
        meta = resp['response'][length - 1]['meta']
        action = resp['response'][length - 1]['action']
        if (action == 'create'):  # action为create时才是新增评论，去除其它如delete等操作的影响
            return length, meta
        else:
            return length, {}

    return 0, {}


# 发送邮件
def send_email(email_info, name, current_count, count, meta):
    log(u'----->> send email')
    last_meta_message = u'最新评论信息：' \
                        + u'\n用户地址：' + unicode(meta.get('ip')) \
                        + u'\n用户昵称：' + unicode(meta.get('author_name')) \
                        + u'\n用户邮箱：' + unicode(meta.get('author_email')) \
                        + u'\n用户网站：' + unicode(meta.get('author_url')) \
                        + u'\n评论文章：' + unicode(meta.get('thread_key')) \
                        + u'\n评论时间：' + unicode(meta.get('created_at')) \
                        + u'\n评论内容：' + unicode(meta.get('message')) \
                        + u'\n审核状态：' + unicode(meta.get('status'))

    duoshuo_admin_url = 'http://' + name + '.duoshuo.com/admin/'
    text = u'后台记录变更数：' + str(count) + u'\n多说后台：' + duoshuo_admin_url + u'\n\n' + last_meta_message;
    log(text)
    msg = MIMEText(text, 'plain', 'utf-8')
    msg['Subject'] = u'多说评论通知 #' + str(current_count)
    msg['From'] = email_info.get('from_address')
    msg['To'] = email_info.get('to_address')
    log(u'发送的信息：\n' + str(msg))
    server = smtplib.SMTP()
    server.connect(email_info.get('email_host'))
    server.login(email_info.get('from_address'), email_info.get('password'))
    server.sendmail(email_info.get('from_address'), [email_info.get('to_address')], msg.as_string())
    server.close()
    log('发送邮件完成')


if __name__ == '__main__':
    monitor()
