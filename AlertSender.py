# Sends an alert on telegram when a product is 90%
# This function sends the alert to the telegram group
def send_msg(content):
    headers = {'dnt': '1',
               'upgrade-insecure-requests': '1',
               'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
               'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
               'sec-fetch-site': 'same-origin',
               'sec-fetch-mode': 'navigate',
               'sec-fetch-user': '?1',
               'sec-fetch-dest': 'document',
               'referer': 'https://www.amazon.com/',
               'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'}
    base_url = 'https://api.telegram.org/bot1385005548:AAGxYkP6a0nBcjJRttV0KjJIuu_7fd_ZuyE/sendMessage?chat_id=-1001200925197&text="{}"'.format(content)
    r = requests.get(base_url, headers=headers)

# Generates the content for sending the message
with open("output.json",'r') as infile:
    file_data = json.load(infile)
    for data in file_data['extract']:
        price_1, mrp_1, deal = str(data['price']), str(data['mrp']), str(data['deal'])
        price_1 = price_1.replace(',','')
        mrp_1 = mrp_1.replace(',','')
        deal = deal.replace(',','')
        if mrp_1 == 'None':
            mrp_1 = '0'
        if price_1 == 'None':
            price_1 = '0'
        if deal == 'None':
            deal = '0'
        price_en = (price_1.encode('ascii', 'ignore')).decode("utf-8")
        mrp_en = (mrp_1.encode('ascii', 'ignore')).decode("utf-8")
        deal_en = (deal.encode('ascii', 'ignore')).decode("utf-8")
        price = float(price_en)
        mrp = float(mrp_en)
        deal = float(deal_en)
        print(price,mrp,deal)
        try:
            discount = int(((price-mrp)/mrp)*100)
            dis = str(discount)
            if discount > 90:
                content = "Title: " + data['name'] + "\nMRP: " + mrp_en + "\nPrice: " + price_en + "\nUrl: " + data['url']
                try:
                    send_msg(content)
                    print("SEND...")
                except Exception as e:
                    print("An Error occurred !!!",e)
            deal_dis = int(((deal-mrp)/mrp)*100)
            deal_disc = str(deal_dis)
            content = "Amazing Deal that YOU must not miss\nTitle: " + data['name'] + "\nMRP: " + mrp_en + "\nDeal Price: " + deal_disc + "\nUrl: " + data['url']
            try:
                send_msg(content)
                print("SEND...")
            except Exception as e:
                print("An Error occurred !!!",e)                
        except Exception as e:
            print("An Error occurred !!!",e)
