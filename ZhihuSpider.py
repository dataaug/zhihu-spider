# -*- coding: utf-8  -*-
"""
Module name: ZhihuSpider;
Author: Duguce;
Description: 抓取知乎某一问题下的所有回答（回答数量不超过800左右）
"""

import datetime
import time, json, re
from time import sleep
import pandas as pd
import config
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


def get_html(url):
    driver = get_driver(url)
    # 隐式等待
    driver.implicitly_wait(10)
    # 浏览器最大化
    driver.maximize_window()
    driver.get(url)
    time.sleep(random.uniform(3, 4))
    # 定位登录界面关闭按钮
    close_btn = driver.find_element(By.XPATH, "//button[@class='Button Modal-closeButton Button--plain']")
    # 点击登录界面关闭按钮
    close_btn.click()
    scroll_to_bottom(driver)
    answerElementList = driver.find_elements(By.CSS_SELECTOR, "#QuestionAnswers-answers .List-item .ContentItem")
    return answerElementList, driver


def get_driver(url):
    # 输入需要爬取知乎回答的问题链接
    # url = input('请输入需要爬取知乎回答的问题链接：\n')
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    # 谷歌文档提到需要加上这个属性来规避bug
    chrome_options.add_argument('--disable-gpu')
    # # 禁止图片和CSS加载，减小抓取时间
    prefs = {'profile.default_content_setting_values': { 'images': 2, 'javascript': 2, 
                            'plugins': 2,}}
    chrome_options.add_experimental_option("prefs", prefs)


    # 禁止图片和CSS加载，减小抓取时间
    # firefox_profile = webdriver.ChromeOptions()
    # firefox_profile.set_preference('permissions.default.image', 2)
    # firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
    # firefox_profile.set_preference('permissions.default.stylesheet', 2)
    # 打开浏览器 mac 如果是win，在chromedriver后添加.exe
    s = Service("Driver/chromedriver")

    driver = webdriver.Chrome(service=s, options=chrome_options)
    return driver


def scroll_to_bottom(driver):
    # 获取当前窗口的总高度
    js = 'return action=document.body.scrollHeight'
    # 初始化滚动条所在的高度
    height = 0
    # 当前窗口总高度
    currHeight = driver.execute_script(js)
    while height < currHeight:
        # 将滚动条调整至页面底端
        for i in range(height, currHeight, 100):
            driver.execute_script("window.scrollTo(0, {})".format(i))
            time.sleep(0.01)
        height = currHeight
        currHeight = driver.execute_script(js)
        time.sleep(0.2)


def get_answers(answerElementList, url):
    # 定义一个存储回答中的信息的数据表格
    answerData = pd.DataFrame(
        columns=(
            'question_title', 'answer_url', 'question_url', 'author_name', 'fans_count', 'created_time', 'updated_time',
            'comment_count',
            'voteup_count', 'content'))
    numAnswer = 0
    # 遍历每一个回答并获取回答中的信息
    for answer in answerElementList:
        dictText = json.loads(answer.get_attribute('data-zop'))
        question_title = dictText['title']  # 问题名称
        answer_url = answer.find_element(By.XPATH,
                                         "meta[@itemprop='url' and contains(@content, 'answer')]").get_attribute(
            'content')  # 获取回答的链接
        author_name = dictText['authorName']  # 回答作者名称
        fans_count = answer.find_element(By.XPATH, "*//meta[contains(@itemprop, 'followerCount')]").get_attribute(
            'content')  # 获取粉丝数量
        created_time = answer.find_element(By.XPATH, "meta[@itemprop='dateCreated']").get_attribute(
            'content')  # 获取回答的创建时间
        updated_time = answer.find_element(By.XPATH, "meta[@itemprop='dateModified']").get_attribute(
            'content')  # 获取回答最近的编辑时间
        comment_count = answer.find_element(By.XPATH, "meta[@itemprop='commentCount']").get_attribute(
            'content')  # 获取该回答的评论数量
        voteup_count = answer.find_element(By.XPATH, "meta[@itemprop='upvoteCount']").get_attribute(
            'content')  # 获取回答的赞同数量
        contents = answer.find_elements(By.TAG_NAME, "p")# .text.replace("\n", "")  # 回答内容
        # print(contents.text)
        content = ''.join([content.text for content in contents])
        # print(answer)
        # content = ''
        time.sleep(0.001)
        row = {'question_title': [question_title],
               'author_name': [author_name],
               'question_url': [url],
               'answer_url': [answer_url],
               'fans_count': [fans_count],
               'created_time': [created_time],
               'updated_time': [updated_time],
               'comment_count': [comment_count],
               'voteup_count': [voteup_count],
               'content': [content]
               }
        answerData = answerData.append(pd.DataFrame(row), ignore_index=True)
        numAnswer += 1
        print(f"[NORMAL] 问题：【{question_title}】 的第 {numAnswer} 个回答抓取完成...")
        time.sleep(0.2)

    return answerData, question_title


if __name__ == '__main__':

    # 获取当前已经抓取的所有问题
    try:
        df_tmp = pd.read_csv('zhihu_result.csv')
        question_url_contained = set(df_tmp['question_url'].to_list())
        
    except Exception as e:
        print('no breakpoint:', e)
        question_url_contained = set()

    answerData_all = pd.DataFrame(
        columns=(
            'question_title', 'answer_url', 'question_url', 'author_name', 'fans_count', 'created_time', 'updated_time',
            'comment_count',
            'voteup_count', 'content'))
    print('需要抓取的问题数量：', len(config.urls))
    for url in config.urls:
        print('----------------------------------------')
        if url in question_url_contained:
            continue
        print('url:', url)

        # https://www.zhihu.com/question/20000010
        url_num = int(url.split('/')[-1])
        if True:
            time.sleep(random.uniform(30, 40))
            answerElementList, driver = get_html(url)
            print("[NORMAL] 开始抓取该问题的回答...")
            answerData, question_title = get_answers(answerElementList, url)
            print(f"[NORMAL] 问题：【{question_title}】 的回答全部抓取完成...")
            time.sleep(random.uniform(1, 3))
            question_title = re.sub(r'[\W]', '', question_title)
            filename = str(f"result-{datetime.datetime.now().strftime('%Y-%m-%d')}-{question_title}")
            # answerData.to_csv(f'{config.results_path}/{filename}.csv', encoding='utf-8', index=False)
            # 并入总表
            answerData_all = answerData_all.append(pd.DataFrame(answerData), ignore_index=True)
            #if url_num % 100 == 0:
            answerData_all.to_csv(f'zhihu_result.csv', encoding='utf-8', index=False)
            print(f"[NORMAL] 问题：【{question_title}】 的回答已经保存至 {filename}.xlsx...")
            driver.close()
            # print(e)
            # print(f"[ERROR] 抓取失败...")
