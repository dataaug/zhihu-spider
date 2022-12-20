# 这个程序简单记录所有有效的知乎问题链接
import requests
import re
import random
from time import sleep

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
nummber = 19550224
try:
    with open('breakpoint.txt', 'r') as f:
        nummber = int(f.read())
except:
    print('no breakpoint')

num_need = 1000
num_end = nummber + num_need
while nummber >= 19550224 and nummber <=  num_end:
    # 随机休息
    time_sleep = random.uniform(1, 4)
    sleep(time_sleep)

    nummber = nummber + 1
    url = 'https://www.zhihu.com/question/' + str(nummber)
    response = requests.get(url, headers=headers)
    # print(url)
    # print(response.text)
    if response.status_code == 200:
        if '你似乎来到了没有知识存在的荒原' in response.text:
            continue
        else:
            title = re.findall('<title data-rh="true">(.*)</title>', response.text)[0]
            num_answer = re.findall('<span>(.*)<!-- --> 个回答</span>', response.text)[0]
            print('title:', title)
            print('num_answer:', num_answer)
            if title == "安全验证 - 知乎":
                print('question id:', nummber, ';触发安全验证，请降低速度')
                with open('breakpoint.txt', 'a') as f:
                    f.write(str(nummber))
                break

            with open('zhihu_valid_links.txt', 'a') as f:
                f.write(url + '|*|' + title +'|*|' + str(num_answer) + '\n')
            # print(response.text)

        print(url)
        print('--')
    else:
        print('question id:', nummber, ';error code:', response.status_code)
