import discord
import random
from discord.ext import commands
import asyncio
from discord.ui import Button, View, Select

from Location import mainlocation
import json
import os
from enemy import enemy_record
from ItemInfo import market_list, buy_able
from Help import Cmd

# importing libraries

os.chdir('C:/Users/axolo/Documents')

# enabling all intents and setting a command prefix for commands
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=",", intents=intents)  # set a prefix
bot.remove_command('help')


# A start event after the bot ran
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(',help'))
    print('Bot is online')
    print(discord.__version__)

# this event contain the bot's status and activity plus is shows the version of discord python we're using.


@bot.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = ['Absolutely.', 'Yes.', 'No.',  # responses
                 'Better not tell you now.',
                 'Of course.',
                 'Maybe later I will tell you.',
                 'Never.', 'Maybe.', 'Nope.', 'Do not ask me dumb questions.',
                 'Unfortunately yes.', 'No idea.', 'Of course not.', 'No you dummy.',
                 'Cannot predict now', 'Hell no.', 'Ask again later', 'Always!', 'Deffinitely.']

    answer = random.choice(responses)

    embed = discord.Embed(title='8ball response', color=10181046)
    embed.add_field(name="Question:", value=f"{question}", inline=False)
    embed.add_field(name='Answer:', value=f'{answer}', inline=False)

    await ctx.send(embed=embed)


@bot.command(description='Send user\'s latency number')
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=5):
    await ctx.message.delete()
    await ctx.channel.purge(limit=amount)
    await ctx.send('Message deleted')


@bot.command(description='A moderation command')
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{ctx.author} kicked {member} reason:{reason}')


# An object called DurationConverter to convert time
class DurationConverter(commands.Converter):
    async def convert(self, ctx, argument):
        amount = argument[:-1]
        unit = argument[-1]

        if amount.isdigit() and unit in ['s', 'm']:
            return (int(amount), unit)

        raise commands.BadArgument(message='invalid duration')


@bot.command(description='A moderation command')
@commands.has_permissions(ban_members=True)
async def tempban(ctx, member: discord.Member, duration: DurationConverter):
    multiplier = {'s': 1, 'm': 60}
    amount, unit = duration

    await member.ban()
    await ctx.send(f'{ctx.author} banned {member} for {amount}{unit}.')
    await asyncio.sleep(amount * multiplier[unit])
    await ctx.guild.unban(member)


@bot.command(description='A moderation command')
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{ctx.author} banned {member} reason:{reason}')


@bot.command(description='A moderation command')
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.name}#{user.discriminator}')
            return





