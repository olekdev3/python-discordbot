from requests_html import HTMLSession

session = HTMLSession()
counter = 0 
for x in range(0, 50000):
    url = f'https://myanimelist.net/anime/{x}'
    response = session.get(url)
    if response.status_code == 200:
        counter = counter + 1
    print(f'Code: {response.status_code} | Anime Counted: {counter}')