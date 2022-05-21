const MSG_TYPE_GROUP = 1;
const MSG_TYPE_PERSONAL = 2;
const MSG_NOTIFICATION = 3;

function parse(notification) {
    let splits = notification.split(",");
    let rawContent = splits.slice(2).join(",").match(/.+(?=,%evtprm4,%evtprm5,%evtprm6)/)[0];
    let msgFrom = splits[1];
    var msgType, msgPublisher, msgNum, msgContent;

    if (rawContent.includes(": ")) {
        let contentSplits = rawContent.split(": ");

        if (/^\[\d+条].+$/.test(contentSplits[0])) {
            msgPublisher = contentSplits[0].match(/(\[\d+条])?(.+)/)[2];
            msgNum = contentSplits[0].match(/(?<=\[)\d+(?=条])/)[0];
        } else {
            msgPublisher = contentSplits[0];
            msgNum = 1;
        }

        msgContent = contentSplits[1];
        msgType = msgFrom !== msgPublisher ? MSG_TYPE_GROUP : MSG_TYPE_PERSONAL;
    } else {
        msgType = MSG_TYPE_PERSONAL;
        msgPublisher = splits[1];
        msgNum = 1;
        msgContent = rawContent;
    }

    if (!/,%evtprm\d,msg,false/.test(splits.slice(3).join(","))) {
        msgType = MSG_NOTIFICATION;
    }

    return {
        from: msgFrom,
        type: msgType,
        publisher: msgPublisher,
        num: msgNum,
        content: msgContent
    };
}

function actionMessage(msg) {
    let types = ["图片", "动画表情", "链接", "语音", "文件", "视频"];
    let numWord = ["一张", "一张", "一条", "一段", "一个", "一段"];

    if (/.*@.+ .*/.test(msg)) {
        who = msg.match(/(?<=@).+(?= )/)[0];
        msg = msg.replace(/@.+? /, "");
        return `@了${who}并且说，${msg}`;
    } 
    if (/\[.{1,4}]/.test(msg)) {
        let type = types.find(v => msg.includes(v));
        if (type !== undefined) {
            return `发布了${numWord[types.indexOf(type)]}${type}`;
        } else {
            return `发布了一个表情，${msg}`;
        }
    }   
    return "说，" + msg;
}

function read(notification) {
    const packages = {
        "com.tencent.mm": "微信",
        "com.tencent.tim": "qq",
        "com.tencent.wework": "企业微信"
    };

    let notificationSplits = notification.split(",");
    let application = packages[notificationSplits[0]];

    if (application === "微信") {
        let results = parse(notification);
        let actionMeg = actionMessage(results.content);

        switch(results.type) {
            case MSG_TYPE_GROUP:
                return `${application}消息，${results.publisher}在群${results.from}中${actionMeg}`;
            case MSG_TYPE_PERSONAL:
                return `${application}消息，${results.publisher}${actionMeg}`;
            default:
                if (results.content.includes("语音通话中")) {
                    return `${application}提醒，和${results.from}语音通话中`;
                } else {
                    return `${application}通知，${results.from},${results.content}`;
                }
        }
    } else {
        if (application === null) {
            application = "应用" + notificationSplits[0];
        }
        return `${application}消息，${notificationSplits[1]}` + notificationSplits.slice(2).join(",");
    }
}

 var output = read(rawmsg);; // 输出变量%output, task中局部变量名应为%rawmsg

//console.log(read("com.tencent.mm,GIANT心電途自行車俱樂部,乐益～老湿人: @凤仙 明早7：30分凤凰弯等你[呲牙]？,%evtprm4,%evtprm5,%evtprm6,msg,false"));

// function main() {
//     let text = process.argv[2];
//     console.log(`raw: ${text}`);
//     // let text = "com.tencent.wework,打卡,下班打卡提醒,%evtprm4,%evtprm5,%evtprm6,msg,true";
//     console.log(`msg: ${read(text)}`);
//     console.log()
// }

// main();
