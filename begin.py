import os
import sys

from scrapy.cmdline import execute

# 打断点调试py文件
# sys.path.append('D:\PyCharm\py_scrapyjobbole')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
print(os.path.dirname(os.path.abspath(__file__)))

if not os.path.exists('sol'):
    os.mkdir('sol')

execute(['scrapy', 'crawl', 'etherscan1'])
