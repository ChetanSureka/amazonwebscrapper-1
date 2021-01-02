from requests_html import HTMLSession
import requests
from bs4 import BeautifulSoup
# import pandas as pd


s = HTMLSession()
dealslist = []

url_list = []
url_list.append('https://www.amazon.in/s?i=apparel&bbn=17487327031&dc&fs=true&qid=1609512513&ref=sr_nr_i_1')
url_list.append('https://www.amazon.in/s?i=appliances&bbn=17487327031&dc&qid=1609594340&ref=sr_nr_i_21')
url_list.append('https://www.amazon.in/s?i=electronics&bbn=17487327031&dc&qid=1609594340&ref=sr_nr_i_7')
url_list.append('https://www.amazon.in/s?i=computers&bbn=17487327031&dc&qid=1609594340&ref=sr_nr_i_11')
url_list.append('https://www.amazon.in/s?i=todays-deals&rh=n%3A17487327031&fs=true&ref=lp_17487327031_sar')

print(url_list[4])

def alert(msg):
    headers = {'dnt': '1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-user': '?1',
                'sec-fetch-dest': 'document',
                'referer': 'https://www.amazon.in/',
                'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'}
    # base_url = 'https://api.telegram.org/bot1261801205:AAFGQXEgDC1gQlA766jcZvno0rsdoOejCJE/sendMessage?chat_id=-397628494&text="{}"'.format(msg)
    base_url = 'https://api.telegram.org/bot1385005548:AAGxYkP6a0nBcjJRttV0KjJIuu_7fd_ZuyE/sendMessage?chat_id=-1001200925197&text="{}"'.format(msg)
    r = requests.get(base_url, headers=headers)


def getdata(url):
    r = s.get(url)
    # r.html.render(sleep=1)
    if r.status_code != 200:
        alert(str(r.status_code))
    soup = BeautifulSoup(r.html.html, 'html.parser')
    return soup

def discount(mrp,price,title,url):
    dis_fl = (((mrp - price)/mrp)*100)
    dis = int(dis_fl)
    if dis >= 90:
        dis = str(dis)
        content = "Title: " + title + "\nPrice: ₹{}".format(price) + "\nMRP: {}".format(mrp) + "\nDiscount: {}%".format(dis) + "\nurl: https://www.amazon.in" + url
        alert(content)

def getdeals(soup):
    products = soup.find_all('div', {'data-component-type': 's-search-result'})
    for item in products:
        title = item.find('a', {'class': 'a-link-normal a-text-normal'}).text.strip()
        link = item.find('a', {'class': 'a-link-normal a-text-normal'})['href']
        try:
            saleprice = float(item.find_all('span', {'class': 'a-offscreen'})[0].text.replace('₹','').replace(',','').strip())
            oldprice = float(item.find_all('span', {'class': 'a-offscreen'})[1].text.replace('₹','').replace(',','').strip())
        except Exception as e:
            oldprice = float(item.find('span', {'class': 'a-offscreen'}).text.replace('₹','').replace(',','').strip())
            alert(str(e))

        discount(oldprice, saleprice, title, link)
        
        saleitem = {
            'title': title,
            'link': link,
            'saleprice': saleprice,
            'oldprice': oldprice,
            }
        dealslist.append(saleitem)
    return

def getnextpage(soup): 
    pages = soup.find('ul', {'class': 'a-pagination'})   
    if not pages.find('li', {'class': 'a-disabled a-last'}):
        url = 'https://www.amazon.in' + str(pages.find('li', {'class': 'a-last'}).find('a')['href'])
        return url
    else:
        return

url = url_list[4]
alert("Starting Web scraping...\n\nScrapping: {}".format(url))
run = True
while run:
    soup = getdata(url)
    getdeals(soup)
    url = getnextpage(soup)
    if not url:
        run = False
    else:
        print(url)
        print(len(dealslist))
        if len(dealslist) == 1000:
            msg = "Found 1000 products currently on \n{}".format(url)
            alert(msg)
        elif len(dealslist) == 2000:
            msg = "Found 2000 products currently on \n{}".format(url)
            alert(msg)
            run = False
        else:
            alert("{} Products completed".format(len(dealslist)))

# df = pd.DataFrame(dealslist)
# df['percentoff'] = 100 - ((df.saleprice / df.oldprice) * 100)
# df = df.sort_values(by=['percentoff'], ascending=False)
# df.to_csv('deals-bfdeals.csv', index=False)
alert("Completed scraping...")
print('Fin.')
