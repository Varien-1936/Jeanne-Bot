import contextlib
from io import StringIO
from nextcord.ext.commands import Cog
from nextcord import *
from nextcord import slash_command as jeanne_slash
from os import execv
from sys import executable, argv
from assets.db_functions import add_botbanned_user, check_botbanned_user
from config import BB_WEBHOOK
from nextcord.ext.application_checks import *
from assets.errormsgs import owner_only, no_user

format = "%a, %d %b %Y | %H:%M:%S"

def restart_bot():
  execv(executable, ['python'] + argv)

class slashowner(Cog):
    def __init__(self, bot):
        self.bot = bot


    @jeanne_slash(description="Changes the bot's play activity")
    @is_owner()
    async def activity(self, ctx : Interaction, activitytype=SlashOption(description="Choose an activity type", choices=['listen', 'play'], required=True), activity=SlashOption(description="What is the new activity")):
        await ctx.response.defer()
        check = check_botbanned_user(ctx.user.id)
        if check == ctx.user.id:
            pass
        else:
            if activitytype=="listen":
                await self.bot.change_presence(activity=Activity(type=ActivityType.listening, name=activity))
                await ctx.followup.send(f"Bot's activity changed to `listening to {activity}`")            
            elif activitytype=="play":
                await self.bot.change_presence(activity=Game(name=activity))
                await ctx.followup.send(f"Bot's activity changed to `playing {activity}`")            
             
                

    @jeanne_slash(description="Finds a user")
    @is_owner()
    async def finduser(self, ctx: Interaction, user_id=SlashOption(description="Which user?")):
        await ctx.response.defer()
        check = check_botbanned_user(ctx.user.id)
        if check == ctx.user.id:
            pass
        else:
            user = await self.bot.fetch_user(user_id)
            if user.bot == True:
                botr = ":o:"
            else:
                botr = ":x:"
            fuser = Embed(title="User Found", color=0xccff33)
            fuser.add_field(name="Name",
                            value=user,
                            inline=True)
            fuser.add_field(name="Creation Date", value=user.created_at.strftime(format), inline=True)
            fuser.add_field(
                name="Mutuals", value=len(user.mutual_guilds), inline=True)
            fuser.add_field(
                name="Bot?", value=botr, inline=True)
            fuser.set_image(url=user.display_avatar)
            if user.banner==None:
                await ctx.followup.send(embed=fuser)
            else:
                userbanner = Embed(title="User Banner", color=0xccff33)
                userbanner.set_image(url=user.banner)

                e = [fuser, userbanner]
                await ctx.followup.send(embeds=e)
           

    @jeanne_slash(description="Restart me to be updated")
    @is_owner()
    async def update(self, ctx:Interaction):
        await ctx.response.defer()
        check = check_botbanned_user(ctx.user.id)
        if check == ctx.user.id:
            pass
        else:
            await ctx.followup.send(f"YAY! NEW UPDATE!")
            restart_bot()
    
    @jeanne_slash(description="Botban a user from using the bot")
    @is_owner()
    async def botban(self, ctx: Interaction, user_id=SlashOption(description="Which user?"), reason = SlashOption(description="Add a reason")):
        await ctx.response.defer(ephemeral=True)
        check = check_botbanned_user(ctx.user.id)
        if check == ctx.user.id:
            pass
        else:   
            user= await self.bot.fetch_user(user_id)
            add_botbanned_user(user_id, reason) is True                     

            botbanned=Embed(title="User has been botbanned!", description="They will no longer use Jeanne,permanently!")
            botbanned.add_field(name="User",
                            value=user)
            botbanned.add_field(name="ID", value=user.id,
                            inline=True)
            botbanned.add_field(name="Reason of ban",
                                    value=reason,
                                    inline=False)
            botbanned.set_footer(text="Due to this user botbanned, all data except warnings are immediatley deletedfrom the database! They will have no chance of appealing their botban and all the commands executed bythem are now rendered USELESS!")
            botbanned.set_thumbnail(url=user.avatar)
            webhook = SyncWebhook.from_url(BB_WEBHOOK)
            webhook.send(embed=botbanned)

            await ctx.followup.send("User botbanned", ephemeral=True)

    @jeanne_slash(description="Evaluates a code")
    @is_owner()
    async def evaluate(self, ctx: Interaction, raw=SlashOption(choices=["True", "False"], required=False)):
        await ctx.response.defer()
        check = check_botbanned_user(ctx.user.id)
        if check == ctx.user.id:
            pass
        else:
            await ctx.followup.send("Insert your code.\nType 'cancel' if you don't want to evaluate")
            def check(m):
                return m.author == ctx.user and m.content

            code = await self.bot.wait_for('message', check=check)

            if code.content.startswith("cancel"):
                await ctx.followup.send("Evaluation aborted")
                
            else:
                str_obj = StringIO()
                try:
                    with contextlib.redirect_stdout(str_obj):
                        exec(code.content)
                except Exception as e:
                    embed = Embed(title="Evaluation failed :negative_squared_cross_mark:\nResults:",
                                description=f"```{e.__class__.__name__}: {e}```", color=0xFF0000)
                    embed.set_footer(
                        text=f"Compiled in {round(self.bot.latency * 1000)}ms")
                    return await ctx.followup.send(embed=embed)
                if raw == None:
                    embed1 = Embed(title="Evaluation suscessful! :white_check_mark: \nResults:",
                            description=f'```{str_obj.getvalue()}```', color=0x008000)
                    embed1.set_footer(
                        text=f"Compiled in {round(self.bot.latency * 1000)}ms")
                    await ctx.followup.send(embed=embed1)
                else:
                    await ctx.followup.send(str_obj.getvalue())

    @jeanne_slash(description="Make me leave a server")
    @is_owner()
    async def leave_server(self, ctx: Interaction, server_id=SlashOption(description="What is the server's ID?", required=True)):
        await ctx.response.defer()
        check = check_botbanned_user(ctx.user.id)
        if check == ctx.user.id:
            pass
        else:
            guild=await self.bot.fetch_guild(server_id)
            
            try:
                confirm = Embed(title="Is this the server you want me to leave?", description=guild.name)

                if guild.icon == None:
                    pass
                elif guild.icon.is_animated() is True:
                    confirm.set_thumbnail(url=guild.icon.with_size(512))
                else:
                    confirm.set_thumbnail(url=guild.icon)

                confirm.set_footer(text="Type 'yes' to confirm or 'no' to cancel. You have 1 minute")

                confirmation=await ctx.followup.send(embed=confirm)

                def is_correct(m):
                    return m.author == ctx.user and m.content
                try:
                    msg = await self.bot.wait_for("message", check=is_correct, timeout=60.0)

                    if "Yes".lower() in msg.content:
                        confirmed = Embed(
                            description="Successfully left the server")
                        await guild.leave()
                        await confirmation.edit(embed=confirmed)

                    if "No".lower() in msg.content:
                        confirmed = Embed(
                            description="Okay then I'm staying in the server")
                        await confirmation.edit(embed=confirmed)

                except TimeoutError:
                    timeout = Embed(
                        description=f"Timeout", color=0xFF0000)
                    return await ctx.followup.send(embed=timeout)

            except Exception as e:
                await ctx.followup.send(embed=Embed(description=e))

    @Cog.listener()
    async def on_application_command_error(self, ctx: Interaction, error):
        if isinstance(error, ApplicationNotOwner):
            await ctx.send(embed=owner_only)
        elif isinstance(error, NotFound):
            await ctx.send(embed=no_user)




def setup(bot):
    bot.add_cog(slashowner(bot))
