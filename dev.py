import asyncio

class Dev:

    def __init__(self,client):
        self.command_list = ["startloop","queryloop","exitloop"]
        self.client = client
        self.loop = True

    async def call(self, cmdname, args, message):
        if(cmdname not in self.command_list):
            return
        if(cmdname == "startloop"):
            asyncio.ensure_future(self.startloop(message.channel))
        elif(cmdname == "queryloop"):
            await self.queryloop(message.channel)
        elif(cmdname == "exitloop"):
            await self.exitloop()
    
    async def startloop(self, channel):
        self.loop = True
        while(self.loop):
            await asyncio.sleep(1)
        await self.client.send_message(channel, "Loop exited")
    
    async def queryloop(self, channel):
        await self.client.send_message(channel, "Loop is {}active".format("" if self.loop else "in"))
    
    async def exitloop(self):
        self.loop = False

def init(client):
    return Dev(client)

if __name__ == "__main__":
    print("This is a bot module")
    print("Add this module to your bot config.cfg file")