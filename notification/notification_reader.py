#!/data/data/com.termux/files/usr/bin/python
import sys
import re

packages = {
    'com.tencent.mm': '微信',
    'com.tencent.tim': 'qq',
    'com.tencent.wework': '企业微信',
}


class WechatNotificationParser:
    MSG_TYPE_GROUP = 1
    MSG_TYPE_PERSONAL = 2
    MSG_NOTIFICATION = 3  # 非消息类型的微信通知

    msg_from = None  # 比如某人或某群
    msg_type = None  # 个人消息或群消息
    msg_publisher = None  # 发消息的人
    msg_num = 1  # 当前未读消息数量
    msg_content = None  # 消息内容

    def __init__(self, notification: str):
        splits = notification.split(',')
        raw_content = re.search('.+(?=,%evtprm4,%evtprm5,%evtprm6)', ','.join(splits[2:])).group()
        self.msg_from = splits[1]
        if ': ' in raw_content:
            content_splits = raw_content.split(': ')
            if re.match('^\\[\\d+条].+$', content_splits[0]):
                self.msg_publisher = re.search('(\\[\\d+条])?(.+)', content_splits[0]).groups()[1]
                self.msg_num = re.search('(?<=\\[)\\d+(?=条])', content_splits[0]).group()
            else:
                self.msg_publisher = content_splits[0]
                self.msg_num = 1
            self.msg_content = content_splits[1]
            self.msg_type = WechatNotificationParser.MSG_TYPE_GROUP if self.msg_from != self.msg_publisher \
                else WechatNotificationParser.MSG_TYPE_PERSONAL
        else:
            self.msg_type = WechatNotificationParser.MSG_TYPE_PERSONAL
            self.msg_publisher = splits[1]
            self.msg_num = 1
            self.msg_content = raw_content
        if re.search(',%evtprm\\d,msg,false', ','.join(splits[3:])) is None:
            self.msg_type = WechatNotificationParser.MSG_NOTIFICATION

    @staticmethod
    def find(predicate, iterable) -> object:
        for i in iterable:
            if predicate(i):
                return i
        return None

    @staticmethod
    def action_message(msg: str) -> str:
        types = ['图片', '动画表情', '链接', '语音', '文件', '视频']
        num_word = ['一张', '一张', '一条', '一段', '一个', '一段']
        if re.match('\\[.{1,4}]', msg):  # 没有文字内容
            _type = WechatNotificationParser.find(lambda x: x in msg, types)
            if _type is not None:
                return f'发布了{num_word[types.index(_type)]}{_type}'
            else:
                return f'发布了一个表情，{msg}'
        else:
            return '说，' + msg


def read(notification: str) -> str:
    notification_splits = notification.split(',')
    application = packages[notification_splits[0]]
    if application == '微信':
        results = WechatNotificationParser(notification)
        action_meg = WechatNotificationParser.action_message(results.msg_content)
        if results.msg_type == WechatNotificationParser.MSG_TYPE_GROUP:
            return f'{application}消息，{results.msg_publisher}在群{results.msg_from}中{action_meg}'
        elif results.msg_type == WechatNotificationParser.MSG_TYPE_PERSONAL:
            return f'{application}消息，{results.msg_publisher}{action_meg}'
        else:
            return f'{application}通知，{results.msg_from},{results.msg_content}'
    else:
        if application is None:
            application = '应用' + notification_splits[0]
        return f'{application}消息，{notification_splits[1]}' + ','.join(notification_splits[2:])


if __name__ == '__main__':
    notification = ' '.join(sys.argv[1:])
    print(read(notification))
