import discord
import random
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import requests
from discord.ext.commands.errors import NSFWChannelRequired

class fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(description="Ask 8 ball anything and you will get your awnser")
    async def _8ball(self, ctx: SlashContext, question):
        responses = [
            'It is certain.', 'It is decidedly so.', 'Without a doubt.',
            'Yes – definitely.', 'You may rely on it.', 'As I see it, yes.',
            'Most likely.', 'Outlook good.', 'Yes.', 'Signs point to yes.',
            'Reply hazy, try again.', 'Ask again later.',
            'Better not tell you now.', 'Cannot predict now.',
            'Concentrate and ask again.', 'Dont count on it.', 'My reply is no.',
            'My sources say no.', 'Outlook not so good.', 'Very doubtful.'
        ]
        embed = discord.Embed(color=0x0000FF)
        embed.add_field(name="Question:", value=f'{question}', inline=False)
        embed.add_field(
            name="Answer:", value=f'{random.choice(responses)}', inline=False)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(description="Roll a dice")
    async def dice(self, ctx:SlashContext):
        embed = discord.Embed(color=0x0000FF)
        embed.add_field(name="Dice Rolled", value="You rolled a {}!".format(
            random.randint(1, 6)), inline=False)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(description="Type two words to get one combined word")
    async def combine(self, ctx:SlashContext, name1, name2):
        name1letters = name1[:round(len(name1) / 2)]
        name2letters = name2[round(len(name2) / 2):]
        ship = "".join([name1letters, name2letters])
        emb = (discord.Embed(color=0x36393e, description=f"{ship}"))
        emb.set_author(name=f"{name1} + {name2}")
        await ctx.send(embed=emb)

    @cog_ext.cog_slash(description="Flip a coin")
    async def flip(self, ctx:SlashContext):
        await ctx.send(embed=discord.Embed(color=0x0000FF,
                                           description=f"`{random.choice(['Heads', 'Tails'])}`"))

    @cog_ext.cog_slash(description="Get some hentai from Yande.re")
    @commands.is_nsfw()
    async def hentai(self, ctx: SlashContext):
                yandere_api = random.choice(requests.get("https://yande.re/post.json?tags=rating:explicit-yiff-loli-ntr-vore-poop-pooping-scat-scat_eating-scat_on_penis-bestiality-furry-shota-blood-rape-bee-animal-hyper-guro-child-cub").json())
                yandere = discord.Embed(color=0xFFC0CB)
                yandere.set_image(url=yandere_api["file_url"])
                yandere.set_footer(text="Fetched from Yande.re")

                await ctx.send(embed=yandere)

    @hentai.error
    async def hentai_error(self, ctx, error):
        if isinstance(error, NSFWChannelRequired):
            error = discord.Embed(
                        title='Hentai Failed', description="Hentai couldn't be sent in this channel", color=0xff0000)
            error.add_field(
                        name="Reason", value="Channel is not NSFW enabled")
            await ctx.send(embed=error)
 
def setup(bot):
    bot.add_cog(fun(bot))