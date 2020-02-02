import discord
from discord.ext import commands, tasks
import random
import asyncio

client = commands.Bot(command_prefix=".")
allow_spam = True
number, ans, play_guess_num, play_millionaire = 0, 0, 0, 0
guess_count = 'None'
messages_list = []

million_questions = [['q1. 1+1 = ?', ['a:2', 'b:1', 'c:3', 'd:4']]]
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


song_ban_list = []  # todo keep it from being blank every time I run this bot


@client.command(aliases=['bansong', 'bs'])
async def ban_song(ctx, song_name):
    """this func is under development, not working at the moment"""
    await ctx.send(f'{song_name} has been banned')
    global song_ban_list
    song_ban_list.append(song_name)
    print(song_ban_list)


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
async def ran_num_gen(ctx, start, end):
    """.rannum <start> <end>, this allow you to generate a random number in a range"""
    await ctx.send(f'{random.randint(int(start),int(end))}')


@client.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()


@client.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()


@client.command(aliases=['playguessnum'])
async def guess_num(ctx, num=100):
    global ans, play_guess_num, guess_count
    number = int(num)
    ans = random.randint(1,number)
    play_guess_num = True
    guess_count = 0
    await ctx.send("Enter number to guess.")


@client.command(aliases=['playmillionaire', 'playmil'])
async def millionaire(ctx):
    global play_millionaire, mil_ans
    play_millionaire = True

    question_set = random.choice(million_questions)
    mil_choices = question_set[1]
    random.shuffle(mil_choices)
    mil_ans = mil_choices.index(question_set[1][0])

    await ctx.send(question_set[0])
    await ctx.send(f'A: {mil_choices[0]}')
    await ctx.send(f'B: {mil_choices[1]}')
    await ctx.send(f'C: {mil_choices[2]}')
    await ctx.send(f'D: {mil_choices[3]}')


@client.event
async def on_message(msg):

    if '-play' in msg.content.split():
        await msg.channel.send("-stop")
        await msg.channel.send("Why doesn't this work on groovy??")
        # todo make groovy stop

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

    global play_millionaire, mil_ans
    if play_millionaire:
        if msg.content in ['a', 'b', 'c', 'd', 'A', 'B', 'C', 'D']:
            if mil_ans == 0:
                if msg.content == 'a' or 'A':
                    await msg.channel.send('You are right.')
                    mil_continue = True
            if mil_ans == 1:
                if msg.content == 'b' or 'B':
                    await msg.channel.send('You are right.')
                    mil_continue = True
            if mil_ans == 2:
                if msg.content == 'c' or 'C':
                    await msg.channel.send('You are right.')
                    mil_continue = True
            if mil_ans == 3:
                if msg.content == 'd' or 'D':
                    await msg.channel.send('You are right.')
                    mil_continue = True
                    


    await client.process_commands(msg)


client.run('NjYxNTg0NjUyNTgyMjU2Njgw.Xgtrug.sM-4vY0u-DwJH9YeOiWlsD7o0vo')


# todo make a 百萬富翁 game
