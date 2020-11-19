  
'''
using discord.py version 1.0.0a
'''
import discord
import asyncio
import re
import random
import datetime
import multiprocessing
import threading
import concurrent
from discord.ext import commands
from discord.ext.commands import bot
import colorsys

client = commands.Bot(command_prefix='-')
client.remove_command('help')

@client.event
async def on_ready():
    print('online')
    print('----------')
    
	    
@client.command()
async def q(ctx,que: str):
             #await ctx.delete()
	     embed=discord.Embed(title="**__QUESTION ALERT !__**", url="https://discord.gg/2degbQMAxU", description=f"**Question No. [{que}](https://discord.gg/2degbQMAxU) is coming soon on your mobile screen.**", color=discord.Color.red())
	     embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/775385239245160478/778865719437164544/help-147419__340.png")
	     embed.set_image(url="https://cdn.discordapp.com/attachments/775385239245160478/778921858363949057/Tw.gif")
	     embed.set_footer(text="Developed by Subrata#3297", icon_url="https://cdn.discordapp.com/attachments/775385239245160478/778865719437164544/help-147419__340.png")
	     await ctx.send(embed=embed)

@client.command()
async def hq(ctx,time=None, accuracy=None, ques=None, prize=None):
	if not time or not accuracy or not ques or not prize:
		await ctx.say("wrong use! please add correct values")
	else:
		embed=discord.Embed(color=discord.Color.red())
		embed.add_field(name="Hq Trivia",value="Results of Hq Trivia")
		embed.add_field(name="Game Time",value=time)
		embed.add_field(name="Accuracy",value=accuracy)
		embed.add_field(name="Total Question",value=ques)
		embed.add_field(name="Winning amount",value=prize)
		embed.set_footer(text="Made by Myran#0001")
		embed.set_thumbnail(url="") #Put Your Thumbnail url
		await ctx.send(embed=embed)

client.run('NzczOTI4NTc1NzAyNzk0MjUx.X6QXJw.r-U_XbSALwkVzSxK7zg0DTNytvU')

#BOT_OWNER_ROLE = 'Runner' # change to what you need
#BOT_OWNER_ROLE_ID = "503197827556704268" 
  
g="https://discord.gg/2degbQMAxU" 

 
oot_channel_id_list = ["773610866679611413", "775945251340156930"]

answer_pattern = re.compile(r'(n|not)?([1-4]{1})(\?)?(cnf|c|cf|conf|apg)?(\w|\ww)?$', re.IGNORECASE)

apgscore = 1000
nomarkscore = 320
markscore = 320

async def update_scores(content, answer_scores):
    global answer_pattern

    m = answer_pattern.match(content)
    if m is None:
        return False

    ind = int(m[2])-1

    if m[1] is None:
        if m[3] is None:
            if m[4] is None:
                answer_scores[ind] += nomarkscore
            else: # apg
                if m[5] is None:
                    answer_scores[ind] += apgscore
                else:
                    answer_scores[ind] += markscore

        else: # 1? ...
            answer_scores[ind] += markscore

    else: # contains not or n
        if m[3] is None:
            answer_scores[ind] -= nomarkscore
        else:
            answer_scores[ind] -= markscore

    return True

class SelfBot(discord.Client):

    def __init__(self, update_event, answer_scores):
        super().__init__()
        global oot_channel_id_list
        #global wrong
        self.oot_channel_id_list = oot_channel_id_list
        self.update_event = update_event
        self.answer_scores = answer_scores

    async def on_ready(self):
        print("======================")
        print("DANGER TRIVIA || BOTS")
        print("Connected to discord.")
        print("User: " + self.user.name)
        print("ID: " + str(self.user.id))

    # @bot.event
    # async def on_message(message):
    #    if message.content.startswith('-debug'):
    #         await message.channel.send('d')

        def is_scores_updated(message):
            if message.guild == None or \
                str(message.channel.id) not in self.oot_channel_id_list:
                return False

            content = message.content.replace(' ', '').replace("'", "")
            m = answer_pattern.match(content)
            if m is None:
                return False

            ind = int(m[2])-1

            if m[1] is None:
                if m[3] is None:
                    if m[4] is None:
                        self.answer_scores[ind] += nomarkscore
                    else: # apg
                        if m[5] is None:
                            self.answer_scores[ind] += apgscore
                        else:
                            self.answer_scores[ind] += markscore

                else: # 1? ...
                    self.answer_scores[ind] += markscore

            else: # contains not or n
                if m[3] is None:
                    self.answer_scores[ind] -= nomarkscore
                else:
                    self.answer_scores[ind] -= markscore

            return True

        while True:
            await self.wait_for('message', check=is_scores_updated)
            self.update_event.set()

