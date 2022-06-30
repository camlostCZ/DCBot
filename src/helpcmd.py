from discord.ext import commands


class PBotHelpCmd(commands.HelpCommand):
   # !help
    async def send_bot_help(self, mapping):
        await self.context.send("This is help")
       
   # !help <command>
    async def send_command_help(self, command):
        await self.context.send("This is help command")
      
   # !help <group>
    async def send_group_help(self, group):
        await self.context.send("This is help group")
    
   # !help <cog>
    async def send_cog_help(self, cog):
        await self.context.send("This is help cog")
