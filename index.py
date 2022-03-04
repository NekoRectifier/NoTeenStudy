import os.path
import sys
from importlib import util
import teen_study
import ruoli_opt


def check_module_integrity():
    try:
        for name in ("requests", "pillow", "urllib3", "bs4",):
            util.find_spec(name)
            print('finding...')
    except ImportError as e:
        raise ImportError(f"依赖库不完整, 请使用pip安装\n[{e}]")
    sys.path.append(os.getcwd())


def main():
    # 主函数
    os.environ['TZ'] = "Asia/Shanghai"  # 将时区设为UTC+8
    check_module_integrity()
    teen_study.run()
    ruoli_opt.main()


def main_handler(event, context):
    # 腾讯云入口函数
    main()
    return 'ok'


if __name__ == '__main__':
    main()
