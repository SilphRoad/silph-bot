
import discord

from discord.ext.commands import Bot


role_whitelist = [
    182106535588134912,  # US_South
    182107305125347328,  # South_America
    182107632293773313,  # Japan
    182107963115175940,  # Africa
    182108089946734592,  # Australasia
    182108160117571585,  # Southeast_Asia
    182108273007263744,  # Asia
    182108333690454016,  # Eastern_Europe
    182108404091846656,  # Western_Europe
    182108484991582208,  # UK_And_Ireland
    182108603824472064,  # Central_America
    182108658853740544,  # US_Northeast
    182108743771750400,  # US_Midwest
    182108808313569280,  # US_Southwest
    182108858448084992,  # US_Mountain_West
    182108955613462528,  # US_Pacific_Coast
    182109068591235073,  # Eastern_Canada
    182109121150058496,  # Western_Canada
]


role_match = {}

silph_bot = Bot(command_prefix="!")


def build_roles(roles):
    for r in roles:
        if int(r.id) in role_whitelist:
            role_match[r.name.lower()] = r


def get_role(ch):
    name = str(ch).replace('#', '').lower()
    return role_match.get(name)


@silph_bot.event
async def on_ready():
    for s in silph_bot.servers:
        build_roles(s.roles)

    await silph_bot.change_presence(game=discord.Game(name='Pokemon Go'))
    print("Bot is active")


@silph_bot.command(pass_context=True)
async def silphbot(ctx, channel):
    channel_id = channel.replace('<#', '').replace('>', '')
    name = ctx.message.server.get_channel(channel_id)

    if not name:
        return

    name = name.name
    role = get_role(name)

    if not role:
        print("{} is not a role".format(name))
        return

    await silph_bot.add_roles(ctx.message.author, role)
    await silph_bot.add_reaction(ctx.message, u"\U0001F44B")
    print("{} joined {}".format(ctx.message.author, role.name))


@silph_bot.command(pass_context=True)
async def hello(ctx):
    pass
    # print(dir(ctx.message.author))
    # return await silph_bot.say("Hello, world!")


@silph_bot.command(pass_context=True)
async def working(ctx, *, status: str):
    if str(ctx.message.author.top_role) != 'Executives':
        return

    return await silph_bot.change_presence(game=discord.Game(name=status))


@silph_bot.command(pass_context=True)
async def map(ctx):
    await ctx.send(
        'The Silph League is a global player network for Pokemon GO that '
        'enables large-scale coordination and events! You can view the map '
        'of local groups here: https://thesilphroad.com/map'
    )


if __name__ == '__main__':
    import os

    token = os.environ.get('DISCORD_KEY')

    if not token:
        raise Exception('DISCORD_KEY is not set')

    silph_bot.run(token)
