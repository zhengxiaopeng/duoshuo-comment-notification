## 多说评论邮件通知脚本程序

使用，修改ds.config为你的正确配置信息：  

``` bash
[email_info]
email_host = 电子邮件主机，如：smtp.qq.com，注意你的邮箱是否开启了POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务
from_address = 你要发送邮件的邮件地址
password = 邮箱的登陆密码
to_address = 你要接受邮件的地址

[duoshuo_account]
name = 多说的二级域名名, 如我的：rocko
secret = 多说的秘钥，在后台的设置查看
id = 多说用户 id，用于排除自己的评论。http://duoshuo.com/settings/ 中点击用户名然后在地址栏中的 profile 后跟着的数字即为 id

[period_time]
period = 定时检查评论的时间（s）
```

## 运行
``` Bash
python ds.py
```
   
## 开机自启

在 `/etc/rc.local` 的 **exit 0** 前加入，python 的路径视自己情况而定。
``` bash
/usr/bin/python /your_path/ds.py &
exit 0

```

   
## License

-------

```
Copyright 2015 Rocko (zhengxiaopeng.com) <rocko.zxp@gmail.com>.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
