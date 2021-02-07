  
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


#client.run('NzczOTI4NTc1NzAyNzk0MjUx.X6QXJw.r-U_XbSALwkVzSxK7zg0DTNytvU')

#BOT_OWNER_ROLE = '($DTBR$)' # change to what you need
#BOT_OWNER_ROLE_ID = "793123278481784852" 
  
g="https://discord.gg/2degbQMAxU" 

 
oot_channel_id_list = ["806800636540747786", "801499869251764244", "800989471628722186", "793388002553364490", "801499868467429427", "788389503982108673", "798822635261657108", "798468658057445428", "798238659631382600", "797755504738697216", "796573179732164669", "793392396876120115", "786768541797711932", "789520246443868200", "788389503982108673", "789520646978797618", "789044225336803358", "788389503982108673", "789044225336803358", "789520246443868200", "788389503982108673", "788998011149484033", "789520246443868200", "788977659547746336", "788389503982108673", "775945251340156930", "788977659547746336", "788977659547746336"]

answer_pattern = re.compile(r'(n|not|nt)?([1-4]{1})(\?)?(cnf|c|cf|conf|apg)?(\w|\ww)?$', re.IGNORECASE)

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
        self.embed=discord.Embed(title="**Zaimo || Fangame**", colour=0x00ff00)
        #self.embed.set_author(name="**Crowd Results !**", icon_url="https://cdn.discordapp.com/emojis/787155458996568115.png")
        self.embed.add_field(name="**__Option -１__**", value=f"➜ **[0]({g})**", inline=False)
        self.embed.add_field(name="**__Option -２__**", value=f"➜ **[0]({g})**", inline=False)
        self.embed.add_field(name="**__Option -３__**", value=f"➜ **[0]({g})**", inline=False)
        self.embed.add_field(name="**__Option -４__**", value=f"➜ **[0]({g})**", inline=False)
        self.embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/787155458996568115.png")
        self.embed.set_footer(text='Connected to PVTS...',icon_url='https://cdn.discordapp.com/avatars/807922855501234197/91732a6af9cf4ed8e725969e85dd7edd.webp?size=1024')
        #self.embed.add_field(name="**__Correct Answer :__**", value="0", inline=False)
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
        gif_ans = 'https://cdn.discordapp.com/emojis/773955381063974972.gif'
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
                best_answer = "**Option ➜** <:emoji_65:778484715761434634> <a:Yes:769595037028843580>"
                   
            else:
                one_check = " "

            if answer == 2:
                two_check = " <:emoji_13:772843132093202443>  "
                mark_check_two = "<:emoji_62:735102374523306047>"
                gif_ans = "https://cdn.discordapp.com/emojis/778484756840448011.png"
                best_answer = "**Option ➜** <:emoji_66:778484756840448011> <a:Yes:769595037028843580>"
                   
            else:
                two_check = ""

            if answer == 3:
                three_check = " <:emoji_13:772843132093202443> "
                mark_check_three = "<:emoji_62:735102374523306047>"
                gif_ans = "https://cdn.discordapp.com/emojis/778484782132756480.png"
                best_answer = "**Option ➜** <:emoji_67:778484782132756480> <a:Yes:769595037028843580>"
                   
            else:
                three_check = ""

            if answer == 4:
                four_check = " <:emoji_13:772843132093202443> "
                mark_check_three = "<:emoji_62:735102374523306047>"
                gif_ans = "https://cdn.discordapp.com/emojis/778487061741174814.png"
                best_answer = "**Option ➜** <:emoji_68:778487061741174814> <a:Yes:769595037028843580>"

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
         
    
        self.embed.set_field_at(0, name="**__Option -１__**", value=f"➜ **[{lst_scores[0]}]({g}){one_check}{one_cross}**")
        self.embed.set_field_at(1, name="**__Option -２__**", value=f"➜ **[{lst_scores[1]}]({g}){two_check}{two_cross}**")
        self.embed.set_field_at(2, name="**__Option -３__**", value=f"➜ **[{lst_scores[2]}]({g}){three_check}{three_cross}**")
        self.embed.set_field_at(3, name="**__Option -４__**", value=f"➜ **[{lst_scores[3]}]({g}){four_check}{four_cross}**")
        self.embed.set_thumbnail(url="{}".format(gif_ans))
        #self.embed.set_field_at(4, name="**__Correct Answer :__**", value=best_answer, inline=True)
        #self.embed.set_field_at(5, name="**__Erased Answer !__**", value=not_answer, inline=True) 


        if self.embed_msg is not None:
            await self.embed_msg.edit(embed=self.embed)

    async def on_ready(self):
        print("==============")
        print("DANGER TRIVIA || BOTS")
        print("Connected to discord.")
        print("User: " + self.user.name)
        print("ID: " + str(self.user.id))
        log=self.get_channel(775942082615443497)
        await log.send("> ** DT Database Is Updated ** ✅")
        await self.clear_results()
        await self.update_embeds()
        while True:
            await self.change_presence(activity=discord.Game(name="with Danger || Trivia★᭄ꦿ᭄ | Command=dt"))
            await asyncio.sleep(2)
            await self.change_presence(activity=discord.Activity(type=2,name="with Zaimo & Kumu Trivia !"))
            await asyncio.sleep(2)


    async def on_message(self, message):


        # if message is private
        if message.author == self.user or message.guild == None:
            return

        if message.content.lower() == "+":
                await message.delete()
            #if BOT_OWNER_ROLE in [role.name for role in message.author.roles]:
                self.embed_msg = None
                await self.clear_results()
                await self.update_embeds()
                self.embed_msg = \
                    await message.channel.send('',embed=self.embed)
                await self.embed_msg.add_reaction("<a:emoji_48:776277928333017129>")
                await self.embed_msg.add_reaction("<a:emoji_26:772878582930210848>")
                self.embed_channel_id = message.channel.id  

            #else:
                #embed=discord.Embed(title="__Danger Private [DTB]#7565__", description="**Lol** You Not Have Permission to Use This **Cmd!** :stuck_out_tongue_winking_eye: If You Want to Use This Command Then DM Subrata#3297", color=0x00ff00)
                #await message.channel.send("**Lol** You Not Have Permission To Use This Cmd! :stuck_out_tongue_winking_eye:")
            #return
                
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
    loop.create_task(bot.start('ODA3OTIyODU1NTAxMjM0MTk3.YB_Cyw.EzLtqCkZtgtTITmpH3b5UEi4v8E'))
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




 
 
