import os.path
import sys
from importlib import util
import teen_study
import ruoli_opt
import yaml


def main():
    # 主函数
    os.environ['TZ'] = "Asia/Shanghai"  # 将时区设为UTC+8

    with open('config.yml', 'r', encoding='utf-8') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    for user in config['users']:
        teen_study.run(user=user)
        ruoli_opt.main(user)  # 待修改



def main_handler(event, context):
    # 腾讯云入口函数
    main()
    return 'ok'


def handler(event, context):
    # 阿里云入口函数
    main()
    return 'ok'


if __name__ == '__main__':
    main()
