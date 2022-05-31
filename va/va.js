exports.convertRaw = convertRaw; // 用于测试，Tasker中注释掉这行，否则报错

function convert(configs, command) {
    var task, param1, param2;
    for (var i of configs) {
        var parts = i.split(/ +/);
        if (new RegExp(parts[0]).test(command)) {
            task = parts[1];
            if (parts.length > 2) {
                param1 = command.match(new RegExp(parts[2]))[0];
            }
            if (parts.length > 3) {
                var result = command.match(new RegExp(parts[3]));
                if (result != null && result.length > 0) {
                    param2 = result[0];
                }
            }
            break;
        }
    }
    return [task, param1, param2];
}

function convertRaw(rawConfig, rawCommand) {
    const configs = rawConfig.split("\\n");
    const command = rawCommand.replace(/^[。. ]/, "").replace(/[。. ]$/, "");
    return convert(configs, command);
}

// var task;
// var param1;
// var param2;
// function main() {
//     var result = convertRaw(config, com);
//     task = result[0];
//     param1 = result[1];
//     param2 = result[2];
// }

// main();

