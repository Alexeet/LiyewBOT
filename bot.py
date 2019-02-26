import discord
import asyncio
import logging
import commands
import sys


_MASTERS_IDS_ = ["217982938703331328"]

class Bot(discord.Client):

    async def on_ready(self):
        print("Logged on as {}!".format(self.user))
        self.pending_commands = {}
    
    async def on_message(self,message):
        await self.command_handler.processMessage(message)

    async def init(self):
        self.command_handler = commands.CommandHandler(self)
        await self.command_handler.loadConfig()
        await self.command_handler.loadModulesFromConfig()
    
    async def list_members(self, username, server):
        if(server == None):
            return
        
        member_list = []

        for i in server.members:
            if((i.name==username) or (i.nick==username) or (i.id==username) or (str(i)==username) or (i.discriminator==username)):
                member_list.append(i)
        
        return member_list


def help():
    print("python bot.py {client token} [...]")

if __name__ == "__main__":
    token = ""
    if(len(sys.argv) <= 1):
        try:
            with open("client.token") as token_f:
                token = token_f.read().replace("\n","")
        except:
            help()
    else:
        token = sys.argv[1]
    
    if(len(token) != 59):
        print("Invalid client token !!")
    
    client = Bot()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(client.init())
    client.run(token)