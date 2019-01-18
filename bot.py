import discord
import asyncio
import logging
import sys


_MASTERS_IDS_ = ["217982938703331328"]

class Bot(discord.Client):
    async def on_ready(self):
        print("Logged on as {}!".format(self.user))


    async def is_for_me(self, message):
        return message.content.startswith("./") and (message.author != self.user) 


    async def check_rank(self, member, server):
        if(member == None or server == None):
            return None
        
        if("ltools" not in [i.name for i in server.roles]):
            try:
                ltools_role = await self.create_role(server)
                await self.edit_role(server, ltools_role, name="ltools")
                await self.add_roles(server.me, ltools_role)
            except discord.errors.Forbidden:
                await self.send_message(server.default_channel, "Missing permission : [discord.manage_roles]")

        if("ltools" in [i.name for i in member.roles]):
            return True
        return False
        

    async def on_message(self, message):
        if(await self.is_for_me(message)):
            authorized = await self.check_rank(message.author, message.channel.server)
            print("{}@{}:\'{}\'{}".format(message.author.name, message.server.name, message.content, authorized))
            if(authorized):
                await self.process_message(message)
            else:
                await self.delete_message(message)
            

    async def process_message(self, message):
        args = message.content.split(" ")
        args[0] = args[0][2:]   #Removing prefix
        
        #Regular commands
        if(args[0] == "ping"):
            await self.send_message(message.channel, "pong!")
        elif(args[0] == "pong"):
            await self.send_message(message.channel, "ping!")
        elif(args[0] == "kick"):
            await self.kick_cmd(args, message)
        
        #Dev commands
        if(args[0].startswith("dev") and message.author.id not in _MASTERS_IDS_):
            await self.send_message(message.channel, "Who do you think you are ?")
            return

        if(args[0] == "dev/checkrank"):
            user = await self.find_user(args[1], message.server)
            res = await self.check_rank(user, message.server)
            await self.send_message(message.channel, str(res))
        elif(args[0] == "dev/kill"):
            await self.die()
    
    
    async def kick_cmd(self, args, message):
        if(len(args) <=1 or message.server == None):
            await self.send_message(message.channel, "./kick_cmd (user) [-f(orce)]")
            return
        
        user_to_kick = await self.find_user(args[1], message.server)

        if(user_to_kick == None):
            await self.send_message(message.channel, "Could not find user {}.".format(args[1]))
            return
        
        if(user_to_kick.voice.voice_channel == None):
            await self.send_message(message.channel, "User {} is not in a voice channel".format(args[1]))
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
    

    async def die(self):
        await self.logout()

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