#!/usr/bin/env python
# encoding: utf-8
import sys
sys.path.append('./joycontrol/');

from joycontrol.controller import Controller
from joycontrol.server import create_hid_server
from joycontrol.protocol import controller_protocol_factory
from aiohttp import web, WSMsgType
import os.path

async def handle(request):
    text = '<meta http-equiv="refresh" content="0;url=./static/index.html">'


async def websocket_handler(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                await ws.send_str(msg.data + '/answer')
        elif msg.type == WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')
    return ws

app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/ws', websocket_handler)])
app.router.add_static('/static/',
                      path='static',
                      name='static')

if __name__ == '__main__':
    web.run_app(app, port=5000)
