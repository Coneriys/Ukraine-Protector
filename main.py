import disnake
from disnake.ext import commands
import asyncio
import datetime

bot = commands.Bot(intents=disnake.Intents.all())
user_last_message_time = {}

@bot.event
async def on_ready():
    print("хохлиии")
    await bot.change_presence(activity=disnake.Game(name="Ukraine Team"), status=disnake.Status.dnd)

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    if message.channel.id == 1174490869462736926:
        return

    # Проверяем, есть ли у пользователя роль мута или ту, которую бот пингует
    roles_to_check = [1183075996820308039, 1174473526489661511, 1174491569215258634, 1174491758390943875]
    if any(role.id in roles_to_check for role in message.author.roles):
        return

    utc_now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)

    if message.author.id in user_last_message_time:
        if (utc_now - user_last_message_time[message.author.id]).seconds < 4:
            await message.channel.send(f"{message.author.mention}, успокойся, спамерсреша.")
            embed = disnake.Embed(
                title="Нашлась спамерсреша!",
                description=f"По прописанному во мне коде, я замутил этого уебка, вот он: \n<@{message.author.id}>",
                colour=0xff0000,
                timestamp=datetime.datetime.now()
            )
            embed.set_footer(text="Made by Connor")

            channel = bot.get_channel(1174475817347203145)
            await channel.send("<@&1174473526489661511> <@&1174491569215258634> <@&1174491758390943875>", embed=embed)

            role = message.guild.get_role(1183075996820308039)
            await message.author.add_roles(role)
            await asyncio.sleep(3600)
            await message.author.remove_roles(role)
        else:
            user_last_message_time[message.author.id] = utc_now
    else:
        user_last_message_time[message.author.id] = utc_now

    await bot.process_commands(message)

@bot.slash_command(name="ban", description="Ban a user for a specified time")
async def ban(ctx, user: disnake.Member, duration: int):
    if ctx.author.guild_permissions.ban_members:
        await ctx.guild.ban(user)
        await ctx.send(f"{user.mention} был забанен на {duration} секунд.")
        await asyncio.sleep(duration)
        await ctx.guild.unban(user)
        await ctx.send(f"{user.mention} был разбанен после {duration} секунд.")
    else:
        await ctx.send("У вас нет разрешений на бан пользователей.")

@bot.slash_command(name="mute", description="Mute a user for a specified time")
async def mute(ctx, user: disnake.Member, duration: int):
    if ctx.author.guild_permissions.manage_roles:
        mute_role = disnake.utils.get(ctx.guild.roles, name="Muted")
        if not mute_role:
            mute_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(mute_role, send_messages=False)
        await user.add_roles(mute_role)
        await ctx.send(f"{user.mention} был замучен на {duration} секунд.")
        await asyncio.sleep(duration)
        await user.remove_roles(mute_role)
        await ctx.send(f"{user.mention} был размучен после {duration} секунд.")
    else:
        await ctx.send("У вас нет разрешений на управление ролями.")

bot.run("token here")
