import re
from .common import  COMMON_HEADERS
from lib import requests
from lib.logger import logger
from bs4 import BeautifulSoup
async def request_detail(link:str,cookie: str) -> tuple[list, int]: 
    headers = {'cookie': cookie}
    headers.update(COMMON_HEADERS)
    try:
      logger.info(f'request url: {link}')
      resp = await requests.get(link, headers=headers)
      logger.info(f'response url: {link}, body: {resp.text}')
      ret = await parse_detail_html(resp.text,headers)
      return ret
    except Exception as e:
        logger.error(f"failed to request {link}, error: {e}")
        return []
  
async def parse_detail_html(html,headers) -> tuple[list]:
    soup = BeautifulSoup(html, "html.parser")
    datalist = []
    
    # 获取页面配置属性
    page_config  = soup.head.find("script",charset='gbk').text.replace("\n", '').replace("\t", '').replace('\\\'','\'')

    # 查找展示图
    spec_list=soup.find('div',id="spec-list").find_all('li')
    main_img_list = []
    for item in spec_list:
      main_img_list.append(item.find('img')['src'].replace('n5','n0'))
    
    #获取详情图
    
    desc_url = re.search(r"desc: '(.*?)'",page_config).group(1)
    
    try:
      resp = await requests.get('https:' + desc_url,headers=headers)
      # 两种详情图解析方式
      detail_img_list.append(re.findall(r'\\"https:(.*?)\\"',resp.text))
      detail_img_list.append( re.findall(r'url\((.*?)\)',resp.text))
    except  Exception as e:
        logger.error(f"failed to request {desc_url}, error: {e}")
        detail_img_list =  []
    
    data = {
      "mainImgList":main_img_list,
      "detailImgList":detail_img_list
    }
    
    datalist.append(data)
    return datalist