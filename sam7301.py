import discord
from discord.ext import commands, tasks
import random
import asyncio
import math

client = commands.Bot(command_prefix=".")
allow_spam = True
number, ans, play_guess_num = 0, 0, 0
guess_count = 'None'
messages_list = []


client.remove_command("help")

@client.event
async def on_ready():
    global nine_chat
    for channel in client.get_all_channels():
        if channel.name == "9chat":
            nine_chat = channel
    open('messages.txt', 'w').close()  # clear the messages.txt file
    print("Bot is ready")
    # todo schedule that task using schedule

    a = [a for a in client.all_commands]
    for a1 in a:
        print(a1)


@client.command()
async def get_id(ctx):
    # get the voice channel id
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
        print(channel)
        print(channel.id)
    else:
        await ctx.send("You are not connected to a voice channel")
        return

@client.command()
async def help(ctx):
    helpEmbed = discord.Embed(color=ctx.author.color, title="HELP")

    helpEmbed.add_field(name="help", value="Bring up this message", inline=False)
    helpEmbed.add_field(name="split", value="Split user in the voice channel into two group", inline=False)
    helpEmbed.add_field(name="ping", value="Return the network latency", inline=False)
    helpEmbed.add_field(name="8ball <question>", value="Answer your question", inline=False)
    helpEmbed.add_field(name="stopspam", value="Ban the command 'spam'", inline=False)
    helpEmbed.add_field(name="allowspam", value="Allow the command 'spam' to be used", inline=False)
    helpEmbed.add_field(name="spam <time> <content>", value="Spam the content for a number of time", inline=False)
    helpEmbed.add_field(name="guessnum <maxium number>", value="Play a game of guessing number", inline=False)

    await ctx.message.channel.send(embed=helpEmbed)

@client.command()
async def split(ctx):
    # get channel id
    try:
        channel = ctx.message.author.voice.channel
    except Exception:
        await ctx.send("You must be in a channel in order to use this command")
    # create splited team list 
    else:
        mem_list = [mem for mem in channel.members if not mem.bot]
        length = len(mem_list)
        if length <= 1:
            await ctx.send("There must be more than one user in the channel in order to use this command")
            return
        random.shuffle(mem_list)
        teamA = mem_list[0:math.ceil(length/2)]
        teamB = [a.display_name for a in mem_list if a not in teamA]
        teamA = [a.display_name for a in teamA]

    #create embed object and send result
        mesA = discord.Embed(
            title = "TEAM A",
            colour = discord.Colour.red(),
            description = "\n".join(teamA)
        )

        mesB = discord.Embed(
            title = "TEAM B",
            colour = discord.Colour.blue(),
            description = "\n".join(teamB)
        )

        await ctx.message.channel.send(embed=mesA)
        await ctx.message.channel.send(embed=mesB)


@client.command()
async def ping(ctx):
    """.ping, this is use for testing your ping"""
    await ctx.send(f'ping: {round(client.latency * 1000)}ms')


@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    """.8ball <question>, this func will ans your question"""
    replies = ['It is certain.',
               'It is decidedly so.',
               'Without a doubt.',
               'Yes - definitely.',
               'You may rely on it.',
               'As I see it, yes.',
               'Most likely.',
               'Outlook good.',
               'Yes.',
               'Signs point to yes.',
               'Reply hazy, try again.',
               'Ask again later.',
               'Better not tell you now.',
               'Cannot predict now.',
               'Concentrate and ask again.',
               "Don't count on it.",
               'My reply is no.',
               'My sources say no.',
               'Outlook not so good.',
               'Very doubtful.']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(replies)}')


@client.command(aliases=['stopspam'])
async def stop_spam(ctx):
    """.stopspam, this ban people from using the func 'spam'"""
    global allow_spam
    allow_spam = False


@client.command(aliases=['allowspam'])
async def allow_spam(ctx):
    """.allowspam, this allow people to use the func 'spam'"""
    global allow_spam
    allow_spam = True


@client.command()
async def spam(ctx, time, *args):
    """.spam <time> <text>, this func allow people to spam text"""
    if allow_spam:
        text = ' '
        text = text.join(args)
        for a in range(int(time)):
            if allow_spam:  # this is for banning spam when it is spamming
                await ctx.send(text)


@client.command(aliases=['rannum'])
async def ran_num_gen(ctx, start=1, end=10):
    """.rannum <start> <end>, this allow you to generate a random number in a range"""
    await ctx.send(f'{random.randint(int(start),int(end))}')


@client.command(aliases=['playguessnum', 'pgn', "guessnum"])
async def guess_num(ctx, num=100):
    global ans, play_guess_num, guess_count
    number = int(num)
    ans = random.randint(1,number)
    play_guess_num = True
    guess_count = 0
    await ctx.send("Enter number to guess.")


@client.event
async def on_message(msg):

    # guess num
    global play_guess_num, guess_count
    if play_guess_num:
        try:
            guess = int(msg.content)
        except ValueError:
            pass  # if msg.content isn't a number
        else:
            if guess > ans:
                await msg.channel.send("Your guess is higher than the answer")
                guess_count += 1
            if guess < ans:
                await msg.channel.send("Your guess is lower than the answer")
                guess_count += 1
            if guess == ans:
                if guess_count == 0:
                    await msg.channel.send("You win! You have guessed 1 time.")
                else:
                    await msg.channel.send(f"You win! You have guessed {guess_count+1} times.")
                play_guess_num = False

    await client.process_commands(msg)


client.run('NjYxNTg0NjUyNTgyMjU2Njgw.Xgtrug.sM-4vY0u-DwJH9YeOiWlsD7o0vo')


# todo make a 百萬富翁 game
