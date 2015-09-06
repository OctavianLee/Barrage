# Barrage

一个开源的b站直播间弹幕姬，主播可以获取直播间内弹幕信息且可以进行发送弹幕功能。

参考了弹幕姬的功能，感谢copyliu!

感谢b站高人气直播间提供的大量弹幕！

版本 ***0.1.6***

## 功能介绍

+ 在直播间接收弹幕；
+ 在直播间发送弹幕；
+ ...

## 使用说明

+ 安装环境：

```python
pip install -r requirements.txt
```

+ 代码使用：

```python
python main.py
```


## Todo List

+ 代码项目化；
+ 编写测试，完成开源配套设施；
+ 打包命令行版发布；
+ 制作UI版；
+ 提升服务质量。

***

Version Changes:

+ 2015-07-12 05H  完成接收弹幕的功能，能实时捕获弹幕信息。 By Octavian
+ 2015-07-13 01H  完成弹幕发送的功能，能登陆后进入直播间持续发送弹幕。 By Octavian
+ 2015-07-14 04H  可以持续获取弹幕信息，但是断线问题没有得到有效解决。 By Octavian
+ 2015-07-14 11H  整合代码，增加体验和错误控制功能，可以使用。 By Octavian
+ 2015-07-22 11H  修改bug，结构性重构代码。 By Octavian
+ 2015-07-23 04H  更新获取数据结构，能够获取直播间人数。 By Octavian
+ 2015-07-24 02H  添加数据模型，拆分弹幕接收功能接口功能。 By Octavian
+ 2015-09-04 02H  解决接受弹幕服务各类连接问题（包括保持连接，超时响应，异常中止服务等）及体验问题（包括弹幕异常，更多的文本反馈等）（暂时未优化本次版本代码）。 By Octavian
+ 2015-09-05 22H  Finish the new model of producer and consumer and Refator the code about recieving danmaku. By Octavian
+ 2015-09-06 23H  Fix the bug when caught timeout and Write some basic documents in files. By Octavian
+ 2015-09-06 24H  Fix the problem about decoding Chinese. By Octavian
