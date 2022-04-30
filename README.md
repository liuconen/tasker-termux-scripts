# tasker-termux-scripts

一些个人使用的、应用于Tasker或Termux的工具代码集合。

## NotificationReader

用于将Tasker读取到的通知信息`%evtprm()`转换为自然的中文语言描述，通常作为语音播报。

比如接收到微信消息张三给你发一条消息，你好，转换为字符串“微信消息，张三说，你好”.

主要处理了微信消息的解析，比如图片提示，位置提示，语音提示等。

