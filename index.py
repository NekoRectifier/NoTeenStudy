import os.path
import sys
from importlib import util
import teen_study
import ruoli_opt


def main():
    # 主函数
    os.environ['TZ'] = "Asia/Shanghai"  # 将时区设为UTC+8
    teen_study.run()
    ruoli_opt.main()


def main_handler(event, context):
    # 腾讯云入口函数
    main()
    return 'ok'


if __name__ == '__main__':
    main()
