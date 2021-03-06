from config import db
from time import time
from datetime import timedelta
from sys import version_info as py_version
from nextcord.ext.commands import Cog
from nextcord import *
from nextcord import slash_command as jeanne_slash, __version__ as discord_version

format = "%a, %d %b %Y | %H:%M:%S"
start_time = time()

class slashinfo(Cog):
    def __init__(self, bot):
        self.bot = bot

    @jeanne_slash(description="See the bot's status from development to now")
    async def stats(self, ctx : Interaction):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                "SELECT * FROM botbannedData WHERE user_id = ?", (ctx.user.id,))
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]

            if ctx.user.id == botbanned:
                pass
        except:
            botowner = self.bot.get_user(597829930964877369)
            embed = Embed(title="Bot stats", color=0x236ce1)
            embed.add_field(
                name="Developer", value=f"• **Name:** {botowner}\n• **ID:** {botowner.id}", inline=True)
            embed.add_field(name="Bot ID", value=self.bot.user.id, inline=True)
            embed.add_field(name="Creation Date", value=self.bot.user.created_at.strftime(format), inline=True)
            embed.add_field(
                name="Version", value=f"• **Python Version:** {py_version.major}.{py_version.minor}.{py_version.micro}\n• **Nextcord Version:** {discord_version}\n• **Bot:** 3.2a", inline=True)

            cur=db.execute("SELECT * FROM globalxpData")
            all_users=len(cur.fetchall())
            embed.add_field(name="Count",
                            value=f"• **Server Count:** {len(self.bot.guilds)} servers\n• **User Count:** {len(set(self.bot.get_all_members()))}\n• **Cached Members:** {all_users}", inline=True)

            current_time = time()
            difference = int(round(current_time - start_time))
            uptime = str(timedelta(seconds=difference))
            embed.add_field(
                name="Uptime", value=f"{uptime} hours", inline=True)

            embed.add_field(name="Invites",
                            value="• [Invite me to your server](https://discord.com/api/oauth2/authorize?client_id=831993597166747679&permissions=1565918620726&scope=bot%20applications.commands)\n• [Vote for me](https://top.gg/bot/831993597166747679)\n• [Join the support server](https://discord.gg/VVxGUmqQhF)", inline=True)

            embed.set_thumbnail(
                url=self.bot.user.avatar)
            await ctx.followup.send(embed=embed)

    @jeanne_slash(description="See the information of a member or yourself")
    async def userinfo(self, ctx : Interaction, member: Member = SlashOption(description="Which member?", required=False)):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                "SELECT * FROM botbannedData WHERE user_id = ?", (ctx.user.id,))
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]

            if ctx.user.id == botbanned:
                pass
        except:
            if member == None:
                member = ctx.user
            user = await self.bot.fetch_user(member.id)
            hasroles = [
                role.mention for role in member.roles][1:][:: -1]

            if member.bot == True:
                botr = "Yes"
            else:
                botr = "No"

            date = round(member.joined_at.timestamp())
            userinfo = Embed(title="{}'s Info".format(member.name),
                            color=0xccff33)
            userinfo.add_field(name="Name", value=member, inline=True)
            userinfo.add_field(name="ID", value=member.id, inline=True)
            userinfo.add_field(name="Is Bot?", value=botr, inline=True)
            userinfo.add_field(
                name="Joined Server", value='<t:{}:F>'.format(str(date)), inline=True)
            userinfo.add_field(name="Number of Roles",
                               value=(len(hasroles) + 1), inline=True)
            userinfo.add_field(name="Roles Held",
                            value=''.join(hasroles[:20]) + '@everyone', inline=False)
            userinfo.set_thumbnail(url=member.display_avatar)
            
            try:
                userinfo.set_image(url=user.banner)
            except:
                pass
            await ctx.followup.send(embed=userinfo)

    @jeanne_slash(description="Get information about this server")
    async def serverinfo(self, ctx : Interaction):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                "SELECT * FROM botbannedData WHERE user_id = ?", (ctx.user.id,))
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]

            if ctx.user.id == botbanned:
                pass
        except:        
            guild = ctx.guild
            emojis = [str(x) for x in guild.emojis]
            features = guild.features

            if guild.premium_subscription_count < 2:
                boostlevel = "0"
            elif guild.premium_tier == 1:
                boostlevel = "1"
            elif guild.premium_tier == 2:
                boostlevel = "2"
            elif guild.premium_tier == 3:
                boostlevel = "3"

            date = round(guild.created_at.timestamp())
            serverinfo = Embed(title="Server's Info", color=0x00B0ff)
            serverinfo.add_field(name="Name", value=guild.name, inline=True)
            serverinfo.add_field(name="ID", value=guild.id, inline=True)
            serverinfo.add_field(
                name="Creation Date", value='<t:{}:F>'.format(str(date)), inline=True)
            serverinfo.add_field(name="Owner", value=f"• **Name: ** {guild.owner}\n• ** ID: ** {guild.owner_id}", inline=True)
            serverinfo.add_field(
                name="Members", value=f"• **Humans:** {len(guild.humans)}\n• **Bots:** {len(guild.bots)}\n• **Total Members:** {guild.member_count}")
            serverinfo.add_field(name="Boost Status",
                                 value=f"• **Boosters:** {len(guild.premium_subscribers)}\n• **Boosts:** {guild.premium_subscription_count}\n• **Tier:** {boostlevel}",
                            inline=True)
            serverinfo.add_field(name='Features',
                            value=features, inline=False)

            if guild.icon==None:
                pass
            elif guild.icon.is_animated() is True:
                serverinfo.set_thumbnail(url=guild.icon.with_size(512))
            else:
                serverinfo.set_thumbnail(url=guild.icon)

            if guild.splash==None:
                pass
            else:
                serverinfo.set_image(url=guild.splash)

            if len(emojis) == 0:
                await ctx.followup.send(embed=serverinfo)

            else:
                emojie = Embed(title="Emojis", description=''.join(emojis[:40]), color=0x00B0ff)

                e=[serverinfo, emojie]
                
                await ctx.followup.send(embeds=e)


    @jeanne_slash(description="Check how fast I respond to a command")
    async def ping(self, ctx : Interaction):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                "SELECT * FROM botbannedData WHERE user_id = ?", (ctx.user.id,))
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]

            if ctx.user.id == botbanned:
                pass
        except:
            start_time = time()
            test = Embed(description="Testing ping", color=0x236ce1)
            msg= await ctx.followup.send(embed=test)

            ping = Embed(color=0x236ce1)
            ping.add_field(
                name="**>** Bot Latency", value=f'{round(self.bot.latency * 1000)}ms', inline=False)
            end_time = time()
            ping.add_field(
                name="**>** API Latency", value=f'{round((end_time - start_time) * 1000)}ms', inline=False)
            await msg.edit(embed=ping)

    @jeanne_slash(description="See the server's banner")
    async def guildbanner(self, ctx : Interaction):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                "SELECT * FROM botbannedData WHERE user_id = ?", (ctx.user.id,))
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]

            if ctx.user.id == botbanned:
                pass
        except:
            guild = ctx.guild
            banner = guild.banner

            if guild.premium_subscription_count < 2:
                nobanner = Embed(description="Server is not boosted at tier 2")
                await ctx.followup.send(embed=nobanner)
            
            else:
                try:
                    embed = Embed(colour=0x00B0ff)
                    embed.set_footer(text=f"{guild.name}'s banner")
                    embed.set_image(url=banner)
                    await ctx.followup.send(embed=embed)
                except:
                    embed=Embed(description='Guild has no banner')
                    await ctx.followup.send(embed=embed)

    @jeanne_slash(description="See your avatar or another member's avatar")
    async def avatar(self, ctx: Interaction, member: Member = SlashOption(description="Which member?", required=False)):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                "SELECT * FROM botbannedData WHERE user_id = ?", (ctx.user.id,))
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]

            if ctx.user.id == botbanned:
                pass
        except:
            if member==None:
                member=ctx.user

            avatar = Embed(title=f"{member}'s Avatar", color=0x236ce1)
            avatar.set_image(url=member.avatar)
            await ctx.followup.send(embed=avatar)

    @jeanne_slash(description="See your guild avatar or a member's guild avatar")
    async def guildavatar(self, ctx: Interaction, member: Member = SlashOption(description="Which member?", required=False)):
        await ctx.response.defer()
        try:
            botbanquery = db.execute(
                "SELECT * FROM botbannedData WHERE user_id = ?", (ctx.user.id,))
            botbanned_data = botbanquery.fetchone()
            botbanned = botbanned_data[0]

            if ctx.user.id == botbanned:
                pass
        except:
            if member == None:
                member = ctx.user

            guild_avatar = Embed(title=f"{member}'s Avatar", color=0x236ce1)

            try:
                guild_avatar.set_image(url=member.guild_avatar)
                await ctx.followup.send(embed=guild_avatar)
            except:
                guild_avatar.set_image(url=member.avatar)
                guild_avatar.set_footer(
                    text="Member has no server avatar. Passed normal avatar instead")
                await ctx.followup.send(embed=guild_avatar)


def setup(bot):
    bot.add_cog(slashinfo(bot))
