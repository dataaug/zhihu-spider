# 这个程序简单记录所有有效的知乎问题链接
import requests
import re
import random
from time import sleep

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
nummber = 19551349 # 初次运行时，默认开启知乎第一个问题

try:
    with open('zhihu_valid_links.txt', 'r') as f:
        data = f.readlines()[-1]
        # print(data)
        zhihu_link = data.split('|*|')[0]
        # print(zhihu_link.split('/'))
        nummber = int(zhihu_link.split('/')[-1].strip())
except Exception as e:
    print('no breakpoint:', e)

num_need = 100000
num_end = nummber + num_need
print(f'from {nummber} to {num_end}')
while nummber >= 19550224 and nummber <=  num_end:
    # 随机休息
    time_sleep = random.uniform(1, 4)
    sleep(time_sleep)

    nummber = nummber + 1
    url = 'https://www.zhihu.com/question/' + str(nummber)

    try: # 网络错误情况处理
        response = requests.get(url, headers=headers)
    except Exception as e:
        print('**')
        time_sleep = random.uniform(300, 600)
        print('网络错误，暂停{time_sleep}s')
        sleep(time_sleep)
        print('question id:', nummber, ';error:', e)
        nummber -= 1
        continue

    # print(url)
    # print(response.text)
    if response.status_code == 200:
        if '你似乎来到了没有知识存在的荒原' in response.text:
            continue
        else:
            title = re.findall('<title data-rh="true">(.*)</title>', response.text)[0]
    
            print('title:', title)
            if title == "安全验证 - 知乎":
                print('question id:', nummber, ';触发安全验证，请降低速度')
                with open('breakpoint.txt', 'a') as f:
                    f.write(str(nummber))
                break
            
            try:
                num_answer = re.findall('<span>(.*)<!-- --> 个回答</span>', response.text)[0]
            except Exception as e: # 一般是没有回答的问题
                # print('question id:', nummber, ';error:', e)
                # continue
                num_answer = 0

            print('num_answer:', num_answer)
            with open('zhihu_valid_links.txt', 'a') as f:
                f.write(url + '|*|' + title +'|*|' + str(num_answer) + '\n')
            # print(response.text)

        print(url)
        print('--')
    else:
        print('question id:', nummber, ';error code:', response.status_code)
