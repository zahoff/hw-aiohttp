import aiohttp_sqlalchemy as ahsa

from aiohttp import web
from datetime import datetime

from sqlalchemy import select, update
from models import Advertisement


class AdvertisementView(web.View, ahsa.SAMixin):

    async def get(self):
        response = []

        db_session = self.get_sa_session()
        result = await db_session.execute(select(Advertisement))
        result = result.fetchall()

        for ad in result:
            ad = ad[0]
            response.append({
                'id': ad.id,
                'title': ad.title,
                'description': ad.description,
                'user_id': ad.user_id,
                'created_at': ad.created_at.strftime('%m/%d/%Y, %H:%M:%S')
            })

        return web.json_response(response)

    async def delete(self):
        ad_id = self.request.match_info['ad_id']
        db_session = self.get_sa_session()

        ad = await db_session.execute(
            select(Advertisement).where(Advertisement.id == ad_id)
        )
        ad = ad.fetchone()

        if not ad:
            return web.json_response({'error': 'Not found'})

        ad = ad[0]

        await db_session.delete(ad)
        await db_session.commit()

        return web.json_response({
            'status': 'ok',
            'ad_id': ad_id
        })

    async def patch(self):
        ad_id = self.request.match_info['ad_id']
        db_session = self.get_sa_session()

        ad = await db_session.execute(
            select(Advertisement).where(Advertisement.id == ad_id)
        )
        ad = ad.fetchone()

        if not ad:
            return web.json_response({'error': 'Not found'})

        ad = ad[0]

        ad_data = await self.request.json()
        statement = update(Advertisement).where(Advertisement.id == ad.id).values(**ad_data)

        await db_session.execute(statement)
        await db_session.commit()
        await db_session.refresh(ad)

        return web.json_response({
            'id': ad.id,
            'title': ad.title,
            'description': ad.description,
            'user_id': ad.user_id,
            'created_at': ad.created_at.strftime('%m/%d/%Y, %H:%M:%S')
        })

    async def post(self):
        ad_data = await self.request.json()
        db_session = self.get_sa_session()

        ad_data['created_at'] = datetime.now()

        ad = Advertisement(**ad_data)
        db_session.add(ad)

        await db_session.commit()
        await db_session.refresh(ad)

        return web.json_response({
            'id': ad.id,
            'title': ad.title,
            'description': ad.description,
            'user_id': ad.user_id,
            'created_at': ad.created_at.strftime('%m/%d/%Y, %H:%M:%S')
        })