# An object MyView1
# Attributes to MyView1 are score, ctx, score2 and shame
class MyView1(View):

    def __init__(self, ctx, score, score2, shame):
        super().__init__()
        self.ctx = ctx
        self.score = score
        self.score2 = score2
        self.shame = shame

    @discord.ui.button(label='Start', style=discord.ButtonStyle.blurple, emoji='🔛', custom_id='H')
    async def button_callback_hi(self, button, interaction):
        embed = discord.Embed(title='BJ')
        embed.add_field(name="Your score:", value=f"{self.score}", inline=False)
        embed.add_field(name="Opponent's score:", value="?", inline=False)

        await interaction.response.edit_message(view=self, embed=embed)

    @discord.ui.button(label='Hit/Double-down', style=discord.ButtonStyle.danger, emoji='⚠', custom_id='move')
    async def button_callback(self, button, interaction):
        button2 = [x for x in self.children if x.custom_id == 'move'][0]
        button1 = [x for x in self.children if x.custom_id == 'inspect'][0]
        button3 = [x for x in self.children if x.custom_id == 'H'][0]
        add = random.randrange(5, 10)
        add2 = random.randrange(5, 10)
        self.score += add
        self.score2 += add2
        self.shame += 1
        embed = discord.Embed(title='BJ', color=0x00ff00)

        embed.add_field(name="Your score:", value=f"{self.score}", inline=False)
        embed.add_field(name="Opponent's score:", value=f"{self.score2}", inline=False)
        embed.add_field(name="You won!", value="You reached 21 and bust your opponent", inline=False)

        embed2 = discord.Embed(title='BJ', color=15548997)
        embed2.add_field(name='You lost!', value='You went over 21 and got busted', inline=False)

        embed3 = discord.Embed(title='BJ', color=15548997)
        embed3.add_field(name="Your score:", value=f"{self.score}", inline=False)
        embed3.add_field(name="Opponent's score:", value=f"{self.score2}", inline=False)
        embed3.add_field(name="You lost!", value="Your Opponent reached 21", inline=False)

        em = discord.Embed(title='BJ', color=0x00ff00)
        em.add_field(name="Your score:", value=f"{self.score}", inline=False)
        em.add_field(name="Opponent's score:", value=f"{self.score2}", inline=False)
        em.add_field(name='You won!', value='Your Opponent went over 21', inline=False)

        embed4 = discord.Embed(title='BJ')
        embed4.add_field(name="Your score:", value=f"{self.score}", inline=False)
        embed4.add_field(name="Opponent's score:", value="?", inline=False)
        if self.score >= 22:
            button2.disabled = True
            button1.disabled = True
            button.disabled = True
            button3.disabled = True
            button3.disabled = True
            await interaction.response.edit_message(view=self, embed=embed2)
        elif self.score == 21:
            button2.disabled = True
            button1.disabled = True
            button.disabled = True
            button3.disabled = True
            await interaction.response.edit_message(view=self, embed=embed)
        if self.score2 >= 22:
            button2.disabled = True
            button1.disabled = True
            button.disabled = True
            button3.disabled = True
            button3.disabled = True
            await interaction.response.edit_message(view=self, embed=em)
        elif self.score2 == 21:
            button2.disabled = True
            button1.disabled = True
            button.disabled = True
            button3.disabled = True
            await interaction.response.edit_message(view=self, embed=embed3)
        elif self.shame == 2:
            button.disabled = True
            await interaction.response.edit_message(view=self, embed=embed4)
        else:
            await interaction.response.edit_message(view=self, embed=embed4)

    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message('Did you get lost pal?', ephemeral=True)
            return False
        else:
            return True

    @discord.ui.button(label='Stand', style=discord.ButtonStyle.blurple, custom_id='inspect')
    async def inspect_button_callback(self, button, interaction):
        button2 = [x for x in self.children if x.custom_id == 'move'][0]
        button1 = [x for x in self.children if x.custom_id == 'inspect'][0]
        button3 = [x for x in self.children if x.custom_id == 'H'][0]
        embed = discord.Embed(title='BJ', color=0x00ff00)
        embed.add_field(name="Your score:", value=f"{self.score}", inline=False)
        embed.add_field(name="Opponent's score:", value=f"{self.score2}", inline=False)
        embed.add_field(name="You won!", value="Your score was higher", inline=False)

        embed2 = discord.Embed(title='BJ', color=15548997)
        embed2.add_field(name="Your score:", value=f"{self.score}", inline=False)
        embed2.add_field(name="Opponent's score:", value=f"{self.score2}", inline=False)
        embed2.add_field(name="You lost!", value="Your Opponent's score was higher", inline=False)

        embed3 = discord.Embed(title='BJ', color=0x00ff00)
        embed3.add_field(name="Your score:", value=f"{self.score}", inline=False)
        embed3.add_field(name="Opponent's score:", value=f"{self.score2}", inline=False)
        embed3.add_field(name='Draw!', value='You got the same score with your Opponent', inline=False)

        if self.score2 > self.score:
            button2.disabled = True
            button1.disabled = True
            button.disabled = True
            button3.disabled = True
            await interaction.response.edit_message(view=self, embed=embed2)
        elif self.score > self.score2:
            button2.disabled = True
            button1.disabled = True
            button.disabled = True
            button3.disabled = True
            await interaction.response.edit_message(view=self, embed=embed)
        elif self.score == self.score2:
            button2.disabled = True
            button1.disabled = True
            button.disabled = True
            button3.disabled = True
            await interaction.response.edit_message(view=self, embed=embed3)

    @discord.ui.button(label='Forfeit', style=discord.ButtonStyle.blurple)
    async def end_button_callback(self, button, interaction):
        button2 = [x for x in self.children if x.custom_id == 'move'][0]
        button1 = [x for x in self.children if x.custom_id == 'inspect'][0]
        button3 = [x for x in self.children if x.custom_id == 'H'][0]
        button.disabled = True
        button1.disabled = True
        button2.disabled = True
        button3.disabled = True
        await interaction.response.edit_message(view=self)


@bot.command()
async def bj(ctx):
    view1 = MyView1(ctx, score=random.randrange(3, 21), score2=random.randrange(3, 21), shame=0)
    await ctx.send('Welcome to blackjack :)', view=view1)


async def open_account(user):
    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]['experience'] = 0
        users[str(user.id)]['upgrade'] = 0
        users[str(user.id)]['damage'] = 0
        users[str(user.id)]['code'] = 0
        users[str(user.id)]['Coins'] = 0
        users[str(user.id)]['things'] = 0
        users[str(user.id)]['Gem'] = 0
        users[str(user.id)]['level'] = 0
        users[str(user.id)]['health'] = 100
    with open('mainbank.py', 'w') as f:
        json.dump(users, f)
    return True


async def get_bank_data():
    with open('mainbank.py', 'r') as f:
        users = json.load(f)
    return users


