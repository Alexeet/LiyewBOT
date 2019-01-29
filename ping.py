
class Ping:

    def __init__(self,client):
        self.command_list = ["ping"]
        self.client = client

    async def call(self, cmdname, args, message):
        if(cmdname not in self.command_list):
            return
        if(cmdname == "ping"):
            await self.client.send_message(message.channel, "pong!")

def init(client):
    return Ping(client)

if __name__ == "__main__":
    print("This is a bot module")
    print("Add this module to your bot config.cfg file")