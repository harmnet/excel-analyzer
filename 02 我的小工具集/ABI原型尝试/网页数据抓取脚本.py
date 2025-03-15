import requests
from bs4 import BeautifulSoup
import re
import time
import random
from urllib.parse import urljoin
from fake_useragent import UserAgent

def get_wenlv_links():
    base_url = "http://wglj.changchun.gov.cn/sy_44789/wlsj/index.html"
    
    # 使用随机User-Agent和更多请求头参数
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Referer': 'https://wglj.changchun.gov.cn/',
        'Connection': 'keep-alive'
    }
    
    try:
        # 使用会话保持并设置随机延迟
        with requests.Session() as session:
            print(f"\n尝试请求: {base_url}")
            print(f"使用请求头: {headers}")
            
            # 设置随机请求间隔（0.5-1.5秒）
            time.sleep(random.uniform(0.5, 1.5))
            
            # 增加请求重试机制和超时设置
            response = session.get(base_url, 
                                 headers=headers, 
                                 timeout=(10, 15),
                                 verify=True,  # 启用证书验证
                                 allow_redirects=True)
            
            print(f"实际请求URL: {response.url}")
            print(f"响应状态码: {response.status_code}")
            print("响应头:", response.headers)
            print("响应内容预览:", response.text[:500])  # 打印前500个字符
            
            # 检查响应状态码
            if response.status_code != 200:
                print(f"请求失败，状态码: {response.status_code}")
                return []

            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 打印所有找到的链接用于调试
            print("\n找到的所有链接:")
            for a in soup.find_all('a', href=True):
                print(f"文本: {a.text.strip()} | 链接: {a['href']}")
            
            # 匹配文旅数据相关链接（根据实际页面结构调整正则表达式）
            pattern = re.compile(r'文旅数据.*?\d{4}[-年]\d{1,2}[-月]\d{1,2}日?')  # 更宽松的匹配模式
            links = []
            
            for a in soup.find_all('a', href=True):
                if pattern.search(a.text.strip()):
                    full_url = urljoin(base_url, a['href'])
                    links.append(full_url)
                    
            # 去重处理
            return list(set(links))
            
    except requests.exceptions.RequestException as e:
        print(f"网络请求异常: {str(e)}")
        return []
    except Exception as e:
        print(f"处理异常: {str(e)}")
        return []

if __name__ == "__main__":
    # 增加重试机制
    max_retries = 3
    for attempt in range(max_retries):
        url_list = get_wenlv_links()
        if url_list:
            print("获取到以下有效链接：")
            for url in url_list:
                print(url)
            break
        else:
            print(f"第{attempt+1}次尝试失败，等待重试...")
            time.sleep(2 ** attempt)  # 指数退避策略