@bot.command()
async def profile(ctx, user : discord.Member = None):
    await experience_converter(ctx)
    await open_account(ctx.author)
    users = await get_bank_data()

    if user == None:
        user = ctx.author

    wallet_amt = users[str(user.id)]['Coins']
    damage_amt = users[str(user.id)]['damage']
    level_amt = users[str(user.id)]['level']
    experience_amt = users[str(user.id)]['experience']
    gem_amt = users[str(user.id)]['Gem']
    health_amt = users[str(user.id)]['health']
    Weapon = ''
    Emoji = ''

    for item in mainshop:
        name = item["name"]
        code = item["code"]
        emoji = item["emoji"]
        Attack = item["Atk"]
        obj = [{"weapon_name": name, "code": code, "weapon_emoji": emoji, "Damage": Attack}]

        for item in obj:
            name_ = item["weapon_name"]
            obj_code = item["code"]
            emoji_stuff = item["weapon_emoji"]
            Damage_stuff = item["Damage"]

            if users[str(user.id)]['code'] == 0:
                Weapon = 'Nothing'
            elif users[str(user.id)]['code'] == obj_code:
                Weapon = name_
                Emoji = emoji_stuff
                users[str(user.id)]['damage'] = 0
                users[str(user.id)]['damage'] += Damage_stuff

    name = user.display_name
    pfp = user.display_avatar

    em9 = discord.Embed(title=f'{name} profile', colour=0xe67e22)
    em9.set_thumbnail(url=f'{pfp}')
    em9.add_field(name='Damage:', value=f'{damage_amt}⚔️', inline=False)
    em9.add_field(name='Level:', value=f'{level_amt}')
    em9.add_field(name='Coins:', value=f'${wallet_amt} <:pixilframe0:1035163208312426506>')
    em9.add_field(name='Weapon:', value=f'{Weapon}{Emoji}')
    em9.add_field(name='Gem:', value=f'{gem_amt} 💎')
    em9.add_field(name='Experience:', value=f'{experience_amt}')
    em9.add_field(name='Health:', value=f'{health_amt}/{health_amt}🩸')

    await ctx.send(embed=em9)


