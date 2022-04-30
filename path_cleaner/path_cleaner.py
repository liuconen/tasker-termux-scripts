#!/data/data/com.termux/files/usr/bin/python
import os
import shutil
import datetime
import sys
import time


def _any(predicate, iterable) -> bool:
    for i in iterable:
        if predicate(i):
            return True
    return False


def find_match_dest(ext: str, match: dict) -> str or None:
    if ext is None:
        return None
    for dir, keys in match.items():
        if _any(lambda v: ext.lower() == v, keys):
            return dir
    return None


def move(src: str, des: str):
    if not os.path.exists(des):
        print(f'mkdir {des}')
        os.makedirs(des)
    if os.path.exists(f'{des}{os.path.basename(src)}'):
        basename = os.path.basename(src)
        des = f'{des}{time.time()}-{basename}'
    print(f'move {src} to {des}')
    shutil.move(src, des)


def move_file(file: str, match: dict, default_move_path: str):
    splits = os.path.basename(file).split('.')
    ext = splits[-1] if len(splits) > 1 else None
    dest = find_match_dest(ext, match)
    if dest is None:
        dest = default_move_path
    move(file, dest)


def get_dir_files(root: str, recursive: bool = False) -> list:
    result = []
    if not os.path.exists(root):
        return result
    for f in os.listdir(root):
        f = root + '/' + f
        if os.path.isfile(f):
            result.append(f)
        elif recursive and os.path.isdir(f):
            result += get_dir_files(f, recursive)
    return result


if __name__ == '__main__':
    # 创建回收站文件夹/sdcard/.RecycleBin
    recycle_bin = '/sdcard/.RecycleBin/' + datetime.datetime.now().strftime('%Y%m%d')
    device_os = sys.argv[1]
    if os.path.isdir(recycle_bin):
        sys.exit()
    else:
        os.makedirs(recycle_bin)

    # 系统相关的白名单文件夹
    device_white_list = {
        'miui': [
            'Catfish',  # 系统的文件搜索
            'mipush',
        ],
        'flyme': [
            '.flymeSafeBox',  # flyme相关
            'Customize',  # 魅族手机主题相关
            'meizu',
        ],
        'mokee': [],
        'zui': [],
        'ppui': [
            'Audiobooks',
            'Fonts',
            'Notifications',
        ]
    }
    # 通用的白名单文件夹
    white_list = [
                     '.RecycleBin',
                     '.YoudaoNote',
                     'Alarms',
                     'Android',
                     'amap',  # 高德
                     'autonavi',  # 高德
                     'DCIM',
                     'DingTalk',
                     'Documents',
                     'Download',
                     'IDMP',  # IDMP下载器
                     'iReader',  # 掌阅
                     'Movies',
                     'Music',
                     'netease',  # 网易云
                     'Pictures',
                     'PlugIReader',  # 掌阅
                     'Podcasts',  # 博客(通常是系统自带的)
                     'Quark',
                     'qqmusic',
                     'Recorder',  # 通话录音
                     'Ringtones',
                     'smartisan',  # 锤子便签
                     'SpeedSoftware',
                     'Tasker',
                     'TWRP',  # twrp recovery创建的目录
                     'tencent',
                     'UCTurbo',
                     'voice',
                     'zhihu',
                 ] + device_white_list.get(device_os, [])
    for i in white_list:
        print(i)
    # 文件整理到的目标目录
    documents = {
        '/sdcard/Documents/Notes/': ['md', 'mht', 'mhtml'],
        '/sdcard/Documents/Docs/': ['xls', 'xlsx', 'ppt', 'doc', 'docx', 'pdf', 'txt', 'ofd', 'rtf'],
        '/sdcard/Documents/Archivers/': ['zip', 'rar', '7z', 'tar', 'jar'],
        '/sdcard/Documents/Others/': ['vcf'],
        '/sdcard/Pictures/Others/': ['jpg', 'jpeg', 'png', 'gif', 'bmp'],
        '/sdcard/Movies/': ['mp4', '3gp', 'flv', 'avi', 'rmvb'],
        '/sdcard/Download/Apks/': ['apk', 'sh', 'py', 'exe', 'kt']
    }
    # 整理文件的目录
    file_clean_path = [
        ('/sdcard', False),
        ('/sdcard/UCTurbo', True),
        ('/sdcard/zhihu', True),
        ('/sdcard/IDMP', True),
        ('/sdcard/tieba', True),
        ('/sdcard/Download', False),
        ('/sdcard/SpeedSoftware', True),
    ]
    files = [f for path in file_clean_path for f in get_dir_files(path[0], path[1])]
    for f in files:
        move_file(f, documents, recycle_bin)

    # 整理文件夹的目录
    dir_clean_path = ['/sdcard']
    dirs = [path + '/' + d for path in dir_clean_path for d in os.listdir(path)]
    dirs = [i for i in dirs if os.path.isdir(i) and os.path.basename(i) not in white_list]
    for i in dirs:
        move(i, recycle_bin)