class Bot(discord.Client):

    def __init__(self, answer_scores):
        super().__init__()
        self.bot_channel_id_list = []
        self.embed_msg = None
        self.embed_channel_id = None
        #global wrong
        self.answer_scores = answer_scores

        # embed creation
        #value=random.randint(0,0xffffff)
        self.embed=discord.Embed(title="**__Kumu Trivia Answers :__**", colour=0x00ff00)
        self.embed.add_field(name="**__Option ❶__**", value=f"**[0]({g})**", inline=False)
        self.embed.add_field(name="**__Option ❷__**", value=f"**[0]({g})**", inline=False)
        self.embed.add_field(name="**__Option ❸__**", value=f"**[0]({g})**", inline=False)
        self.embed.add_field(name="**__Option ❹__**", value=f"**[0]({g})**", inline=False)
        self.embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/775948612014178315/778496961354924042/icon.png")
        self.embed.set_footer(text='Kumu | Subrata#3297',icon_url='https://cdn.discordapp.com/emojis/778499210798432256.png')
        #self.embed.add_field(name="**__Correct Answer !__**", value="0", inline=False)
        #self.embed.add_field(name="**__Erased Answer !__**", value="0", inline=False) 


        #await self.bot.add_reaction(embed,':spy:')


    async def clear_results(self):
        for i in range(len(self.answer_scores)):
            self.answer_scores[i]=0

    async def update_embeds(self):
      #  global wrong

         

        one_check = ""
        two_check = ""
        three_check = ""
        four_check = ""
        mark_check_one=""
        mark_check_two=""
        mark_check_three=""
        mark_check_four=""
        one_cross =""
        two_cross =""
        three_cross =""
        four_cross =""
        best_answer = "**Option ➜** <a:redload:772439692411011073>"
        not_answer = "**Option ➜** <a:redload:772439692411011073>"
              

        lst_scores = list(self.answer_scores)
        

        highest = max(lst_scores)
        gif_ans = 'https://cdn.discordapp.com/attachments/769445612231720960/774230429023993896/unnamed.gif'
        best_answer = '**Option ➜** <a:redload:772439692411011073>'
        lowest = min(lst_scores)
        answer = lst_scores.index(highest)+1
        wrong = lst_scores.index(lowest)+1
       #global wrong             

        if highest > 0:
            if answer == 1:
                one_check = " <:emoji_13:772843132093202443>  "
                mark_check_one = "<:emoji_62:735102374523306047>"
                gif_ans = "https://cdn.discordapp.com/emojis/778484715761434634.png"
                best_answer = "**Option ➜** <:emoji_65:778484715761434634> <a:emoji_26:772878582930210848>"
                   
            else:
                one_check = " "

            if answer == 2:
                two_check = " <:emoji_13:772843132093202443>  "
                mark_check_two = "<:emoji_62:735102374523306047>"
                gif_ans = "https://cdn.discordapp.com/emojis/778484756840448011.png"
                best_answer = "**Option ➜** <:emoji_66:778484756840448011> <a:emoji_26:772878582930210848>"
                   
            else:
                two_check = ""

            if answer == 3:
                three_check = " <:emoji_13:772843132093202443> "
                mark_check_three = "<:emoji_62:735102374523306047>"
                gif_ans = "https://cdn.discordapp.com/emojis/778484782132756480.png"
                best_answer = "**Option ➜** <:emoji_67:778484782132756480> <a:emoji_26:772878582930210848>"
                   
            else:
                three_check = ""

            if answer == 4:
                four_check = " <:emoji_13:772843132093202443> "
                mark_check_three = "<:emoji_62:735102374523306047>"
                gif_ans = "https://cdn.discordapp.com/emojis/778487061741174814.png"
                best_answer = "**Option ➜** <:emoji_68:778487061741174814> <a:emoji_26:772878582930210848>"

            else:
                four_check = ""


        if lowest < 0:
            if wrong == 1:
                one_cross = " <:emoji_43:776062431100928001>"
                not_answer = "**Option ➜** <:emoji_43:776062431100928001>" 
               
            if wrong == 2:
                two_cross = " <:emoji_43:776062431100928001>"
                not_answer = "**Option ➜** <:emoji_43:776062431100928001>" 
               
            if wrong == 3:
                three_cross = " <:emoji_43:776062431100928001>"
                not_answer = "**Option ➜** <:emoji_43:776062431100928001>"

            if wrong == 4:
                four_cross = " <:emoji_43:776062431100928001>"
                not_answer = "**Option ➜** <:emoji_43:776062431100928001>"
         
    
        self.embed.set_field_at(0, name="**__Option ❶__**", value=f"**[{lst_scores[0]}]({g}){one_check}{one_cross}**")
        self.embed.set_field_at(1, name="**__Option ❷__**", value=f"**[{lst_scores[1]}]({g}){two_check}{two_cross}**")
        self.embed.set_field_at(2, name="**__Option ❸__**", value=f"**[{lst_scores[2]}]({g}){three_check}{three_cross}**")
        self.embed.set_field_at(3, name="**__Option ❹__**", value=f"**[{lst_scores[3]}]({g}){four_check}{four_cross}**")
        #self.embed.set_thumbnail(url="{}".format(gif_ans))
        #self.embed.set_field_at(4, name="**__Correct Answer !__**", value=best_answer, inline=True)
        #self.embed.set_field_at(5, name="**__Erased Answer !__**", value=not_answer, inline=True) 


        if self.embed_msg is not None:
            await self.embed_msg.edit(embed=self.embed)

    async def on_ready(self):
        print("==============")
        print("DANGER TRIVIA || BOTS")
        print("Connected to discord.")
        print("User: " + self.user.name)
        print("ID: " + str(self.user.id))
        #log=self.get_channel(775948612014178315)
        #await log.send("> ** Kumu Database Is Updated ** ✅")
        await self.clear_results()
        await self.update_embeds()
        #await self.change_presence(activity=discord.Game(name='with '+str(len(set(self.get_all_members())))+' users'))
        await self.change_presence(activity=discord.Activity(type=1,name="with Kumu Trivia (km)"))

    async def on_message(self, message):


        # if message is private
        if message.author == self.user or message.guild == None:
            return

        if message.content.lower() == "km":
            await message.delete()

            self.embed_msg = None
            await self.clear_results()
            await self.update_embeds()
            self.embed_msg = \
                await message.channel.send('',embed=self.embed)
            await self.embed_msg.add_reaction("<a:emoji_48:776277928333017129>")
            self.embed_channel_id = message.channel.id    
                
        if message.content.startswith('+q1'):
           await message.delete()
           embed = discord.Embed(title=f"**__QUESTION ALERT !__**", url="https://discord.gg/vGeN4ZUQye", description="**Question No. 1 is coming soon on your mobile screen.**", color=0x0000FF)
           embed.set_image(url="https://cdn.discordapp.com/attachments/775945251340156930/778851388108701726/Tw.gif")
           embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/775945251340156930/778840043116167198/help-147419__340.png")
           embed.set_footer(text="HQ Trivia | Subrata#3297", icon_url="https://cdn.discordapp.com/emojis/750255302787465317.png")
           await message.channel.send(embed=embed)

        if message.content.startswith('+q2'):
           await message.delete()
           embed = discord.Embed(title=f"**__QUESTION ALERT !__**", url="https://discord.gg/vGeN4ZUQye", description="**Question No. 2 is coming soon on your mobile screen.**", color=0x0000FF)
           embed.set_image(url="https://cdn.discordapp.com/attachments/775945251340156930/778851388108701726/Tw.gif")
           embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/775945251340156930/778840043116167198/help-147419__340.png")
           embed.set_footer(text="HQ Trivia | Subrata#3297", icon_url="https://cdn.discordapp.com/emojis/750255302787465317.png")
           await message.channel.send(embed=embed)

        if message.content.startswith('+q3'):
           await message.delete()
           embed = discord.Embed(title=f"**__QUESTION ALERT !__**", url="https://discord.gg/vGeN4ZUQye", description="**Question No. 3 is coming soon on your mobile screen.**", color=0x0000FF)
           embed.set_image(url="https://cdn.discordapp.com/attachments/775945251340156930/778851388108701726/Tw.gif")
           embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/775945251340156930/778840043116167198/help-147419__340.png")
           embed.set_footer(text="HQ Trivia | Subrata#3297", icon_url="https://cdn.discordapp.com/emojis/750255302787465317.png")
           await message.channel.send(embed=embed)

        if message.content.startswith('+q4'):
           await message.delete()
           embed = discord.Embed(title=f"**__QUESTION ALERT !__**", url="https://discord.gg/vGeN4ZUQye", description="**Question No. 4 is coming soon on your mobile screen.**", color=0x0000FF)
           embed.set_image(url="https://cdn.discordapp.com/attachments/775945251340156930/778851388108701726/Tw.gif")
           embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/775945251340156930/778840043116167198/help-147419__340.png")
           embed.set_footer(text="HQ Trivia | Subrata#3297", icon_url="https://cdn.discordapp.com/emojis/750255302787465317.png")
           await message.channel.send(embed=embed)

        if message.content.startswith('+q5'):
           await message.delete()
           embed = discord.Embed(title=f"**__QUESTION ALERT !__**", url="https://discord.gg/vGeN4ZUQye", description="**Question No. 5 is coming soon on your mobile screen.**", color=0x0000FF)
           embed.set_image(url="https://cdn.discordapp.com/attachments/775945251340156930/778851388108701726/Tw.gif")
           embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/775945251340156930/778840043116167198/help-147419__340.png")
           embed.set_footer(text="HQ Trivia | Subrata#3297", icon_url="https://cdn.discordapp.com/emojis/750255302787465317.png")
           await message.channel.send(embed=embed)

        if message.content.startswith('+q6'):
           await message.delete()
           embed = discord.Embed(title=f"**__QUESTION ALERT !__**", url="https://discord.gg/vGeN4ZUQye", description="**Question No. 6 is coming soon on your mobile screen.**", color=0x0000FF)
           embed.set_image(url="https://cdn.discordapp.com/attachments/775945251340156930/778851388108701726/Tw.gif")
           embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/775945251340156930/778840043116167198/help-147419__340.png")
           embed.set_footer(text="HQ Trivia | Subrata#3297", icon_url="https://cdn.discordapp.com/emojis/750255302787465317.png")
           await message.channel.send(embed=embed)

        if message.content.startswith('+q7'):
           await message.delete()
           embed = discord.Embed(title=f"**__QUESTION ALERT !__**", url="https://discord.gg/vGeN4ZUQye", description="**Question No. 7 is coming soon on your mobile screen.**", color=0x0000FF)
           embed.set_image(url="https://cdn.discordapp.com/attachments/775945251340156930/778851388108701726/Tw.gif")
           embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/775945251340156930/778840043116167198/help-147419__340.png")
           embed.set_footer(text="HQ Trivia | Subrata#3297", icon_url="https://cdn.discordapp.com/emojis/750255302787465317.png")
           await message.channel.send(embed=embed)

        if message.content.startswith('+q8'):
           await message.delete()
           embed = discord.Embed(title=f"**__QUESTION ALERT !__**", url="https://discord.gg/vGeN4ZUQye", description="**Question No. 8 is coming soon on your mobile screen.**", color=0x0000FF)
           embed.set_image(url="https://cdn.discordapp.com/attachments/775945251340156930/778851388108701726/Tw.gif")
           embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/775945251340156930/778840043116167198/help-147419__340.png")
           embed.set_footer(text="HQ Trivia | Subrata#3297", icon_url="https://cdn.discordapp.com/emojis/750255302787465317.png")
           await message.channel.send(embed=embed)

        if message.content.startswith('+q9'):
           await message.delete()
           embed = discord.Embed(title=f"**__QUESTION ALERT !__**", url="https://discord.gg/vGeN4ZUQye", description="**Question No. 9 is coming soon on your mobile screen.**", color=0x0000FF)
           embed.set_image(url="https://cdn.discordapp.com/attachments/775945251340156930/778851388108701726/Tw.gif")
           embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/775945251340156930/778840043116167198/help-147419__340.png")
           embed.set_footer(text="HQ Trivia | Subrata#3297", icon_url="https://cdn.discordapp.com/emojis/750255302787465317.png")
           await message.channel.send(embed=embed)

        if message.content.startswith('+q0'):
           await message.delete()
           embed = discord.Embed(title=f"**__QUESTION ALERT !__**", url="https://discord.gg/vGeN4ZUQye", description="**Question No. 10 is coming soon on your mobile screen.**", color=0x0000FF)
           embed.set_image(url="https://cdn.discordapp.com/attachments/775945251340156930/778851388108701726/Tw.gif")
           embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/775945251340156930/778840043116167198/help-147419__340.png")
           embed.set_footer(text="HQ Trivia | Subrata#3297", icon_url="https://cdn.discordapp.com/emojis/750255302787465317.png")
           await message.channel.send(embed=embed)

        if message.content.startswith('+qe1'):
           await message.delete()
           embed = discord.Embed(title=f"**__QUESTION ALERT !__**", url="https://discord.gg/vGeN4ZUQye", description="**Question No. 11 is coming soon on your mobile screen.**", color=0x0000FF)
           embed.set_image(url="https://cdn.discordapp.com/attachments/775945251340156930/778851388108701726/Tw.gif")
           embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/775945251340156930/778840043116167198/help-147419__340.png")
           embed.set_footer(text="HQ Trivia | Subrata#3297", icon_url="https://cdn.discordapp.com/emojis/750255302787465317.png")
           await message.channel.send(embed=embed)

        if message.content.startswith('+qe2'):
           await message.delete()
           embed = discord.Embed(title=f"**__QUESTION ALERT !__**", url="https://discord.gg/vGeN4ZUQye", description="**Question No. 12 is coming soon on your mobile screen.**", color=0x0000FF)
           embed.set_image(url="https://cdn.discordapp.com/attachments/775945251340156930/778851388108701726/Tw.gif")
           embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/775945251340156930/778840043116167198/help-147419__340.png")
           embed.set_footer(text="HQ Trivia | Subrata#3297", icon_url="https://cdn.discordapp.com/emojis/750255302787465317.png")
           await message.channel.send(embed=embed)   

        # process votes
        if message.channel.id == self.embed_channel_id:
            content = message.content.replace(' ', '').replace("'", "")
            updated = await update_scores(content, self.answer_scores)
            if updated:
                await self.update_embeds()