@bot.command()
async def starter(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    em0 = discord.Embed(title='_', colour=0xe67e22)
    em0.add_field(name='Error:', value='You already use your starter money!')

    em01 = discord.Embed(title='_', colour=0xe67e22)
    em01.add_field(name='_', value='Here is your starter coin of $500 :)')

    if users[str(user.id)]['things'] == 1:
        await ctx.send(embed=em0)
    else:
        users[str(user.id)]['things'] += 1
        users[str(user.id)]['Coins'] += 500

        await ctx.send(embed=em01)

    with open('mainbank.py', 'w') as f:
        json.dump(users, f)
    return True


async def experience_converter(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    experience = users[str(user.id)]['experience']
    level_start = users[str(user.id)]['level']
    level_end = int(experience ** (1 / 2))
    gain = level_end * 10
    level_gain = (level_end - level_start)

    if level_end > level_start:
        users[str(user.id)]['level'] += level_gain
        users[str(user.id)]['health'] += gain

    with open('mainbank.py', 'w') as f:
        json.dump(users, f)
    return True



mainshop = [
    {"name": "Medieval Axe", "price": 85, "code": 9382, "emoji": "<:Medieval_Axe:1054958856188465213>",
     "Atk": 70},
    {"name": "The Sorcerer Staff", "price": 3750, "code": 3827, "emoji": "<:pixilframe01:1034710260050575381>",
     "Atk": 500},
    {"name": "The Axe", "price": 75, "code": 4009, "emoji": "<:PlainAxe:1034798734770458654>", "Atk": 45},
    {"name": "Iron Sword", "price": 120, "code": 3145, "emoji": "<:CrystalKatana:1034800001353781248>", "Atk": 85},
    {"name": "Holy Knight Sword", "price": 1160, "code": 3142, "emoji": "<:Holy_Knight_Sword:1038340050137657354>",
     "Atk": 200},
    {"name": "Wooden Sword", "price": 50, "code": 6969, "emoji": "<:Wooden_sword:1054957450278740108>", "Atk": 25},
    {"name": "Sea Glide", "price": 1000, "code": 4231, "emoji": "<:Sea_Powered:1039173704510349393>", "Atk": 175}
]


@bot.command()
async def weaponshop(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    await open_location(ctx.author)
    users1 = await get_xy_data()

    e = discord.Embed(title='Weapon Shop:', colour=0xe67e22)
    e.add_field(name='_', value='You do not have enough money.')

    e1 = discord.Embed(title='Weapon Shop:', colour=0xe67e22)
    e1.add_field(name='_', value='You already have a weapon.')

    select = Select(
        placeholder='Choose a weapon',
        options=[
            discord.SelectOption(
                label='Iron Sword',
                emoji='<:CrystalKatana:1034800001353781248>',
                description='$120'
            ),
            discord.SelectOption(
                label='Wooden Sword',
                emoji='<:Wooden_sword:1054957450278740108>',
                description='$50'
            ),
            discord.SelectOption(
                label='Medieval Axe',
                emoji='<:Medieval_Axe:1054958856188465213>',
                description='$2500'
            ),
            discord.SelectOption(
                label='The Axe',
                emoji='<:PlainAxe:1034798734770458654>',
                description='$75'
            ),
            discord.SelectOption(
                label='The Sorcerer Staff',
                emoji='<:pixilframe01:1034710260050575381>',
                description='$3750'
            ),
            discord.SelectOption(
                label='Holy Knight Sword',
                emoji='<:Holy_Knight_Sword:1038340050137657354>',
                description='$1160'
            ),
            discord.SelectOption(
                label='Sea Glide',
                emoji='<:Sea_Powered:1039173704510349393>',
                description='$1000'
            )
        ])

    async def my_callback(interaction):

        for item in mainshop:
            name = item["name"]
            price = item["price"]
            code = item["code"]
            atk = item["Atk"]
            obj = [{"priceamt": price, "code": code, "atk": atk}]

            if select.values[0] == name:
                if interaction.user != ctx.author:
                    await interaction.response.send_message('Did you get lost pal?', ephemeral=True)
                    return False
                else:
                    for things in obj:
                        priceamt = things["priceamt"]
                        code = things["code"]
                        atk = things["atk"]
                        if users[str(user.id)]['code'] > 0:
                            await interaction.response.send_message(embed=e1)
                        else:
                            if users[str(user.id)]['Coins'] < priceamt:
                                await interaction.response.send_message(embed=e)
                            else:
                                users[str(user.id)]['code'] += code
                                users[str(user.id)]['Coins'] -= priceamt
                                users[str(user.id)]['damage'] += atk

                                e2 = discord.Embed(title='Weapon Shop:', colour=0xe67e22)
                                e2.add_field(name='Cost:', value=f'{priceamt}🪙')
                                e2.add_field(name='Weapon:', value=f'{select.values[0]}⚔')
                                e2.add_field(name='Code:', value=f'{code}✅')
                                e2.add_field(name='_', value='Thank you for shopping here.')

                                await interaction.response.send_message(embed=e2)

                                with open('mainbank.py', 'w') as f:
                                    json.dump(users, f)
                                return True

    select.callback = my_callback
    viewx = View()
    viewx.add_item(select)

    if users1[str(user.id)]['x'] != 151:
        await ctx.send('You are not near any villages')
    else:
        if users1[str(user.id)]['y'] != 72:
            await ctx.send('You are not near any villages')
        else:
            await ctx.send(view=viewx)

    with open('Coordinates.py', 'w') as f:
        json.dump(users1, f)
    return True


@bot.command()
async def sell(ctx, select):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    select = str(select)

    for item in mainshop:
        price = item["price"]
        code = item["code"]
        name = item["name"]
        obj = [{"priceamt": price, "code": code}]

        if select == name:
            for things in obj:
                price = things["priceamt"]
                code = things["code"]

                if users[str(user.id)]['code'] != code:
                    await ctx.send(f'You do not have {select}')
                else:
                    embedg = discord.Embed(title='Selling...')
                    embedg.add_field(name='_', value=f'<@{ctx.author.id}>, You sold {select} for ${price}')

                    users[str(user.id)]['code'] = 0
                    users[str(user.id)]['Coins'] += price
                    users[str(user.id)]['damage'] = 0
                    users[str(user.id)]['upgrade'] = 0
                    await ctx.send(embed=embedg)

    with open('mainbank.py', 'w') as f:
        json.dump(users, f)
    return True


@bot.command()
async def travel(ctx, x, y):
    await open_location(ctx.author)
    user = ctx.author
    users1 = await get_xy_data()

    x = int(x)
    y = int(y)

    for item in mainlocation:
        xcoord = item["x"]
        ycoord = item["y"]
        embed = item["embed"]
        obj = [{"xlocation": xcoord, "ylocation": ycoord, "embedlocation": embed}]
        if x == xcoord:
            if y == ycoord:
                users1[str(user.id)]['x'] = 0
                users1[str(user.id)]['y'] = 0
                for things in obj:
                    embedlocation = things["embedlocation"]
                    users1[str(user.id)]['x'] += x
                    users1[str(user.id)]['y'] += y

                    await ctx.send(embed=embedlocation)

    with open('Coordinates.py', 'w') as f:
        json.dump(users1, f)
    return True


async def open_location(user):
    users1 = await get_xy_data()

    if str(user.id) in users1:
        return False
    else:
        users1[str(user.id)] = {}
        users1[str(user.id)]['x'] = 0
        users1[str(user.id)]['y'] = 0
    with open('Coordinates.py', 'w') as f:
        json.dump(users1, f)
    return True


async def get_xy_data():
    with open('Coordinates.py', 'r') as f:
        users1 = json.load(f)
    return users1


class MyView4(View):

    def __init__(self, ctx,
                 user,
                 users,
                 enemy_health,
                 enemy_name,
                 damage_enemy,
                 player_health,
                 image_e,
                 experience_gain
                 ):
        super().__init__()
        self.ctx = ctx  # specify ctx
        self.user = user  # specify
        self.users = users  # specify users
        self.enemy_health = enemy_health  # specify enemy's health
        self.enemy_name = enemy_name
        self.damage_enemy = damage_enemy
        self.player_health = player_health
        self.image_enemy = image_e
        self.experience_gain = experience_gain

    @discord.ui.button(label='Attack!', style=discord.ButtonStyle.danger, emoji='🔪', custom_id='H')  # create a button
    async def button_callback_hi(self, button, interaction):  # name the interaction
        await open_account(self.ctx.author)  # open account
        attack_dmg = self.users[str(self.user.id)]['damage']  # set player's attack damage
        random_dmg = random.randrange(attack_dmg)  # set a random damage
        enemy_random_dmg = random.randrange(self.damage_enemy)

        self.enemy_health -= random_dmg
        self.player_health -= enemy_random_dmg

        constant_health = self.users[str(self.user.id)]['health']

        status = discord.Embed(title='KILL THE ENEMY!', colour=0xe67e22)
        status.set_thumbnail(url=self.image_enemy)
        status.add_field(name=f'{self.enemy_name}\'s health', value=f'{self.enemy_health}🩸')
        status.add_field(name=f'{self.enemy_name}\'s attack damage', value=f'{enemy_random_dmg}⚔')
        status.add_field(name='Your health:', value=f'{self.player_health}/{constant_health}🩸', inline=False)
        status.add_field(name='Your attack damage:', value=f'{random_dmg}⚔', inline=True)

        status2 = discord.Embed(title='KILL THE ENEMY')
        status2.add_field(name=f'{self.enemy_name}', value='0🩸')

        status3 = discord.Embed(title='You died')
        status3.add_field(name='Penalty:', value='Lose all coins and weapons')

        if self.player_health <= 0:
            self.users[str(self.user.id)]['Coins'] = 0
            self.users[str(self.user.id)]['damage'] = 0
            self.users[str(self.user.id)]['code'] = 0
            self.users[str(self.user.id)]['upgrade'] = 0
            await interaction.response.edit_message(view=self, embed=status3)
        else:
            if self.enemy_health <= 0:
                self.users[str(self.user.id)]['experience'] += self.experience_gain
                button.disabled = True
                await interaction.response.edit_message(view=self, embed=status2)
            else:
                await interaction.response.edit_message(view=self, embed=status)

        with open('mainbank.py', 'w') as f:
            json.dump(self.users, f)
        return True


@bot.command()
async def fight(ctx, enemy_choose):
    global health_enemy, name_enemy, enemy_damage, enemy_image, xp_enemy, xp_enemy
    await open_account(ctx.author)
    await open_location(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    users1 = await get_xy_data()

    url = user.display_avatar

    health_player = users[str(user.id)]['health']

    for item in enemy_record:
        name = item["enemy"]
        health = item["health"]
        damage = item["damage"]
        image = item["image"]
        exp = item["exp"]
        obj = [
            {"enemy_name": name, "health_enemy": health, "enemy_damage": damage, "image_enemy": image, "enemy_xp": exp}]
        if enemy_choose == name:
            for things in obj:
                name_enemy = things["enemy_name"]
                health_enemy = things["health_enemy"]
                enemy_damage = things["enemy_damage"]
                enemy_image = things["image_enemy"]
                xp_enemy = things["enemy_xp"]

    view4 = MyView4(ctx, user=ctx.author,
                    users=await get_bank_data(),
                    enemy_health=health_enemy,
                    enemy_name=name_enemy,
                    damage_enemy=enemy_damage,
                    player_health=health_player,
                    image_e=enemy_image,
                    experience_gain=xp_enemy
                    )  # create a button view

    status = discord.Embed(title='KILL THE ENEMY!', colour=0xe67e22)
    status.set_author(name=f'Requested by {user}', icon_url=url)
    status.set_thumbnail(url=enemy_image)
    status.add_field(name=f'{name_enemy}:', value=f'{health_enemy}🩸')
    status.add_field(name='You:', value=f'{health_player}/{health_player}🩸')

    if users1[str(user.id)]['x'] != 32:
        await ctx.send(f'<@{ctx.author.id}> You are not near areas that has enemies.')
    else:
        if users1[str(user.id)]['y'] != 125:
            await ctx.send(f'<@{ctx.author.id}> You are not near areas that has enemies.')
        else:
            await ctx.send(f'<@{ctx.author.id}>', view=view4, embed=status)


async def open_inventory(user):
    users2 = await get_bag_data()

    if str(user.id) in users2:
        return False
    else:
        users2[str(user.id)] = {}
        users2[str(user.id)]['toolkit'] = 0
        users2[str(user.id)]['Scraps'] = 0
        users2[str(user.id)]['Schematic'] = 0
        users2[str(user.id)]['fish'] = 0
        users2[str(user.id)]['bread'] = 0
        users2[str(user.id)]['beef'] = 0
        users2[str(user.id)]['pork'] = 0
        users2[str(user.id)]['Wheat'] = 0
        users2[str(user.id)]['Gem'] = 0
        users2[str(user.id)]['Books'] = 0
        users2[str(user.id)]['Ancient_Medallions'] = 0
        users2[str(user.id)]['FishingRod'] = 0
        users2[str(user.id)]['Shovel'] = 0
    with open('Inventory.py', 'w') as f:
        json.dump(users2, f)
    return True


async def get_bag_data():
    with open('Inventory.py', 'r') as f:
        users2 = json.load(f)
    return users2


async def inventory_sorter(ctx):
    await open_inventory(ctx.author)
    user = ctx.author
    users2 = await get_bag_data()

    Toolkit = users2[str(user.id)]['toolkit']
    Scraps = users2[str(user.id)]['Scraps']
    Guide = users2[str(user.id)]['Schematic']
    Fish = users2[str(user.id)]['fish']
    Bread = users2[str(user.id)]['bread']
    Beef = users2[str(user.id)]['beef']
    Pork = users2[str(user.id)]['pork']
    Book = users2[str(user.id)]['Books']
    Ancient_Medallions = users2[str(user.id)]['Ancient_Medallions']
    FishingRod = users2[str(user.id)]['FishingRod']
    Shovel = users2[str(user.id)]['Shovel']



    Upgrade_resource_count = Scraps + Guide + Toolkit + FishingRod + Ancient_Medallions + Fish + Bread + Beef + Book + Shovel + Pork
    pfp = ctx.author.display_avatar

    resource = [
        {
            "name": "Scraps", "amount": Scraps
        },
        {
            "name": "Toolkit", "amount": Toolkit
        },
        {
            "name": "Schematic", "amount": Guide
        },
        {
            "name": "Fish", "amount": Fish
        },
        {
            "name": "Bread", "amount": Bread
        },
        {
            "name": "Beef", "amount": Beef
        },
        {
            "name": "Pork", "amount": Pork
        },
        {
            "name": "Books", "amount": Book
        },
        {
            "name": "Ancient Medallions", "amount": Ancient_Medallions
        },
        {
            "name": "FishingRod", "amount": FishingRod
        },
        {
            "name": "Shovel", "amount": Shovel
        }
    ]

    global inventory_embed
    inventory_embed = discord.Embed(title=f'{ctx.author}\'s embed')
    inventory_embed.set_thumbnail(url=pfp)

    for i in resource:
        name = i["name"]
        amount = i["amount"]
        obj = [{"name": name, "amount": amount}]
        for x in obj:
            obj_name = x["name"]
            obj_amount = x["amount"]
            if Upgrade_resource_count == 0:
                continue
            else:
                if obj_amount == 0:
                    continue
                else:
                    inventory_embed.add_field(name=f'{obj_name}', value=f'{obj_amount}')


@bot.command(aliases=['inv', 'invent'])
async def inventory(ctx):
    await inventory_sorter(ctx)
    await ctx.send(embed=inventory_embed)



class MyView5(View): # A button class object

    def __init__(self, ctx, user, users, users2): # Adding variables to the class
        super().__init__()
        self.ctx = ctx
        self.user = user
        self.users = users
        self.users2 = users2

    @discord.ui.button(label='Upgrade', style=discord.ButtonStyle.blurple, emoji='🔛', custom_id='H') # Adding a button to the class
    async def button_callback_hi(self, button, interaction): # An async defined button_callback func that responds to interactions
        await open_account(self.ctx.author)
        await open_inventory(self.ctx.author)
        scrap = round(price_ / 10) * weapon_level_new # Variables
        toolkit = round(price_ / 20) * weapon_level_new
        guide = 1


        if self.users2[str(self.user.id)]['Scraps'] < scrap: #Requirements
            await interaction.response.edit_message(embed=embedg, view=self)
        else:
            if self.users2[str(self.user.id)]['toolkit'] < toolkit:
                await interaction.response.edit_message(embed=embedg, view=self)
            else:
                if self.users2[str(self.user.id)]['Schematic'] < guide:
                    await interaction.response.edit_message(embed=embedg, view=self)
                else:
                    self.users2[str(self.user.id)]['Scraps'] -= scrap
                    self.users2[str(self.user.id)]['toolkit'] -= toolkit
                    self.users2[str(self.user.id)]['Schematic'] -= guide
                    await upgrade_weapon(self.ctx)
                    new_level = self.users[str(self.user.id)]['upgrade'] + 1
                    embed_success = discord.Embed(title='Upgrade Success!', color=0x00ff00)
                    embed_success.add_field(name='Weapon Level:', value=f'{new_level}')
                    button.disabled = True
                    await interaction.response.edit_message(view=self, embed=embed_success) # Requirements

                    with open('Inventory.py', 'w') as f:
                        json.dump(self.users2, f)
                    return False

    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message('Did you get lost pal?', ephemeral=True)
            return False
        else:
            return True


async def upgrade_weapon(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    damage_up = round(price_ / 15) * weapon_level_new

    users[str(user.id)]['damage'] += damage_up
    users[str(user.id)]['upgrade'] += 1

    with open('mainbank.py', 'w') as f:
        json.dump(users, f)
    return True







@bot.command()
async def upgrade(ctx, select):
    global embedg # Permitting the variable the ability to be use anywhere
    global price_
    global weapon_level_new
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    view5 = MyView5(ctx, user=ctx.author, users=await get_bank_data(), users2=await get_bag_data())

    url = user.display_avatar

    weapon_level_org = users[str(user.id)]['upgrade']
    weapon_level_new = users[str(user.id)]['upgrade'] + 1

    for item in mainshop:
        price = item["price"]
        code = item["code"]
        name = item["name"]
        emoji = item["emoji"]
        obj = [{"priceamt": price, "code": code, "emoji": emoji}]


        if select == name:
            for things in obj:
                price_ = things["priceamt"]
                code = things["code"]
                emoji = things["emoji"]

                scrap = round(price_ / 10) * weapon_level_new  # Variables
                toolkit = round(price_ / 20) * weapon_level_new
                guide = 1

                if users[str(user.id)]['code'] != code:
                    await ctx.send(f'You do not have {select}')
                else:
                    embedg = discord.Embed(title=f'<@{ctx.author}> Upgrade Station')
                    embedg.set_author(name=f'Requested by {ctx.author}', icon_url=url)
                    embedg.add_field(name='Weapon\'s Name:', value=f'{select}{emoji}')
                    embedg.add_field(name='Weapon\'s Code:', value=f'{code}')
                    embedg.add_field(name='Weapon\'s Current Level:', value=f'{weapon_level_org}')
                    embedg.add_field(name='Weapon upgrade level goal:', value=f'{weapon_level_new}')
                    embedg.add_field(name='Scraps needed:', value=f'{scrap}')
                    embedg.add_field(name='Toolkits needed:', value=f'{toolkit}')
                    embedg.add_field(name='Schematic needed:', value=f'{guide}')
                    await ctx.send(embed=embedg, view=view5)






@bot.command()
async def gift(ctx, amount : int, item, user2 : discord.Member = None):
    await open_inventory(ctx.author)
    user = ctx.author
    users2 = await get_bag_data()

    try:

        if users2[str(user.id)][item] < amount:
            await ctx.send(f'You do not have {amount} {item} <@{ctx.author.id}>')
        else:
            embed_gift = discord.Embed(title='Gifts')
            embed_gift.set_thumbnail(url='https://cdn.discordapp.com/attachments/1055036823740612672/1055124153595875378/pixil-frame-0_7.png')
            embed_gift.add_field(name=f'{ctx.author} sent you a gift.', value=f'The gift contain {amount} {item}')

            users2[str(user.id)][item] -= amount
            users2[str(user2.id)][item] += amount
            await ctx.send(f'<@{user2.id}>', embed=embed_gift)


    except:
        await ctx.send(f'Item {item} does not exist.')


    with open('Inventory.py', 'w') as f:
        json.dump(users2, f)
    return True


Market_image = 'https://cdn.discordapp.com/attachments/1032198460767744064/1055472626212020255/image.png'


async def market_profit(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    users[str(user.id)]['Coins'] += Grand_total
    users[str(user.id)]['Coins'] -= 65

    with open('mainbank.py', 'w') as f:
        json.dump(users, f)
    return True


async def market_fail(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    users[str(user.id)]['Coins'] -= 65

    with open('mainbank.py', 'w') as f:
        json.dump(users, f)
    return True

Link_embed = 'https://cdn.discordapp.com/attachments/1032198460767744064/1055672625726226452/image.png'

@bot.command()
async def market(ctx, select, cost, amount):
    cost = int(cost)
    amount = int(amount)
    await open_inventory(ctx.author)
    await open_account(ctx.author)
    await open_location(ctx.author)
    user = ctx.author
    users2 = await get_bag_data()
    users = await get_bank_data()
    users1 = await get_xy_data()

    global Grand_total

    Grand_total = cost*amount

    embed_crash = discord.Embed(title='Market', colour=0x00ff00)
    embed_crash.set_thumbnail(url=Link_embed)
    embed_crash.add_field(name='Market result:', value=f'You made a grand total of ${Grand_total}')
    embed_crash.add_field(name='Cost of starting a shop in the market:', value='$65')
    embed_crash.add_field(name=f'{select} sold:', value=f'{amount}.')

    embed_fail = discord.Embed(title='Market', colour=15548997)
    embed_fail.set_thumbnail(url=Link_embed)
    embed_fail.add_field(name='Market result:', value=f"Your neighbour sold the same product but cheaper so no one bought it from you.")
    embed_fail.add_field(name='Cost of starting a shop in the market:', value='$65')

    if users1[str(user.id)]['x'] != 151:
        await ctx.send('You need to be in a village to use the market command.')
    else:
        if users1[str(user.id)]['y'] != 72:
            await ctx.send('You need to be in a village to use the market command.')
        else:
            if users[str(user.id)]['Coins'] < 65:
                await ctx.send('You do not have enough money to start a shop.')
            else:
                for i in market_list:
                    cost_org = i["price"]
                    m_item = i["Market Item"]
                    obj = [{"m_item": m_item, "cost_org": cost_org}]

                    if select == m_item:
                        for foo in obj:
                            foo_item = foo["m_item"]
                            foo_cost = foo["cost_org"]
                            chance = random.randrange(foo_cost)
                            chance_user = random.randrange(cost)
                            if chance_user > chance:
                                await market_fail(ctx)
                                await ctx.send(f'<@{ctx.author.id}>', embed=embed_fail)
                            else:
                                users2[str(user.id)][select] -= amount
                                await market_profit(ctx)
                                await ctx.send(f'<@{ctx.author.id}>', embed=embed_crash)

    with open('Inventory.py', 'w') as f:
        json.dump(users2, f)
    return True




async def buy_item(ctx, cost : int, amt : int):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    tot = cost*amt
    users[str(user.id)]['Coins'] -= tot

    with open('mainbank.py', 'w') as f:
        json.dump(users, f)
    return True



@bot.command()
async def buy(ctx, item, amount):
    await open_inventory(ctx.author)
    await open_account(ctx.author)
    user = ctx.author
    users2 = await get_bag_data()
    users = await get_bank_data()
    amount = int(amount)

    embed = discord.Embed(title='Shop Receipt')
    embed.add_field(name=f'You bought {amount} {item}', value='_ _')


    for i in buy_able:
        Market_Item = i["Market Item"]
        price = i["price"]
        obj = [{'Market Item': Market_Item, 'price': price}]
        if item == Market_Item:
            for x in obj:
                Market_Item_ = x['Market Item']
                price_ = x['price']
                price_ = int(price_)
                pricetot = price_ * amount
                if users[str(user.id)]['Coins'] < pricetot:
                    await ctx.send('You do not have enough money.')
                else:
                    users2[str(user.id)][Market_Item_] += amount
                    await buy_item(ctx, price_, amount)
                    await ctx.send(embed=embed)

    with open('Inventory.py', 'w') as f:
        json.dump(users2, f)
    return True

@bot.command()
async def help(ctx, command=None):

    url = ctx.author.display_avatar

    mainhelp = discord.Embed(title=f'A help embed')
    mainhelp.set_author(name=f'Requested by {ctx.author}', icon_url=url)
    mainhelp.add_field(name='Moderation Commands:', value='`clear` `tempban` `kick` `unban`')
    mainhelp.add_field(name='Fun Commands:', value='`8ball` `bj`')
    mainhelp.add_field(name='General Commands:', value='`ping`')
    mainhelp.add_field(name='Entertainment Commands:', value='`profile` `starter` `weaponshop` `sell` `travel` `fight` '
                                                             '`inventory` `upgrade` `gift` `market` `buy` `shop` `search` '
                                                             '`marketinfo`')
    for data in Cmd:
        Command = data['Command']
        info = data['info']
        Requirements: str = data['Requirements']

        obj = [{"Command": Command, "info": info, "Requirements": Requirements}]
        if command == Command:
            for data_ in obj:
                Command_ = data_['Command']
                info_ = data_['info']
                Requirements = data_['Requirements']
                help = discord.Embed(title='A help embed')
                help.add_field(name=f'{Command_}', value=f'{info_}, requirements: {Requirements}')
                await ctx.send(embed=help)
    if command == None:
        await ctx.send(embed=mainhelp)


@bot.command()
async def marketinfo(ctx):
    url = ctx.author.display_avatar
    market_embed = discord.Embed(title='Market Item List')
    market_embed.set_author(name=f'Requested by {ctx.author}', icon_url=url)
    for i in market_list:
        Market_Item = i["Market Item"]
        Price = i["price"]
        market_embed.add_field(name=f'{Market_Item}', value=f'${Price}')
    await ctx.send(embed=market_embed)


@bot.command()
async def shop(ctx):
    url = ctx.author.display_avatar
    shop_embed = discord.Embed(title='Shop List')
    shop_embed.set_author(name=f'Requested by {ctx.author}', icon_url=url)
    for i in buy_able:
        Market_Item = i["Market Item"]
        Price = i["price"]
        shop_embed.add_field(name=f'{Market_Item}', value=f'${Price}')
    await ctx.send(embed=shop_embed)



@bot.command()
@commands.cooldown(1,20,commands.BucketType.user)
async def search(ctx):
    await open_location(ctx.author)
    await open_inventory(ctx.author)
    user = ctx.author
    users1 = await get_xy_data()
    users2 = await get_bag_data()

    death_chance = random.randrange(15)

    Scrap_add = random.randrange(20)

    if users1[str(user.id)]['x'] != 200:
        await ctx.send('You are not near forests to search.')
    else:
        if users1[str(user.id)]['y'] != 21:
            await ctx.send('You are not any near forests to search.')
        else:
            if death_chance == 5:
                await instant_death(ctx)
                await ctx.send('You died mysteriously, your death penalty was losing all coins and weapons.')
            else:
                users2[str(user.id)]['Scraps'] += Scrap_add
                await ctx.send(f'<@{ctx.author.id}> You found {Scrap_add} scraps while searching in the woods.')

    with open('Inventory.py', 'w') as f:
        json.dump(users2, f)
    return True


async def instant_death(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    users[str(user.id)]['Coins'] = 0
    users[str(user.id)]['code'] = 0
    users[str(user.id)]['damage'] = 0
    users[str(user.id)]['upgrade'] = 0

    with open('mainbank.py', 'w') as f:
        json.dump(users, f)
    return True



@bot.command()
async def fish(ctx):
    await open_inventory(ctx.author)
    await open_location(ctx.author)
    user = ctx.author
    users2 = await get_bag_data()
    users1 = await get_xy_data()

    fishing_luck = random.randrange(15)
    death_luck = random.randrange(20)

    if users1[str(user.id)]['x'] != 252:
        await ctx.send('You are not near places with fishes to fish.')
    else:
        if users1[str(user.id)]['y'] != 59:
            await ctx.send('You are not near places with fishes to fish')
        else:
            if death_luck == 2:
                await instant_death(ctx)
                await ctx.send('You died and your death penalty was losing all coins and weapons.')
            else:
                if users2[str(user.id)]['FishingRod'] < 1:
                    await ctx.send('You need a fishing rod.')
                else:
                    if fishing_luck == 5:
                        users2[str(user.id)]['fish'] += 1
                        await ctx.send('You caught a pretty heavy fish.')
                    else:
                        await ctx.send(f'No fish was caught. Better luck next time.')
    


    
    with open('Inventory.py', 'w') as f:
        json.dump(users2, f)
    return True



@bot.command()
async def finish(ctx):
    await open_account(ctx.author)
    await open_inventory(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    users2 = await get_bag_data()

    if users[str(user.id)]['level'] >= 35:
        if users[str(user.id)]['damage'] >= 1000:
            if users[str(user.id)]['health'] >= 1000:
                if users2[str(user.id)]['Ancient_Medallions'] >= 3:
                    await ctx.send('You finished it.')
            
            



# Enter your bot's token here
bot.run('MTAwNjA0NTExNTc3MDQ3ODU5Mw.GYg1XD.gixE6G4Yvqk4T8NE3vxVq7BfKsXbZWaQ5KOOzo')