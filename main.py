from aiohttp import web
import aiohttp_jinja2
import jinja2


async def index(request):
    context = {}
    response = aiohttp_jinja2.render_template('index.html', request, context)
    return response


app = web.Application()
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

app.add_routes([web.get('/', index)])
app.add_routes([web.static('/static', 'static')])

web.run_app(app, host='127.0.0.1', port=5000)