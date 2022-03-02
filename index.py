import os.path
from importlib import util


def check_module_integrity():
    try:
        for name in ("requests", "pillow", "urllib3", "bs4",):
            util.find_spec(name)
            print('finding...')
    except ImportError as e:
        raise ImportError(f"依赖库不完整, 请使用pip安装\n[{e}]")


def env_clear():
    for file_name in ['teen-study/finish.jpg', 'teen-study/personal_info.jpg']:
        if os.path.exists(file_name):
            os.remove(file_name)
            print('del!')


def submit_info():
    # TODO 先鸽在这 要去写openid的获取办法
    print('')


def main():
    # 主函数
    check_module_integrity()



    # at last
    env_clear()


def main_handler(event, context):
    # 腾讯云入口函数
    main()
    return 'ok'


if __name__ == '__main__':
    main()
