# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class News024NaverComItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    title = scrapy.Field()  # 标题,
    site = scrapy.Field()  # 站点名称，如网易,
    author = scrapy.Field()  # 作者，如果没有为空字符串,
    source_url = scrapy.Field()  # 新闻所在的源地址,
    pictures = scrapy.Field()  # 新闻图片，如果没有为空字符串, 以逗号分割
    videos = scrapy.Field()  # 视频，以逗号分隔地址
    pubtime = scrapy.Field()  # 新闻实际发布时间, 格式为年月日时分秒（时间需要转化成东八区），如果没有使用当前时间
    source_content = scrapy.Field()  # 以html存储原来的网站内容，只存储包含内容的，不用存储全部html代码
    content = scrapy.Field()  # 新闻内容。处理后的网站内容是, 需要对内容格式化下，去除html，将换行替换成\n\t类似的内容
    category = scrapy.Field()  # 新闻类别，如果没有为空字符串
    country = scrapy.Field()  # 对应国家名称，如印度，巴基斯坦
    tag = scrapy.Field()  # 标签，以逗号分割，如果没有为空,
    language = scrapy.Field()  # 新闻使用的语言，如en，使用ISO639 - 1 标准https://xunyidian.com/t/Iso6391Manual
    update_time = scrapy.Field()  # 更新时间，格式为年月日时分秒
