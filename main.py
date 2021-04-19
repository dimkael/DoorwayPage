from aiohttp import web
import aiohttp_jinja2
import jinja2
from webparser import get_content


async def index(request):
    context = {'website' : 'New doorway page', 'title': 'Title of new doorway page'}
    response = aiohttp_jinja2.render_template('index.html', request, context)
    return response


async def search_page(request):
    pass


async def key_page(request):
    url_key = request.match_info['url_key']
    print(request)

    text, links = await get_content(url_key)
    key = url_key.replace('+', ' ')

    context = {
        'website' : 'New doorway page',
        'keyword': key.title(),
        'links': links,
        'text': text
    }
    response = aiohttp_jinja2.render_template('page.html', request, context)
    return response


app = web.Application()
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

app.add_routes([web.static('/static', 'static')])
app.add_routes([web.get('/', index)])
app.add_routes([web.post('/search', search_page)])
app.add_routes([web.get('/{url_key}', key_page)])

web.run_app(app, host='127.0.0.1', port=5000)