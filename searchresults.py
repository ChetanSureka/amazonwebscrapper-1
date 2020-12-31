from selectorlib import Extractor
import requests 
import json 
from time import sleep


def scrape(url):
    # Create an Extractor by reading from the YAML file
    e = Extractor.from_yaml_file('search_results.yml')
    
    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) Chrome/83.0.4103.61 Safari/537.36 AppleWebKit/537.36 (KHTML, like Gecko)',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.in/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    print("Downloading %s"%url)
    r = requests.get(url, headers=headers)
    print(r.status_code)
    
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None
    # Pass the HTML of the page and create 
    return e.extract(r.text)


def alert(mrp, price):
    dis_fl = (((mrp - price)/mrp)*100)
    dis = int(dis_fl)

    if dis > 80:
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
        dis = str(dis)
        content = "Title:" + product['title'] + "\nPrice: ₹" + product['price'] + "\nMRP: " + product["mrp"] + "\nDiscount: {}%".format(dis) + "\nurl:" + product["url"]
        base_url = 'https://api.telegram.org/bot1385005548:AAGxYkP6a0nBcjJRttV0KjJIuu_7fd_ZuyE/sendMessage?chat_id=-1001200925197&text="{}"'.format(content)
        r = requests.get(base_url, headers=headers)
        print("send: {}".format(product['title']))


# Extracting URLs from the search results page
with open("search_results_urls.txt",'r') as urllist, open('urls.txt','w') as outfile, open('data.txt','w') as datafile:
    for url in urllist.read().splitlines():
        data = scrape(url) 
        if data:
            try:
                for product in data['products']:
                    # Writing data into a file
                    product['url'] = "https://amazon.in" + product['url']
                    outfile.write(product['url'])
                    json.dump(product,datafile)
                    datafile.write("\n")
                    outfile.write("\n")
                    # formatting the data for ease
                    price_str, mrp_str = str(product['price']), str(product['mrp'])
                    mrp_en = (mrp_str.encode('ascii', 'ignore')).decode("utf-8")
                    price_str, mrp_en = price_str.replace(',',''), mrp_en.replace(',','')
                    price, mrp = int(price_str), int(mrp_en)
                    # Finding the discount by
                    # passing the values to the function
                    alert(mrp, price)
            except:
                try:
                    for product in data['products']:
                        # Writing data into a file
                        product['url'] = "https://amazon.in" + product['url']
                        outfile.write(product['url'])
                        json.dump(product,datafile)
                        datafile.write("\n")
                        outfile.write("\n")
                        # formatting the data for ease
                        price_str, mrp_str = str(product['price']), str(product['mrp'])
                        mrp_en = (mrp_str.encode('ascii', 'ignore')).decode("utf-8")
                        price_str, mrp_en = price_str.replace(',',''), mrp_en.replace(',','')
                        price, mrp = int(price_str), int(mrp_en)
                        # Finding the discount by
                        # passing the values to the function
                        alert(mrp, price)
                except:
                    #print("\n\nError!!!")
