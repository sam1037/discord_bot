#todo better orgainise the code using cogs, see more in yt tutorial.

from asyncio.tasks import wait
import re
from types import DynamicClassAttribute
import discord
from discord.ext import commands, tasks
import random
import asyncio
import math
import datetime
import time
import csv
from dateutil import parser
import sqlite3

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=".", intents=intents)
client = discord.Client()


allow_spam = True
number, ans, play_guess_num = 0, 0, 0
guess_count = 'None'
messages_list = []
num_emojis = [":one:",
    ":two:",
    ":three:",
    ":four:",
    ":five:",
    ":six:",
    ":seven:",
    ":eight:",
    ":nine:",
    ":ten:"]

num_emo_unicode = [
    "1\ufe0f\u20e3",
    "2\ufe0f\u20e3",
    "3\ufe0f\u20e3",
    "4\ufe0f\u20e3",
    "5\ufe0f\u20e3",
    "6\ufe0f\u20e3",
    "7\ufe0f\u20e3",
    "8\ufe0f\u20e3",
    "9\ufe0f\u20e3"
]

bot.remove_command("help")


#set up database
conn = sqlite3.connect("bot.db")
cursor = conn.cursor()


@bot.event
async def on_ready():
    printTime.start()
    global nine_chat
    for channel in bot.get_all_channels():
        if channel.name == "9chat":
            nine_chat = channel
    open('messages.txt', 'w').close()  # clear the messages.txt file
    print("Bot is ready")
    # todo schedule that task using schedule

    a = [a for a in bot.all_commands]
    for a1 in a:
        print(a1)

    #check reminder ?is there better way to implement this?
    check_reminder.start()


@bot.command()
async def get_id(ctx):
    # get the voice channel id
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
        print(channel)
        print(channel.id)
    else:
        await ctx.send("You are not connected to a voice channel")
        return


@tasks.loop(hours=1)
async def printTime():
    now = datetime.datetime.now()
    current_time = now.strftime("%d:%H")
    print("Current Time =", current_time)

@bot.command()
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
    helpEmbed.add_field(name="remind <time> <reminder>", value="send a reminder after some time", inline=False)

    await ctx.message.channel.send(embed=helpEmbed)

@bot.command()
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

    #create embed object and send time_match
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

@bot.command()
async def pick(ctx, num=1):
    num = int(num)
    # get channel id
    try:
        channel = ctx.message.author.voice.channel
    except Exception:
        await ctx.send("You must be in a channel in order to use this command")
    # create splited team list 
    else:
        mem_list = [mem.display_name for mem in channel.members if not mem.bot]
        if num > len(mem_list):
            await ctx.message.channel.send(f"There is not enough member in the channel!")
            return

        choosen_list = random.sample(mem_list, num)
        mes = discord.Embed(
            title = "CHOOSEN PEOPLE",
            colour = discord.Colour.red(),
            description = "\n".join(choosen_list)
        )

        await ctx.message.channel.send(embed=mes)


@bot.command()
async def ping(ctx):
    """.ping, this is use for testing your ping"""
    await ctx.send(f'ping: {round(bot.latency * 1000)}ms')


@bot.command(aliases=['8ball'])
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


@bot.command(aliases=['stopspam'])
async def stop_spam(ctx):
    """.stopspam, this ban people from using the func 'spam'"""
    global allow_spam
    allow_spam = False


@bot.command(aliases=['allowspam'])
async def allow_spam(ctx):
    """.allowspam, this allow people to use the func 'spam'"""
    global allow_spam
    allow_spam = True


@bot.command()
async def spam(ctx, time, *args):
    """.spam <time> <text>, this func allow people to spam text"""
    if allow_spam:
        text = ' '
        text = text.join(args)
        for a in range(int(time)):
            if allow_spam:  # this is for banning spam when it is spamming
                await ctx.send(text)


@bot.command(aliases=['rannum'])
async def ran_num_gen(ctx, start=1, end=2):
    """.rannum <start> <end>, this allow you to generate a random number in a range"""
    try:
        start = int(start)
        end = int(end)
        num = random.randint(start, end)
        await ctx.send(f"The choosen number is num")
    except Exception as e:
        await ctx.send(e)
    

