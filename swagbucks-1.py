import discord
from discord.ext import commands
from discord import Webhook, RequestsWebhookAdapter as adapter
import asyncio
import requests
import json
import websockets
from datetime import datetime, timedelta



class Swagbucks(commands.Cog):
    """Swagbucks Websocket"""
    def __init__(self, client):
        self.client = client
        self.prize = 0
        self.ws = False
        self.socket_url = None
        self.pattern = []
        self.BEARER_TOKEN = None
        self.webhook_url = 'https://discord.com/api/webhooks/978637487557734450/LsGgwRX1sfYQ1AmVio5FvpUUNgk4BLx9GgsxO-NQuVc85PtmxN4zWsV7TUVr1IeDYez7'
        self.headers = None
        self.main_url = 'https://api.playswagiq.com/trivia/home?_uid='
        self.join_url = 'https://api.playswagiq.com/trivia/join?_uid='
        self.thumbnail = 'https://i.imgur.com/cexKy2o.gif'
        self.oot = [716891122491981844, 953918321051459625, 617305632084590593, 752534863013347349]

    def send_hook(self, data, data_type = None):
        hook = Webhook.from_url(self.webhook_url,
                                adapter = adapter())
        if data_type == None:
            hook.send(embed = data)
        elif data == "e":
            hook.send(data)
        else:
            em = discord.Embed(title = data)
            hook.send(embed = em)

    def disconnect_websocket(self):
        self.ws = False
        self.send_hook("Websocket Is Disconnected!", "embeded")
    
    def get_token(self):
        with open("token.json" , "r") as file:
          data = json.load(file)
          self.BEARER_TOKEN = data["token"]
          self.headers = {
                          "Authorization": f"Bearer {self.BEARER_TOKEN}",
                          "user-agent":"SwagIQ-Android/34 (okhttp/3.10.0)"
                         }
    
    def update_token(self):
        with open("token.json" , "w") as file:
          data = {"token" : f"{ket}"}
          json.dump(data, file)

    def response_1(self, x = None ):
        self.get_token()
        r = requests.post(url = self.main_url, headers = self.headers)
        #if r.status_code != 200:
        #    self.send_hook("Token Expired", "embeded")
        #    return
        response_data = r.json()
        prize = response_data["episode"]["grandPrizeDollars"]
        prz = '{:,}'.format(int(prize))
        time = response_data["episode"]["start"]
        time_stamp = datetime.fromtimestamp(time)
        time_change = timedelta(hours=5, minutes=30)
        new_time = time_stamp + time_change
        time = new_time.strftime("%d-%m-%Y %I:%M %p")
        embed=discord.Embed(title="**__Next Show Details !__**", description=f"**• Show Name : Swagbucks Live\n• Show Time : {time}\n• Prize Money : ${prz}**")
        embed.set_thumbnail(url=self.thumbnail)
        embed.set_footer(text="Swagbucks Live")
        embed.timestamp = datetime.utcnow()
        self.prize = int(prize)
        if x == "send": self.send_hook(embed)

    def response_2(self):
        self.response_1()
        r = requests.post(url = self.join_url, headers = self.headers)
        response_data = r.json()
        self.ws = response_data['success']
        if self.ws == True:
            self.send_hook("Websocket Is Connected!", "embeded")
            id = response_data["viewId"]
            socket_url = f"wss://api.playswagiq.com/sock/1/game/{id}?_uid="
            self.socket_url = socket_url
        else: self.send_hook("Show Not On!", "embeded")

    async def connect_websocket(self):
        self.response_2()
        if self.ws == True:
            async with websockets.connect(self.socket_url, extra_headers = self.headers) as wss:
                async for msg in wss:
                    if self.ws == False: return
                    message_data = json.loads(msg)
                    if message_data["code"] != 21: print(message_data)
                    if message_data["code"] == 41:
                        qn = message_data["question"]["number"]
                        tqn = message_data["question"]["totalQuestions"]
                        optid1 = message_data["question"]["answers"][0]["id"]
                        optid2 = message_data["question"]["answers"][1]["id"]
                        optid3 = message_data["question"]["answers"][2]["id"]
                        try:
                            sb = message_data["question"]["sb"]
                        except:
                            sb = 0
                        embed=discord.Embed(title=f"**Question {qn} out of {tqn}**", description=f"**SB for this Question : {sb}**", color=discord.Colour.random())
                        embed.set_thumbnail(url=self.thumbnail)
                        embed.set_footer(text="Swagbucks Live")
                        embed.timestamp = datetime.utcnow()
                        self.send_hook(embed)
                        self.send_hook("e")
                        await asyncio.sleep(10)

                        embed=discord.Embed(title="⏰ **| Time's Up!**", color=discord.Colour.random())
                        self.send_hook(embed)
                    if message_data["code"] == 42:
                        ansid = message_data["correctAnswerId"]
                        s = e = 0
                        for answer in message_data["answerResults"]:
                            if answer["answerId"] == ansid:
                                advancing = answer["numAnswered"]
                                pA = answer["percent"]
                            else:
                                anNum = answer["numAnswered"]
                                s = s + anNum
                                percent = answer["percent"]
                                e = e + percent
                        pay = int(self.prize*100)/int(advancing)
                        payout = int(pay) + int(qn)
                        if ansid == optid1:
                            self.pattern.append("1")
                            option = f"Option :one: {optid1}"
                        if ansid == optid2:
                            self.pattern.append("2")
                            option = f"Option :two: {optid2}"
                        if ansid == optid3:
                            self.pattern.append("3")
                            option = f"Option :three: {optid3}"

                        embed=discord.Embed(title=f"**Question {qn} out of {tqn}**", color=discord.Colour.random())
                        embed.add_field(name="**Correct Answer :**", value=f"**{option}**")
                        embed.add_field(name="**Stats :**", value=f"**• Advancing Players : {advancing} ({pA}%)\n• Eliminated Players : {s} ({e}%)\n• Current Payout : {payout}SB**")
                        embed.add_field(name="**Ongoing Pattern :**", value=f"**{self.pattern}**")
                        embed.set_thumbnail(url=self.thumbnail)
                        embed.set_footer(text="Swagbucks Live")
                        embed.timestamp = datetime.utcnow()
                        self.send_hook(embed)
                    
                    if message_data["code"] == 49:
                        sb = max([data.get("sb") for data in message_data["winners"]])
                        embed = discord.Embed(title = "**__Game Summary !__**", description = f"**• Payout : {sb}SB\n• Total Winners : {advancing}\n• Prize Money : ${self.prize}**")
                        embed.set_thumbnail(url = self.thumbnail)
                        embed.set_footer(text = "Swagbucks Live")
                        embed.timestamp = datetime.utcnow()
                        await self.send_hook(embed)
                        self.pattern.clear()
                        self.ws = False
                        return

    @commands.command(name='startsb', aliases=['startswag', 'sbstart'], help = "Start the Swagbucks Socket")
    async def startsb(self, ctx):
        await ctx.message.delete()
        if self.ws == True:
            self.send_hook("Websocket is already connected!", "embeded")
        else:
            self.send_hook("Websocket is connecting...", "embeded")
            await self.connect_websocket()

    @commands.command(name='stopsb', aliases= ['dcswag', 'sbdisconnect', 'sbstop'], help = "Stop the Swagbucks Socket")
    async def stopsb(self, ctx):
        await ctx.message.delete()
        if self.ws == False:
            self.send_hook("Websocket already disconnected!", "embeded")
        else:
            self.disconnect_websocket()

    @commands.command(name='show', aliases= ['nextshow', 'nextsb'], help = "It gives the next show details")
    async def show(self, ctx):
            await ctx.message.delete()
            self.response_1("send")
    
    @commands.command(name= 'addtoken', aliases = ['updatetoken', 'changetoken'], help = "Change the Existing Swagbucks Token")
    async def addtoken(self, ctx, *, ket):
      if ctx.message.author.id in self.oot:
        try:
          self.update_token()
          await ctx.message.delete()
          self.send_hook("Token Updated Successful!", "embeded")
        except exception as error:
          print(error)
          #self.send_hook("Couldn't Update Token!", "embeded")
      else:
        self.send_hook("You Don't have permission to Update Token!", "embeded")
    
    @commands.command(name= 'gettoken', aliases = ['givetoken'], help = "Gives you Swagbucks Token")
    async def gettoken(self, ctx):
      if ctx.message.author.id in self.oot:
        try:
          self.get_token()
          await self.ctx.message.author.send(token)
        except exception as error:
          print(error)
      else:
        self.send_hook("You don't have Permission to get Token!", "embeded")
        

def setup(client):
    client.add_cog(Swagbucks(client))
    print("WebSocket is loaded.")
