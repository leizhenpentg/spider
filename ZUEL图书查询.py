import requests
import re
import  json
import csv
from pyquery import PyQuery as pq


def get_one_page(url,want,num):
    header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'}
    data={'str':want,
          'pagesize':'10',
          'pageidx':num,
          'opt':'2',
          'grp':'02'
    }
    session=requests.session()
    response=session.post(url,data=data,headers=header)
    if response.status_code==200:
        return response.text
    return  None





def parse_one_page(html):
    pattern=re.compile('"REFCODE":(.*?),"C200A":"(.*?)","SEARCHCODES":"(.*?)",.*?"C210CD":"(.*?)",')
    items=re.findall(pattern,html)
    for item in items:
        item=list(item)
        kk=item[0]
        URL='http://202.114.238.250/Mobile/sjxq?refcode='+kk
        doc=pq(url=URL)
        print(URL)
        listt=doc('.bcont_box .collection .li_right')
        place1=listt.find('li:nth-child(4)').text()
        place2=re.sub('\d*:','',place1)
        place3=place2.split(' ')
        state=listt.find('li:nth-child(6)').text()
        state2=state.split(' ')
        kk={}
        for i in range(1,len(state2)):
            kk[place3[i]]=state2[i]
        item.append(str(kk))
        item[0]=URL
        write_to_csv(item)


# def wreit_to_file(content):
#     with open ('搜索结果.txt','a',encoding='utf-8') as f:
#         f.write(json.dumps(content,ensure_ascii=False)+'\n')


def write_to_csv(item):
    with open('亲，你的书单到了.csv','a',newline='') as csvfile:
        writer=csv.writer(csvfile)
        writer.writerow(item)


def main(num,want):
    url='http://202.114.238.250/Mobile/jdjs'
    html=get_one_page(url,want,num)
    items=parse_one_page(html)


if __name__ == '__main__':
    want = input('你要搜索啥？\n')
    with open('亲，你的书单到了.csv','a',newline='') as csvfile:
        writer=csv.writer(csvfile)
        writer.writerow(['你搜啥？',want])
        writer.writerow(['传送门昂','书叫啥名呢？','去图书馆找找？','出版社','哪里找呀'])
    for num in range(1,10):
        main(num,want)