@bot.command(aliases=['playguessnum', 'pgn', "guessnum"])
async def guess_num(ctx, num=100):
    global ans, play_guess_num, guess_count
    number = int(num)
    ans = random.randint(1,number)
    play_guess_num = True
    guess_count = 0
    await ctx.send("Enter number to guess.")


@bot.command()
async def mkpoll(ctx, topic, *opts):
    # make a poll
    if len(opts) > 10:    
        await ctx.send("The maximum number of options is 10.")

    opts = [(f"{num_emojis[i]} {opt}") for i, opt in enumerate(opts)]
    embed = discord.Embed(
        colour = ctx.author.color,
        title = topic,
        description = "\n".join(opts)
    )

    poll_msg = await ctx.send(embed=embed)
    for i in range(len(opts)):
        await poll_msg.add_reaction(num_emo_unicode[i])


def test(var, name):
    print(f"\n{'-'*30}\n{name}: \n{var}\n{type(var)}\n{'-'*30}\n")


@bot.command()
async def maybe(ctx):
    num = random.randint(1,2)
    if num == 1:
        #post gif 
        await ctx.send(file=discord.File("just_do_it.gif"))
    else:
        await ctx.send(file=discord.File("nah.gif"))


@bot.command()
async def remind(ctx, *, message):
    """send reminder after a specific time, default is 1 hour"""
    if not message:
        await ctx.send("Invalid input")
        return
    #get time and reminder by regex, channel id, and author_id
    time_match = re.search("^[0-9]+(s|h|d|)", message) #note that this is optional 
    channel_id = ctx.channel.id
    author_id = ctx.author.id

    #find the reminder 
    reminder = message
    if time_match:
        if len(message) > len(time_match.group()):
            reminder = re.sub(time_match.group(), "", message).strip() 
        else:
            time_match = None
    
    #find time_unit and time_scaler
    time_unit = "h"
    time_scaler = 1
    if time_match:
        print("We have a time_match!")
        time_scaler = int(re.search("[0-9]+", time_match.group()).group())
        time_unit = re.search("(s|h|d)", time_match.group())
        if time_unit:
            time_unit = time_unit.group()
        
    #tests
    """
    test(time_match, "time_match")
    test(reminder, "reminder")
    test(time_scaler, "time scaler")
    test(time_unit, "time_unit")
    """

    #handle time stuff
    current_local_time = datetime.datetime.now() 
    time_dict = {"s": 1, "h": 3600, "d": 86400}
    wait_time_second = time_dict[time_unit] * time_scaler
    due_time = current_local_time + datetime.timedelta(seconds=wait_time_second)

    # store the reminder into the "reminder" database
    cursor.execute("""INSERT INTO reminder 
        (reminder, receive_time, due_time, channel_id, author_id) 
        VALUES (?, ?, ?, ?, ?)""", 
        (reminder, str(current_local_time), str(due_time), channel_id, author_id))
    conn.commit()

    #
    await ctx.send("reminder received!")

    

@tasks.loop(seconds = 10)
async def check_reminder():
    #get data from database
    raw_data = cursor.execute("""SELECT * FROM reminder""")
    names = [a[0] for a in raw_data.description]
    result= []
    for row in raw_data.fetchall():
        dict_entry = {}
        for i in range(len(row)):
            dict_entry[names[i]] = row[i]
        result.append(dict_entry)

    # check if due
    for reminder in result:
        if parser.parse(reminder["due_time"]) < datetime.datetime.now():
            #send message
            channel = bot.get_channel(int(reminder["channel_id"]))
            author = bot.get_user(int(reminder["author_id"]))
            await channel.send(f"REMINDER by {author.display_name} on {reminder['receive_time']}:\n{reminder['reminder']}")
            
            #remove the ereminder from database
            cursor.execute("DELETE FROM reminder WHERE reminder = ?", (reminder["reminder"], ))
            print("\nDELETE REMINDER!!!!!\n")
            conn.commit()
            #TODO I should used id, but this will work for most cases and maybe do this later


#todo: add task to clear reminder outdated lines periodically (use task loop)
@bot.event
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

    await bot.process_commands(msg)


bot.run('NjYxNTg0NjUyNTgyMjU2Njgw.XgtiuA.SWtnucLY3NX3Dt9r_DVOMvkAcQY')



# TODO make a 百萬富翁 game
