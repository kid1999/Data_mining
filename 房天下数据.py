import requests
from bs4 import BeautifulSoup

def getInfo(url):
    
    dict = {}
    res = requests.get(url)
    soup = BeautifulSoup(res.text,'html.parser')

    title = soup.select('h1')
    dict['标题'] = title[0].text.strip()

    try:
        title = soup.select('.trl-item.price_esf.sty1')
        dict['总价'] = title[0].text
        title = soup.select('.fyms_con.floatl.gray3')
        dict['买点'] = title[0].text
    except:
        pass

    title = soup.select('.tt')
    dict['户型'] =title[0].text.strip()
    dict['建筑面积'] =title[1].text.strip()
    dict['单价'] =title[2].text.strip()
    dict['朝向'] =title[3].text.strip()
    dict['楼层'] =title[4].text.strip()
    dict['装修'] =title[5].text.strip()

    
    title = soup.select('.rcont a')
    dict['小区'] = title[0].text
    dict['区域'] = title[2].text.strip() + ' '+ title[3].text.strip()

    title = soup.select('.zf_jjname')
    dict['中介'] = title[0].text

    title = soup.select('#mobilecode')
    dict['中介电话'] = title[0].text

    title = soup.select('.cont.clearfix')
    str = title[0].text.split()
    try:
        dict[str[0]] = str[1]
        dict[str[2]] = str[3]
        dict[str[4]] = str[5]
        dict[str[6]] = str[7]
        dict[str[8]] = str[9]
        dict[str[10]] = str[11]
        dict[str[12]] = str[13]
    except:
        pass
    return dict


#运行程序
res = requests.get("http://sz.esf.fang.com/")
soup = BeautifulSoup(res.text,'html.parser')

houses= []
for house in soup.select('dd .clearfix a'):
#     print(house)
    print(house['title'])
    url = 'http://sz.esf.fang.com/'+house['href']
    print(url)
    houses.append(getInfo(url))

print(houses)

