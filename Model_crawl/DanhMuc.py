# thư viện requests đọc dữ liệu khi crawl về
from math import fabs
import string
import requests
import random
from datetime import date
from datetime import datetime
# jsson chuyển file lấy từ web về đọc dữ liệu
import json
import time
from bs4 import BeautifulSoup
#url = 'https://shopee.vn/api/v4/recommend/recommend?bundle=daily_discover_main&item_card=9&limit=60&offset=0'
from threading import Thread
import ray
from sqlalchemy import false
ray.init()
from multiprocessing import Process
from threading import Thread, Lock
import random
proxy = ""

def getListProxy():
    page = requests.get("https://www.proxynova.com/proxy-server-list/")
    soup = BeautifulSoup(page.text, 'html.parser')
    data = soup.find_all(align="left")

    host = str(soup)
    listHost = []
    while(True):
        try:
            if host.find("document.write(") == -1 : break

            host = host[host.find("document.write(")+5:]
            hostTemp = host[host.find('(') + 1:host.find(')')]

            if hostTemp.find("'\'") != -1: break

            hostTemp = hostTemp.replace("'","")
            hostTemp = hostTemp.replace("+" ,"")
            hostTemp = hostTemp.replace(" ", "")
            listHost.append(hostTemp)
        except: break

    listPort = []
    for item in data:
        try:
            port = int(str(item.text).strip())
            listPort.append(port)
        except: continue

    output = []
    for index in range(0, len(listHost)):
        try:
            ip = listHost[index] + ":" + str(listPort[index])
            proxy = {"http":"http://"+ip,"https":"http://"+ip}
            proxy = {"http":"http://"+ip}
            output.append(proxy)
        except: break
    
    return output

def proxyTrue():
     # Lấy danh sách proxy
    print("Đang kiểm tra proxy...")
    proxys = getListProxy()
    proxySelect = proxys[0]
    while(True):
        try:
            response = requests.get("https://shopee.vn/api/v4/search/search_items?by=sales&limit=60&match_id=11035567&newest=0&order=desc&page_type=search&scenario=PAGE_OTHERS&version=2", headers={'User-Agent': 'Mozilla/5.0'}, proxies=proxySelect)
            print("proxy :" + str(proxySelect) + " Có thể sử dụng")
            return proxySelect
        except:
            proxys.remove(proxySelect)
             # Không có proxy nào hợp lệ thì return
            if len(proxys) == 0:
                return None

            proxySelect = random.choice(proxys)
            print("Số lượng proxy còn lại: " + str(len(proxys)))
            print("proxy :" + str(proxySelect) + " Lỗi")
            continue





@ray.remote
def crawldanhmucbanchay(match_id):
    # proxy = proxyTrue()
    
    listProxy = []
    proxy = {
            'http' : 'http://101.99.31.69',
            'https' : 'http://101.99.31.69'
        }
    listProxy.append(proxy)
    TongDoanhThuBanChay =0;
    page =0;
    j =0
    lens =0;
    while(page<=60):
        url="https://shopee.vn/api/v4/search/search_items?by=sales&limit=60&match_id={}&newest={}&order=desc&page_type=search&scenario=PAGE_OTHERS&version=2".format(match_id,page)
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0', 
             'Cookie': 'REC_T_ID=9c41a161-5cb6-11ec-902c-9ebae1e75c37; SPC_EC=-; SPC_F=5W9vh3yOqmtUrgJTWnEgjcCk3xj0LRmV; SPC_IA=-1; SPC_R_T_ID=FIiUw7tWvbbAFA2gykhU2fvoAsNCrc1NKMJovEgrQb2OPIMOSd8fe2x2NBcYWy5VqwtoCA2yzPBzOpeJvRkOWxyq7oyOH1l/Pl2KKntkDh0=; SPC_R_T_IV=IMe6x9jGrozefHEBqUUt+g==; SPC_SI=bfftocsg9.j0NNRqciy3pXIQuybzSscugSLXauGAbS; SPC_T_ID=FIiUw7tWvbbAFA2gykhU2fvoAsNCrc1NKMJovEgrQb2OPIMOSd8fe2x2NBcYWy5VqwtoCA2yzPBzOpeJvRkOWxyq7oyOH1l/Pl2KKntkDh0=; SPC_T_IV=IMe6x9jGrozefHEBqUUt+g==; SPC_U=-' 
        }    
        response_X = requests.request("GET", url,headers=headers)
        time.sleep(1.5)
       
        if(response_X.status_code == 200):     
            data = response_X.json()
            try:
                lens = (len(data["items"]))
             
                for j in  range(lens):
                    price = (data["items"][j]["item_basic"]["price_max"]/100000);
                    sold_s = data["items"][j]["item_basic"]["sold"]
                    TongDoanhThuBanChay = TongDoanhThuBanChay+(price*sold_s);
                print("TongDoanhThuBanChay", TongDoanhThuBanChay)
                j = 0
            except:
                return TongDoanhThuBanChay
        else:
            return  None
        page = page+ 60
      
    return TongDoanhThuBanChay

