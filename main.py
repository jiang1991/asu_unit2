import math

import grequests
import time
import os

url = 'http://3.35.16.246:5000/upload'
url_m = 'http://3.35.16.246:5000/'

file_dir = f'D:\\python\\asu_unit2\\imagenet-100'


# file = {'myfile': open('./imagenet-100/test_1.JPEG', 'rb')}

# 识别
def diagnose(file):
    file_upload_path = os.path.join(file_dir, file)
    print(f'开始识别 {file}')
    file_upload = {'myfile': open(file_upload_path, 'rb')}

    # s = int(round(time.time() * 1000))  # request开始时间戳
    r = grequests.post(url, files=file_upload)
    # r = requests.get(url_m)
    # e = int(round(time.time() * 1000))  # request结束时间戳

    # print(f'识别结果为: {r[0].text}\r\n', f'{file}请求时长: {e - s}ms')
    return r


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    list_file = os.listdir(file_dir)
    # 一次最多并行10张图片

    r_times = math.ceil(len(list_file)/10)  # 请求次数
    print(len(list_file), r_times)

    for i in range(r_times):
        req_list = []
        i_max = min(10 * (i + 1) - 1, len(list_file))
        for j in (10*i, i_max):
            req_list.append(diagnose(list_file[j]))
        # print(req_list)
        res_list = grequests.map(req_list)
        for res in res_list:
            print(res.text)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