def bot_with_cyclic_update_process(update_event, answer_scores):

    def cyclic_update(bot, update_event):
        f = asyncio.run_coroutine_threadsafe(bot.update_embeds(), bot.loop)
        while True:
            update_event.wait()
            update_event.clear()
            f.cancel()
            f = asyncio.run_coroutine_threadsafe(bot.update_embeds(), bot.loop)
            #res = f.result()

    bot = Bot(answer_scores)

    upd_thread = threading.Thread(target=cyclic_update, args=(bot, update_event))
    upd_thread.start()

    loop = asyncio.get_event_loop()
    loop.create_task(bot.start('NzczOTI4NTc1NzAyNzk0MjUx.X6QXJw.r-U_XbSALwkVzSxK7zg0DTNytvU'))
    loop.run_forever()


def selfbot_process(update_event, answer_scores):

    selfbot = SelfBot(update_event, answer_scores)

    loop = asyncio.get_event_loop()
    loop.create_task(selfbot.start('NjYwMzM3MzQyMDMyMjQ4ODMy.X6uAMA.Z5E4mok4Fn7iAzMRRN_1dLZSGqY',
                                   bot=False))
    loop.run_forever()

if __name__ == '__main__':

    # running bot and selfbot in separate OS processes

    # shared event for embed update
    update_event = multiprocessing.Event()

    # shared array with answer results
    answer_scores = multiprocessing.Array(typecode_or_type='i', size_or_initializer=5)

    p_bot = multiprocessing.Process(target=bot_with_cyclic_update_process, args=(update_event, answer_scores))
    p_selfbot = multiprocessing.Process(target=selfbot_process, args=(update_event, answer_scores))

    p_bot.start()
    p_selfbot.start()

    p_bot.join()
    p_selfbot.join()




 
 