@ray.remote
def crawldanhmucphobien(match_id):
    TongDoanhThuPhoBien = 0;
    page =0;
    j =0
   
    while(page<=60):
        url=" https://shopee.vn/api/v4/search/search_items?by=pop&limit=60&match_id={}&newest={}&order=desc&page_type=search&scenario=PAGE_OTHERS&version=2".format(match_id,page)
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': '',
             'Cookie': 'REC_T_ID=9c41a161-5cb6-11ec-902c-9ebae1e75c37; SPC_EC=-; SPC_F=5W9vh3yOqmtUrgJTWnEgjcCk3xj0LRmV; SPC_IA=-1; SPC_R_T_ID=FIiUw7tWvbbAFA2gykhU2fvoAsNCrc1NKMJovEgrQb2OPIMOSd8fe2x2NBcYWy5VqwtoCA2yzPBzOpeJvRkOWxyq7oyOH1l/Pl2KKntkDh0=; SPC_R_T_IV=IMe6x9jGrozefHEBqUUt+g==; SPC_SI=bfftocsg9.j0NNRqciy3pXIQuybzSscugSLXauGAbS; SPC_T_ID=FIiUw7tWvbbAFA2gykhU2fvoAsNCrc1NKMJovEgrQb2OPIMOSd8fe2x2NBcYWy5VqwtoCA2yzPBzOpeJvRkOWxyq7oyOH1l/Pl2KKntkDh0=; SPC_T_IV=IMe6x9jGrozefHEBqUUt+g==; SPC_U=-'
        }    
        response_X = requests.request("GET", url,headers=headers, proxies=proxy)
        time.sleep(1.5)
        if(response_X.status_code == 200):     
            data = response_X.json();
            try:
                lens = (len(data["items"]))
                for j in  range(lens):
                    price = (data["items"][j]["item_basic"]["price_max"]/100000);
                    sold_s = data["items"][j]["item_basic"]["sold"]
                    TongDoanhThuPhoBien = TongDoanhThuPhoBien + (price*sold_s);
                    j = j + 1
                print("DoanhThuPhobien", TongDoanhThuPhoBien)
                j = 0
            except:
                return TongDoanhThuPhoBien
        else:
            return  None

        page = page + 60
      
    return TongDoanhThuPhoBien

@ray.remote
def crawldanhmucmoinhat(match_id):
    page =0;
    j =0
    TongDoanhThuMoiNhat =0;
    while(page<=60):
        url=" https://shopee.vn/api/v4/search/search_items?by=ctime&limit=60&match_id={}&newest={}&order=desc&page_type=search&scenario=PAGE_OTHERS&version=2".format(match_id,page)
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': '',
             'Cookie': 'REC_T_ID=9c41a161-5cb6-11ec-902c-9ebae1e75c37; SPC_EC=-; SPC_F=5W9vh3yOqmtUrgJTWnEgjcCk3xj0LRmV; SPC_IA=-1; SPC_R_T_ID=FIiUw7tWvbbAFA2gykhU2fvoAsNCrc1NKMJovEgrQb2OPIMOSd8fe2x2NBcYWy5VqwtoCA2yzPBzOpeJvRkOWxyq7oyOH1l/Pl2KKntkDh0=; SPC_R_T_IV=IMe6x9jGrozefHEBqUUt+g==; SPC_SI=bfftocsg9.j0NNRqciy3pXIQuybzSscugSLXauGAbS; SPC_T_ID=FIiUw7tWvbbAFA2gykhU2fvoAsNCrc1NKMJovEgrQb2OPIMOSd8fe2x2NBcYWy5VqwtoCA2yzPBzOpeJvRkOWxyq7oyOH1l/Pl2KKntkDh0=; SPC_T_IV=IMe6x9jGrozefHEBqUUt+g==; SPC_U=-'
        }    
        response_X = requests.request("GET", url,headers=headers, proxies=proxy)
        time.sleep(1.5)
        if(response_X.status_code == 200):     
            data = response_X.json();
            try:
                lens = (len(data["items"]))
                for j in  range(lens):
                    price = (data["items"][j]["item_basic"]["price_max"]/100000);
                    sold_s = data["items"][j]["item_basic"]["sold"]
                    TongDoanhThuMoiNhat = TongDoanhThuMoiNhat + (price*sold_s);
                    j = j + 1
                print("DoanhThuMoiNhat", TongDoanhThuMoiNhat)
                j = 0
            except:
                return TongDoanhThuMoiNhat
        else:
            return  None

                        
        
        
        page = page+ 60
    
    return TongDoanhThuMoiNhat

def crawlalldanhmuc(match_id):
    # TongDoanhThuBanChays=crawldanhmucbanchay(11035567);
    # TongDoanhThuPhoBiens=crawldanhmucphobien(11035567);
    # TongDoanhThuMoiNhats=crawldanhmucmoinhat(11035567)
    # data1 = ""
   
    now = datetime.now()
    dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
    data1s = crawldanhmucbanchay.remote(match_id);
    data2s = crawldanhmucphobien.remote(match_id);
    data3s = crawldanhmucmoinhat.remote(match_id); 
    data1,data2,data3= ray.get([data1s,data2s,data3s])

    # aDict = {
    #     "BanChay":TongDoanhThuBanChays,
    #     "PhoBien":TongDoanhThuPhoBiens,
    #     "MoiNhat":TongDoanhThuMoiNhats,
    # }
    aDict = {
        "BanChay":data1,
        "PhoBien":data2,
        "MoiNhat":data3,
        "timeupdate":dt_string,
    }
    if(data3 != ""):
        ray.shutdown()
  
    
        
    return aDict



#print(crawlalldanhmuc(11035567))
# print(crawldanhmucbanchay(11035567))

