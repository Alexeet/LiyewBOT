from discord import errors, ChannelType

class Kick:
    def __init__(self, client):
        self.command_list = ["kick"]
        self.client = client

        self.channel_name = "Mexican Border"

    async def call(self, cmdname, args, message):
        if(cmdname not in self.command_list):
            return
        elif(cmdname == "kick"):
            await self.kick(args, message)
    
    async def kick(self, args, message):
        if(len(args) < 1):
            await self.client.send_message(message.channel, "`{}kick [user] (-f)`".format(self.client.command_handler.prefix))
            return
        member_list = await self.client.list_members(args[0], message.server)
        if(len(member_list)==0):
            await self.client.send_message(message.channel, "Could not find user `{}`.".format(args[0]))
            return
        if(len(member_list) > 1):
            await self.client.send_message(message.channel, "Multiple users found. Please be more precise")
            return
        try:
            newchan = await self.client.create_channel(message.server, self.channel_name, type=ChannelType.voice)
        except errors.Forbidden:
            try:
                await self.client.send_message(message.channel, "Missing permission : `create_channel`")
            except errors.Forbidden:
                print("Insufficient permissions in server {}".format(message.server))
            return
                
        try:
            await self.client.move_member(member_list[0], newchan)
        except errors.Forbidden:
            try:
                await self.client.send_message(message.channel, "Missing permission : `move_member`")
            except errors.Forbidden:
                print("Insufficient permissions in server {}".format(message.server))
            return
            
        await self.client.delete_channel(newchan)
        
        
def init(client):
    return Kick(client)

if __name__ == "__main__":
    print("This is a bot module")
    print("Add this module to your bot config.cfg file")