import requests

url = 'http://www.cuaa.net/cur/2019/2019dxpm.shtml'
headers ={
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
    'Cookie': 'AJSTAT_ok_times=1; JSESSIONID=asfFwRYASRH4; bdshare_firstime=1587547598006; AJSTAT_ok_pages=3'
}
rsp = requests.get(url=url,headers=headers)
rsp.encoding='GB2312'
print(rsp.text)