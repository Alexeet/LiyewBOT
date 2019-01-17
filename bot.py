import discord
import asyncio
import logging
import sys

class Bot(discord.Client):
    async def on_ready(self):
        print("Logged on as {}!".format(self.user))

    async def is_for_me(self, message):
        return message.content.startswith("./") and (message.author != self.user) 


    async def on_message(self, message):
        if(await self.is_for_me(message)):
            print("{}@{}:\'{}\'".format(message.author.name, message.server.name, message.content))
            await self.process_message(message)
    

    async def process_message(self, message):
        args = message.content.split(" ")
        args[0] = args[0][2:]   #Removing prefix
        if(args[0] == "ping"):
            print("ping")
            await self.send_message(message.channel, "pong!")
        elif(args[0] == "pong"):
            await self.send_message(message.channel, "ping!")
        elif(args[0] == "kick"):
            await self.kick_cmd(args, message)
    

    async def kick_cmd(self, args, message):
        if(len(args) <=1 or message.server == None):
            await self.send_message(message.channel, "./kick_cmd (user) [-f(orce)]")
            return
        
        user_to_kick = await self.find_user(args[1], message.server)

        if(user_to_kick == None):
            await self.send_message(message.channel, "Could not find user {}.".format(args[1]))
            return
        
        if("-f" not in args[2:] and user_to_kick == message.author):
            await self.send_message(message.channel, "You can't kick yourself ! To bypass this restriction, use `-f` flag")
            return
        
        #Creating ghost channel
        try:
            newchan = await self.create_channel(message.server, "Mexican border", type=discord.ChannelType.voice)
        except discord.errors.Forbidden:
            await self.send_message(message.channel, "Missing permission : [discord.manage_channels]")
            return
        #Moving user
        try:
            await self.move_member(user_to_kick, newchan)
        except discord.errors.Forbidden:
            await self.send_message(message.channel, "Missing permission : [discord.move_member]")
            await self.delete_channel(newchan)
            return
        #Cleaning up
        await self.delete_channel(newchan)

    
    async def find_user(self, username, server):
        if(username == "" or server == None):
            return None
        for member in server.members:
            if(member.nick == username or member.name == username):
                return member
        return None

def help():
    print("python bot.py {client token} [...]")


if __name__ == "__main__":
    if(len(sys.argv) <= 1):
        help()
    else:
        if len(sys.argv[1]) != 59:
            print("[ERROR]: Invalid token\n[ERROR]: Client secret should be 59 characters long")
        else:
            client = Bot()
            client.run(sys.argv[1])