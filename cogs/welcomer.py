from nextcord import *
from nextcord.ext.commands import Cog
from assets.db_functions import *
from config import db

class welcomer(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member):
        try:
            channel_id=get_welcomer(member.guild.id)
            server_id = fetch_welcomer(channel_id)

            if member.guild.id == server_id:
                channel = self.bot.get_channel(channel_id)
            
                welcome = Embed(description=f"Hi {member} and welcome to {member.guild.name}!",color=member.color).set_thumbnail(url=member.display_avatar)
                                
                await channel.send(embed=welcome)
            else:
                pass
        except Exception as e:
            print(e)

    @Cog.listener()
    async def on_member_remove(self, member):
        try:
            channel_id = get_leaver(member.guild.id)
            server_id= fetch_leaver(channel_id)

            if member.guild.id == server_id:
                channel = self.bot.get_channel(channel_id)

                leave = Embed(description=f"{member} left the server", color=0x00FFFF).set_thumbnail(url=member.display_avatar)

                await channel.send(embed=leave)
            else:
                pass
        except:
            pass

def setup(bot):
    bot.add_cog(welcomer(bot))
