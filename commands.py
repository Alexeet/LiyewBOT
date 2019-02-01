import importlib

class CommandHandler():
    def __init__(self, client):
        self.command_dict = dict()
        self.client = client
        self.prefix = "&"
        return
    
    
    async def importModule(self, module_name):
        try:
            new_module = importlib.import_module(module_name)
        except ImportError:
            print("Error trying to import module {}!".format(module_name))
            return
        
        try:
            module_class = new_module.init(self.client)
        except NameError:
            print("Error initializing module {}!".format(module_name))
            return
        
        print("Module {} loaded. Available commands :".format(module_name))
        for i in module_class.command_list:
            print("\t - {}".format(i))
            self.command_dict[i] = module_class
    

    async def loadModulesFromConfig(self, config_path="config.cfg"):
        with open(config_path) as config:

            #config.cfg parsing
            line = "\n"
            while(not line.startswith("modules:") and line != ""):
                    line = config.readline()
                    print(line)
            
            if(line == ""):
                pass

            modulelist = line[8:].split()
            modulelist = filter(lambda x:x!="", modulelist)

            #Import each module specified in config.cfg
            for module in modulelist:
                await self.importModule(module)
            

    async def processMessage(self, message):
        print("{0.author}@{0.server.name}/{0.channel.name}:{0.content}".format(message))
        if(message.author == message.server.me):
            return
        if(not message.content.startswith(self.prefix)):
            return

        splitted_msg = message.content.split()
        cmd_name = splitted_msg[0]
        cmd_name = cmd_name.replace(self.prefix, "", 1)
        if(cmd_name not in self.command_dict):
            await self.client.send_message(message.channel, "Unknown command `{}`".format(cmd_name))
            return
        #Command recognised
        module = self.command_dict[cmd_name]
        await module.call(cmd_name, splitted_msg[1:], message)
        return