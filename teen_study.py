import requests
import requests.utils
import yaml
from random import choice
from urllib.request import urlretrieve
import PIL.Image as Image
import PIL.ImageDraw as Draw
import PIL.ImageFont as Font
import io
from bs4 import BeautifulSoup

with open('config.yml', 'r', encoding='utf-8') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)


def add_horizontal_center_text(img_path, text, y=0, color=(255, 255, 255), size=40):
    image = Image.open(img_path)
    draw = Draw.Draw(image)
    font = Font.truetype("font/" + config['font'], size, encoding='utf-8')
    x_coordinate = int((image.size[0] - font.getsize(text)[0]) / 2)
    draw.text((x_coordinate, y), text, color, font=font)
    return image


def show_exit(content):
    """
    输出错误原因，辅助退出
    :param content:
    :return:
    """
    input(content)
    exit()


def get_code(s):
    """
    调用API获取最新一期青春学习的CODE
    :return:
    """
    url = "https://h5.cyol.com/special/weixin/sign.json"
    headers = {
        "Host": "h5.cyol.com",
        "Connection": "keep-alive",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; PACM00 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, "
                      "like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3164 MMWEBSDK/20211001 Mobile Safari/537.36 "
                      "MMWEBID/556 MicroMessenger/8.0.16.2040(0x28001056) Process/toolsmp WeChat/arm32 Weixin "
                      "NetType/WIFI Language/zh_CN ABI/arm64",
        "Origin": "http://h5.cyol.com",
        "X-Requested-With": "com.tencent.mm",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    resp = s.get(url, headers=headers).json()

    return list(resp)[-1]


def get_user(s):
    """
    调用API获取用户的信息
    :return:
    """
    headers = {
        "Host": "api.fjg360.cn",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; PACM00 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, "
                      "like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3164 MMWEBSDK/20211001 Mobile Safari/537.36 "
                      "MMWEBID/556 MicroMessenger/8.0.16.2040(0x28001056) Process/toolsmp WeChat/arm32 Weixin "
                      "NetType/WIFI Language/zh_CN ABI/arm64",
        "Accept": "*/*",
        "X-Requested-With": "com.tencent.mm",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Dest": "script",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    url = "https://api.fjg360.cn/index.php?m=vote&c=index&a=get_members&openid=" + config['openid']
    resp = s.get(url, headers=headers).json()
    if resp.get("code") == 1:
        print(resp.get("h5_ask_member"))
        return resp.get("h5_ask_member")

    # 在此处获取的className貌似是那种之前的? 最晚一次的登录/观看数据.
    else:
        show_exit("您的OPENID配置有误，请检查后重试")


def get_course(s, code):
    headers = {
        "Host": "h5.cyol.com",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; PACM00 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, "
                      "like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3164 MMWEBSDK/20211001 Mobile Safari/537.36 "
                      "MMWEBID/556 MicroMessenger/8.0.16.2040(0x28001056) Process/toolsmp WeChat/arm32 Weixin "
                      "NetType/WIFI Language/zh_CN ABI/arm64",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/wxpic,image/tpg,image/apng,"
                  "*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "X-Requested-With": "com.tencent.mm",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    url = 'https://h5.cyol.com/special/daxuexi/' + code + '/m.html'
    resp = s.get(url, headers=headers)
    soup = BeautifulSoup(resp.content.decode("utf8"), "lxml")
    course = soup.title.string[7:]
    print(course)
    return course


def save_door(info, course, s):
    """
    调用API提交用户进入页面信息至青春湖北数据库
    :param s:
    :param course:
    :param info:
    :return:
    """
    headers = {
        "Host": "cp.fjg360.cn",
        "Connection": "keep-alive",
        "Accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, "
                  "*/*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; PACM00 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, "
                      "like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3164 MMWEBSDK/20211001 Mobile Safari/537.36 "
                      "MMWEBID/556 MicroMessenger/8.0.16.2040(0x28001056) Process/toolsmp WeChat/arm32 Weixin "
                      "NetType/WIFI Language/zh_CN ABI/arm64",
        "X-Requested-With": "XMLHttpRequest",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    url = "https://cp.fjg360.cn/index.php?m=vote&c=index&a=save_door&sessionId=&imgTextId=&ip="
    url += "&username=" + info["name"]
    url += "&phone=" + "未知"
    url += "&city=" + info["danwei1"]
    url += "&danwei2=" + info["danwei3"]
    url += "&danwei=" + info["danwei2"]
    url += "&openid=" + config['openid']
    url += "&num=10"
    url += "&lesson_name=" + course
    resp = s.get(url, headers=headers).json()
    if resp.get("code") == 1:
        return True
    else:
        show_exit("您的用户信息有误，请检查后重试")


def get_finish_pic(code):
    """
    通过调用dxx青年大学习的公众号服务来获取图片
    :param code:
    :return:
    """
    base_url = "https://h5.cyol.com/special/daxuexi/"

    base_url += code
    base_url += "/images/end.jpg"

    print(base_url)

    urlretrieve(base_url, config['output_dir'] + "finish.jpg")


def get_user_info_pic(course, name, id, company):
    """
    获取用户信息相关截图
    :param id:
    :param name:
    :param course:
    :param company:
    :return:
    """
    req_url = config['personal_info_generate_server']
    req_url += "?course=" + str(course)
    req_url += "&name=" + str(name)
    req_url += "&id=" + str(id)
    req_url += "&company=" + str(company)

    data = {
        'url': req_url,
        'token': config['token'],
        'width': '828',  # 此大小与中青在线提供的完成图片大小一致
        'height': '1366',
        'delay': '1000',
        'device': 'mobile'
    }

    r = requests.post("https://www.screenshotmaster.com/api/v1/screenshot", data=data)
    img = Image.open(io.BytesIO(r.content))
    img = img.convert("RGB")
    img.save(config['output_dir'] + "personal_info.jpg")


def image_processing(course_name, content_img_paths):
    if config['add_status_bar']:
        status_img_path = choice(config['status_images'])
        # TODO: 添加针对不同状态栏高度的适配
        # 具体: 微信toolbar的高度貌似是一样的?
        for content_img_path in content_img_paths:
            content_img = Image.open(content_img_path)
            status_img = add_horizontal_center_text(status_img_path, "“青年大学习”" + course_name, 93, (0, 0, 0), 40)
            full_img = Image.new('RGB', (828, content_img.size[1] + status_img.size[1]), (255, 255, 255))

            full_img.paste(status_img, (0, 0))
            full_img.paste(content_img, (0, status_img.size[1]))

            full_img.save(content_img_path)


def add_name(content_image_paths):
    for content_image_path in content_image_paths:
        result = add_horizontal_center_text(content_image_path, config['name'], 500, (10, 220, 120), 90)
        # result.show()
        result.save(content_image_path)


def run():
    images = config['content_images']

    s = requests.session()
    code = get_code(s)
    user_info = get_user(s)
    course = get_course(s, code)
    save_door(user_info, course, s)
    get_finish_pic(code)
    get_user_info_pic(course, user_info["name"], user_info["uid"],
                      user_info["danwei1"] + user_info["danwei2"] + user_info["danwei3"])

    image_processing(course, images)

    if config['add_name']:
        add_name(images)


if __name__ == '__main__':
    run()
