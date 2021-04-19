from aiohttp import web
import aiohttp_jinja2
import jinja2
from webparser import get_content


async def index(request):
    context = {'website' : 'New doorway page', 'title': 'Title of new doorway page'}
    response = aiohttp_jinja2.render_template('index.html', request, context)
    return response


async def search(request):
    key = ''

    if request.method == 'POST':
        data = await request.post()
        key = data.get('key')
    elif request.method == 'GET':
        url_key = request.match_info['url_key']
        key = url_key.replace('+', ' ')
    else:
        web.Response(text='Error', status=404)

    text, links = await get_content(key)

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
app.add_routes([web.post('/', search)])
app.add_routes([web.get('/{url_key}', search)])

web.run_app(app, host='127.0.0.1', port=5000)