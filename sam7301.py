import discord
from discord.ext import commands, tasks
import random
import asyncio

client = commands.Bot(command_prefix=".")
allow_spam = True
number, ans, play_guess_num = 0, 0, 0
guess_count = 'None'
messages_list = []

@client.event
async def on_ready():
    open('messages.txt', 'w').close()  # clear the messages.txt file
    print("Bot is ready")


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


@client.command(aliases=['playguessnum', 'pgn'])
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
