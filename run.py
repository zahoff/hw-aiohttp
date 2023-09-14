from aiohttp import web
from models import db_context
from views import AdvertisementView


app = web.Application()

app.router.add_routes([
    web.get('/advertisements/', AdvertisementView),
    web.post('/advertisements/', AdvertisementView),
    web.patch('/advertisements/{ad_id}', AdvertisementView),
    web.delete('/advertisements/{ad_id}', AdvertisementView)
])

app.cleanup_ctx.append(db_context)

web.run_app(app)