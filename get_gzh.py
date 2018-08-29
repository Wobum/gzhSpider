#coding = utf-8

import requests
from fake_useragent import UserAgent 
from lxml import etree
import re

def get_html_text(url):
    '''获得目标网页的text属性
    
    Parametre ：
    -----------
    url ： str
        目标网页的url

    Returns :
    ---------
    目标网页的text属性（str）

    '''
    ua = UserAgent()
    headers = {'User-Agent':ua.random}

    try:
        html = requests.get(url,timeout = 10,headers = headers)
        html.encoding = html.apparent_encoding
        return html.text

    except:
        print('连接网页失败\n')
        print('未知错误，url：',url)
        return None


def _search_gzh(name,page = 1):
    
    url = 'http://weixin.sogou.com/weixin?query='+name+'&_sug_type_=&s_from=input&_sug_=n&type=1&page='+str(page)+'&ie=utf8'
    text = get_html_text(url)
    if text != None:
        return text
    else:
        return False

def get_elem_text(elem):
    ''' 获取element元素中的文字
    
    Parameters:
    ----------
        elem : lxml中的element元素

    Returns：
    --------
        str ： 文字内容

    '''
    rc = list()
    for node in elem.itertext():
        rc.append(node.strip())

    return ''.join(rc)


def get_gzh_info(name,page = 1):
    '''通过名字搜索公众号
    
    Parameters :
    -----------
    name : str
        公众号名字

    page ： int
        访问该公众号搜素结果的第几页

    Returns ：
    ---------
    list[dict]
        {
            'name':'' 微信号名字
            'wechatid': '' 微信号唯一ID
            'jieshao': '' 微信号功能介绍
            'qrocde': '' 微信号二维码连接
            'img_url':'' 微信号头像链接
            'gzh_url':'' 微信号链接
            'latest_article_name': '' 微信号最近一篇文章的名字
            'latest_article_url': '' 微信号最近一篇文章的链接
        }


    '''
    img_url = list()
    gzh_url = list()
    gzh_name = list()
    wechatid = list()
    qrcode = list()
    jieshao = list()
    latest_article_name = list()
    latest_article_url = list()
    renzhen = list()

    text = _search_gzh(name , page)
    dom_tree = etree.HTML(text)

    interesting_info = dom_tree.xpath(u'//ul[@class = "news-list2"]')
    for li in interesting_info:        
        info_img = li.xpath(u'//div[@class = "img-box"]/a/img')
        for url  in info_img:
            img_url.append(url.attrib['src'])

        info_gzh= li.xpath(u'//div[@class = "img-box"]/a')
        for url in info_gzh:
            gzh_url.append(url.attrib['href'])

        info_name = li.xpath(u'//div[@class = "txt-box"]/p[1]/a')
        for info in info_name:
            cache_name = get_elem_text(info)
            cache_name = cache_name.replace('red_beg','')
            cache_name = cache_name.replace('red_end','')
            gzh_name.append(cache_name)

        info_wechtid = li.xpath(u'//div[@class = "txt-box"]/p[2]')
        for info in info_wechtid:
            cache_wechatid = get_elem_text(info)
            cache_list = cache_wechatid.split('微信号：')
            wechatid.append(cache_list[1])

        info_qrcode = li.xpath(u'//div[@class = "ew-pop"]/span/img[1]/@src')
        for info in info_qrcode:
            qrcode.append(info)
        
        info_jieshao = li.xpath(u'//li/dl[1]/dd')
        for info in info_jieshao:
            s = etree.tostring(info,encoding = 'unicode')
            s = re.sub(r'<dd>|<em>|<!--red_beg-->|<!--red_end-->|</em>|</dd>','',s).strip()
            jieshao.append(s)

        info_latest_article_name = li.xpath(u'//dl[2]/dd/a/text()')
        for info in info_latest_article_name:
            latest_article_name.append(info)

        info_latest_article_url = li.xpath(u'//dl[2]/dd/a/@href')
        for info in info_latest_article_url:
            latest_article_url.append(info)


    returns = list()
    for i in range(len(gzh_name)):
        returns.append(
            {'name':gzh_name[i],
             'wechatid':wechatid[i],
             'jieshao':jieshao[i],
             'qrocde':qrcode[i],
             'img_url':img_url[i],
             'gzh_url':gzh_url[i]，
             'latest_article_name':latest_article_name[i],
             'latest_article_url':latest_article_url[i]

            }
        )
    return returns  

def get_gzh_article(wechatid):
    '''用于获取公众号最新的十篇文章(PS:还未完成)

    '''
    item = get_gzh_info(wechatid)
    url = item['gzh_url']
    text = get_html_text(url)


if __name__ == '__main__':
    name = input('输入公众号的名称：')
    a = get_gzh_info(name)
    print(a)
