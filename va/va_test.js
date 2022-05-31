const utils = require('../asserts_util');
const va = require('./va');

const configs = ".*手电筒    开关闪光灯\\n" +
    "倒计时.+   倒计时     (?<=倒计时).+\\n" +
    "打开.+      打开应用      (?<=打开).+\\n" +
    "提醒我.+      设置闹钟    \d+:\d+    (?<=\d)[^\d:].*\\n" +
    "[添增]加[代待]办.+   添加待办   (?<=办).+\\n" +
    "任务.+      添加待办      (?<=任务).+\\n" +
    "搜索.+      搜索     (?<=搜索).+\\n" +
    "现在是?几点钟?      报时\\n" +
    ".*远程登录.*   启动SSH服务\\n" +
    ".+       执行任务    .+?(?=，)|.+     (?<=，).+";

console.assert(utils.arrayEqual(va.convertRaw(configs, "倒计时0.5分钟。"), ["倒计时", "0.5分钟", undefined]));