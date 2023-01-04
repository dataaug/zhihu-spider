import os

# 需要爬取知乎回答问题的链接
with open('need_links.txt', 'r', encoding='utf-8') as f:
    urls = f.read().split('\n')
# urls = ['https://www.zhihu.com/question/19550249']

# 将爬取的数据存储于Results文件中
results_path = os.path.join(os.getcwd(), 'Results')
