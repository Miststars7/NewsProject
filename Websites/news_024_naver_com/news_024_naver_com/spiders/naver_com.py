import json
from lxml import etree
import requests
import scrapy
from scrapy import cmdline
from scrapy.http.response.html import HtmlResponse
from scrapy.utils.project import get_project_settings
from .utils import get_last_month_timestamps, md5, convert_to_east_eight, is_exist, current_timestamp
from ..items import News024NaverComItem
settings = get_project_settings()


class NaverComSpider(scrapy.Spider):
    name = "naver_com"
    allowed_domains = ["news.naver.com"]
    start_urls = ["https://news.naver.com"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_month_datetime = get_last_month_timestamps()
        self.redis_key = 'news_024_naver_com'

    def start_requests(self):
        # world栏目
        url = "https://news.naver.com/section/104"
        yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response: HtmlResponse, **kwargs):
        if isinstance(response, HtmlResponse):
            html = response
            page_info = html.xpath('//div[@class="section_latest_article _CONTENT_LIST _PERSIST_META"]')
            page = page_info.xpath('./@data-page-no').get()
            next_timestamp = page_info.xpath('./@data-cursor').get()
        else:
            html_json = json.loads(response.body.decode(response.encoding))['renderedComponent']['SECTION_ARTICLE_LIST']
            html = etree.HTML(html_json)
            page_info = html.xpath('//div[@class="section_latest_article _CONTENT_LIST _PERSIST_META"]')[0]
            page = page_info.xpath('./@data-page-no')[0]
            next_timestamp = page_info.xpath('./@data-cursor')[0]

        # 新闻列表翻页  最近一个月
        # 生产时间
        if int(next_timestamp) > self.last_month_datetime:
            print(self.last_month_datetime)
            next_page_url = ('https://news.naver.com/section/template/SECTION_ARTICLE_LIST?sid=104&sid2=&cluid='
                             '&pageNo={0}&date=&next={1}&_={2}').format(page, next_timestamp, current_timestamp())
            if not is_exist(self.redis_key, next_page_url.rpartition('&_=')[0]):
                yield scrapy.Request(next_page_url, callback=self.parse, dont_filter=True)

        # 获取新闻详情
        news_list = html.xpath('//li[@class="sa_item _LAZY_LOADING_WRAP"]')
        for news in news_list:
            new_detail_url_obj = news.xpath('.//a[@class="sa_thumb_link"]/@href')
            if not isinstance(new_detail_url_obj, scrapy.selector.unified.SelectorList):
                new_detail_url = new_detail_url_obj[0]
            else:
                new_detail_url = new_detail_url_obj.get()
            if not is_exist(self.redis_key, new_detail_url):
                yield scrapy.Request(url=new_detail_url, callback=self.parse_new_detail, dont_filter=True)

    def parse_new_detail(self, response: HtmlResponse):

        new_html = response.xpath('//div[@id="newsct"]').getall()[0]
        article = response.xpath('//article[@id="dic_area"]')
        title = response.xpath('//h2[@id="title_area"]//text()').get()
        author = response.xpath('//em[@class="media_end_head_journalist_name"]/text()').get()
        img_list = article.xpath('.//img[@class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE"]/@data-src').getall()
        # 图片描述
        img_content = article.xpath('.//span[@style="color:#808080"]//text()').getall()
        img_content = ' '.join(img_content)
        publish_time = response.xpath('.//span[@class="media_end_head_info_datestamp_time '
                                      '_ARTICLE_DATE_TIME"]/@data-date-time').get()
        # 保留图片换行
        all_texts = article.xpath('.//text()').getall()
        # 去除存在图片描述
        content = ' '.join(all_texts).replace(img_content, '')

        video_map_list = []
        video_html = response.xpath('//div[@class="_VOD_PLAYER_WRAP"]')
        if video_html:
            try:
                video_id = video_html[0].xpath('./@data-video-id').get()
                video_key = video_html[0].xpath('./@data-inkey').get()
                video_url = ('https://apis.naver.com/rmcnmv/rmcnmv/vod/play/v2.0/{0}?key={1}&sid=2006&pid=&nonce={2}'
                             '&devt=HTML5_PC&prv=N&aup=N&stpb=N&cpl=zh_CN&env=real&lc=zh_CN&adi=%5B%7B%22'
                             'adSystem%22%3A%22null%22%7D%5D&adu=%2F').format(video_id, video_key, current_timestamp())
                # 视频地址需要单独获取
                response_video = requests.get(video_url, headers=settings['DEFAULT_REQUEST_HEADERS'])
                response_json = json.loads(response_video.text)
                video_list = response_json['videos']['list']
                for video in video_list:
                    if video['id'] == video_id:
                        video_map_list.append(video['source'])
            except Exception as e:
                print('get video error', e)

        news_item = News024NaverComItem()
        news_item['title'] = title
        news_item['site'] = 'https://news.naver.com/'
        news_item['author'] = author
        news_item['source_url'] = response.url
        news_item['pictures'] = ','.join(img_list)
        news_item['videos'] = ','.join(video_map_list)
        news_item['pubtime'] = convert_to_east_eight(publish_time)
        news_item['source_content'] = new_html
        news_item['content'] = content
        news_item['category'] = ''
        news_item['country'] = '韩国'
        news_item['tag'] = ''
        news_item['language'] = 'ko'
        # update_time  采集时间
        news_item['update_time'] = current_timestamp()

        yield news_item


def start():
    cmdline.execute(f'scrapy crawl naver_com'.split())


if __name__ == '__main__':
    start()
