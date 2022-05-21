# tasker-termux-scripts

一些个人使用的、应用于Tasker或Termux的工具代码集合。

## NotificationReader

用于将Tasker读取到的通知信息`%evtprm()`转换为自然的中文语言描述，通常作为语音播报。

比如接收到微信消息张三给你发一条消息，你好，转换为字符串“微信消息，张三说，你好”.

主要处理了微信消息的解析，比如图片提示，位置提示，语音提示等。

有两个版本，重新实现的js版本无需额外组件即可由tasker调用。

## PathCleaner

清理手机根目录（/sdcard）的垃圾文件夹。

功能：

1. 并非删除文件夹或文件，而是移动到指定目录（.RecycleBin）。
2. 保留了Android的系统的目录和一些常用应用的目录，自行修改代码配置添加白名单。
3. 如果是文件会进行简单分类，移动到对应的文件夹，比如音乐、视频等。
4. 自动整理Download中的文件到对应的文件类型目录。