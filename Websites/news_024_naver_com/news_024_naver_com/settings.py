# Scrapy settings for news_024_naver_com project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import os

BOT_NAME = "news_024_naver_com"

SPIDER_MODULES = ["news_024_naver_com.spiders"]
NEWSPIDER_MODULE = "news_024_naver_com.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "news_024_naver_com (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
   'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
   'accept-encoding': 'gzip, deflate, br',
   'accept-language': 'zh-CN,zh;q=0.9',
   'cache-control': 'no-cache',
   'pragma': 'no-cache',
   'referer': 'https://news.naver.com/',
   'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"Windows"',
   'sec-fetch-dest': 'document',
   'sec-fetch-mode': 'navigate',
   'sec-fetch-site': 'same-origin',
   'sec-fetch-user': '?1',
   'upgrade-insecure-requests': '1',
   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "news_024_naver_com.middlewares.News024NaverComSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "news_024_naver_com.middlewares.News024NaverComDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   "news_024_naver_com.pipelines.News024NaverComPipeline": 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"


# CURRENT_ENVIRONMENT = 'dev'
CURRENT_ENVIRONMENT = 'live'

if CURRENT_ENVIRONMENT == 'dev':
   # DEV
   # Redis配置
   REDIS_HOST = '127.0.0.1'
   REDIS_PORT = 6379
   REDIS_DB = 2
   REDIS_PASSWORD = ''
   # 4. 启动 redis 数据

   DELAY_SECONDS = 0.5

   # mongodb配置
   MONGO_HOST = "127.0.0.1"  # 主机IP
   MONGO_PORT = 27017  # 端口号
   MONGO_DB = "news"  # 库名
   MONGO_COLL = "news_mr"  # collection名

else:
   # LIVE
   REDIS_HOST = '47.93.153.225'
   REDIS_PORT = 17396
   REDIS_DB = 2
   REDIS_PASSWORD = 'Yh16601111455!@#23436'
   # 4. 启动 redis 数据

   DELAY_SECONDS = 0.5

   # mongodb配置
   MONGO_HOST = "47.93.153.225"  # 主机IP
   MONGO_PORT = 17072  # 端口号
   MONGO_DB = "news"  # 库名
   MONGO_COLL = "news_mr"  # collection名
   MONGO_USER = "mongoadmin"  # 用户名
   MONGO_PASSWORD = "AveiDraJo23sddf123356Me"  # 密码

