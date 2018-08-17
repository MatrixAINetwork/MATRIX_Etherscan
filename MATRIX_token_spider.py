import requests
from datetime import datetime
from pyquery import PyQuery as pq
#from threadpool import * just this scripts run so fast in vps, and too fast to get maybe error
requests.adapters.DEFAULT_RETRIES = 5
domain = "https://etherscan.io/"
index_url = domain+"tokens?p=1"
pagenums = pq(index_url)("#ContentPlaceHolder1_divpagingpanel > div:nth-child(2) > p > a:nth-child(5)").attr("href").split("=")
if len(pagenums) == 2:
    pagenums =  int(pagenums[1])
else:
    print("Error!")
    exit()

def get_code(address=""):
    token_url = domain+"/address/%s#code"%address
    print("//spider token_url\t"+token_url+"\n")
    html =  requests.get(url=token_url).text # just pq(token_url) throw timeout error sometime
    html_dom = pq(html)
    token_code = html_dom("pre#editor").html()#.encode("utf8",'ignore')
    print("//parser token_url\t"+token_url+"\n")
    if token_code!=None and token_code!="":
        token_name = html_dom("#ContentPlaceHolder1_tr_tokeninfo > td:nth-child(2) > a").text().replace(" ","_")
        token_Transactions = html_dom("#ContentPlaceHolder1_divSummary > div:nth-child(1) > table  > tr:nth-child(4) > td >span").text()
        token_price = html_dom("#balancelistbtn > span.pull-left").text().split(" ")
        token_price = token_price[1] if len(token_price)==2 else ""
        spider_time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')

        with open("./tokens_code/"+token_name+".sol",'w') as fp:
            fp.write("//token_name\t"+token_name+"\n")
            fp.write("//token_url\t"+token_url+"\n")
            fp.write("//spider_time\t"+spider_time+"\n")
            fp.write("//token_Transactions\t"+token_Transactions+"\n")
            fp.write("//token_price\t"+token_price+"\n\n")
            fp.write(token_code)
            print("write down\n")
        print("//token_name\t"+token_name+"\n")
        print("//spider_time\t"+spider_time+"\n")
        print("//token_Transactions\t"+token_Transactions+"\n")
        print("//token_price\t"+token_price+"\n")
        print("\n"+token_code+"\n")
    



token_lists = []
urls = [index_url.replace("1",str(page)) for page in range(1,pagenums+1)]
for url in urls:
    print(url)
    html = requests.get(url=url,timeout=3).text
    html_dom = pq(html)
    [token_lists.append(pq(a).attr("href").split("/")[-1]) for a in html_dom("td.hidden-xs>a")]

for token_addr in token_lists:
    get_code(token_addr)

print("Finish")



