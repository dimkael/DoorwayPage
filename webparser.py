from aiohttp import ClientSession
from lxml import html

MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"

async def get_content(key):
    headers = {
        'User-Agent': '''Mozilla/5.0 (Windows NT 10.0; Win64; x64)
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.86 
        YaBrowser/21.3.1.185 Yowser/2.5 Safari/537.36'''
    }

    url = f'https://scholar.google.ru/scholar?q={key}'

    async with ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            html_code = await resp.text()
        html_code = html_code.replace('<b>', '')
        html_code = html_code.replace('</b>', '')

        dom_tree = html.fromstring(html_code)

        links_text = dom_tree.xpath('//h3[@class="gs_rt"]/a/text()')
        links_url = dom_tree.xpath('//h3[@class="gs_rt"]/a/@href')

        links = dict(zip(links_text, links_url))
        text = ''.join(dom_tree.xpath('//div[@class="gs_rs"]/text()'))

    return text, links