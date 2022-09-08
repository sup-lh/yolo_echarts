
import asyncio
import websockets
import threading
from spark import OutputPower

# 存储所有的客户端
Clients = []

class Server():
    ##***************************************发送消息****************************************************##
    # 发送消息
    async def sendMsg(self,msg,websocket):
        print('sendMsg:',msg)
        if websocket != None:
            await websocket.send(msg)
        else:
            await self.broadcastMsg(msg)
        # 避免被卡线程
        await asyncio.sleep(0.2)
	# 群发消息
    async def broadcastMsg(self,msg):
        for user in Clients:
            await user.send(msg)

    ##***************************************回调函数****************************************************##
	# 发消息给客户端的回调函数
    async def s(self,msg,websocket=None):
        await self.sendMsg(msg,websocket)
    # 针对不同的信息进行请求，可以考虑json文本
    async def runCase(self,websocket):
        op = OutputPower()
        await op.run(self.s,websocket)

    ##****************************************主程序****************************************************##
    # 每一个客户端链接上来就会进一个循环
    async def echo(self,websocket, path):
        Clients.append(websocket)
        while True:
            try:
                recv_text = await websocket.recv()
                message = "I got your message: {}".format(recv_text)
                # 直接返回客户端收到的信息
                # await websocket.send(message)
                print(message)

                # 分析当前的消息 json格式，跳进功能模块分析
                await self.runCase(websocket=websocket)

            except websockets.ConnectionClosed:
                print("ConnectionClosed...", path)  # 链接断开
                Clients.remove(websocket)
                break
            except websockets.InvalidState:
                print("InvalidState...")  # 无效状态
                Clients.remove(websocket)
                break
            except Exception as e:
                print(e)
                Clients.remove(websocket)
                break

    ##*************************************启动多线程服务****************************************************##
    # 启动服务器
    async def runServer(self):
        async with websockets.serve(self.echo, 'localhost', 8765):
            await asyncio.Future()  # run forever

    def WebSocketServer(self):
        asyncio.run(self.runServer())

    def startServer(self):
        thread = threading.Thread(target=self.WebSocketServer)
        thread.start()
        thread.join()
    

    ##*************************************main函数****************************************************##
if __name__=='__main__':
    s = Server()
    s.startServer()

