
import requests
from flag_dict import flag_dict
import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from nextcord import File, ButtonStyle
from nextcord.ui import Button, View

from random import randrange
import unidecode
# ---------------------------------------------------------------------------------------------------------------------------------------------#
def flag_output():
    # This function randomises the output of the flag!
    flag_intial_list = list(flag_dict.keys())
    random_index = randrange(len(flag_intial_list))

    flag_initial_url_input = flag_intial_list[random_index]
    flag_name_original = flag_dict[flag_initial_url_input]
    flag_name = flag_name_original

    if type(flag_name) == list:
        for i in range(len(flag_name)):
            flag_name[i] = unidecode.unidecode(flag_name[i])
    else:
        flag_name = unidecode.unidecode(flag_name)

    url = f'https://flagcdn.com/w320/{flag_initial_url_input}.png'

    with open('file.png', 'wb') as f:
        f.write(requests.get(url).content)

    return url, flag_name, flag_initial_url_input, flag_name_original
# ---------------------------------------------------------------------------------------------------------------------------------------------#
def input_checker(message):
    # Checks to see if the message inputteed mathces the correct answer
    def sentenceCapitalization(string):
                    # This function takes a sentence/phrase from the original user inputted message and makes the
                    # first letter of each word capital.
                    string_split = string.split(' ')
                    concatenated_string = ''
                    for word in string_split:
                        concatenated_string += str(word.capitalize() + ' ')
                    return concatenated_string.strip()
    if type(message) == list:
        p = []
        for word in message:
            p.append(sentenceCapitalization(word))
            p.append(word.upper())
            p.append(word.lower())
            p.append(word.capitalize())
        return p
    else:
        
        message_1 = sentenceCapitalization(message)
        message_2 = message.upper()
        message_3 = message.lower()
        message_4 = message.capitalize()
        return [message_1,message_2,message_3,message_4]
# ---------------------------------------------------------------------------------------------------------------------------------------------#
# This function initalises the flag game
intents = nextcord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix = '!',intents = intents)
score_dict = {}
@client.event
async def on_ready():
    await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name='!flag or !flag-team'))

# This commnad opens 
@client.command(name = 'flag')
async def flag(ctx):
    alive = True
    score = 0
    flag_dict_temp = flag_dict
    temp_storage_dict = {}
    guild = ctx.message.guild
    print(ctx.message.author)
    channel_test = nextcord.utils.get(guild.channels, name='lopez4816')
    if channel_test is None:
        channel_name = ctx.author
        new_channel = await guild.create_text_channel(f'{channel_name}')
        print(new_channel)
    else:
        new_channel = channel_test

    while alive == True:
       
        url, flag_name, flag_initial_url_input, flag_name_original = flag_output()
        await new_channel.send(url)
        print(flag_name)
        msg = await client.wait_for('message', check=lambda message: message.author == ctx.author and message.channel == new_channel)
        print(type(msg.author.name))
        check_list = input_checker(flag_name)

        print(check_list)
        
        if msg.content in check_list:
            temp_storage_dict[flag_initial_url_input] = flag_dict[flag_initial_url_input]
            del flag_dict_temp[flag_initial_url_input]
            await new_channel.send('Correct!')
            score += 1
            print(len(flag_dict_temp.keys()))
            print(temp_storage_dict)
        else:
            try:
                flag_name_for_url = flag_name_original.replace(' ','_')
            except:
                flag_name_for_url = flag_name_original[0].replace(' ','_')
            await new_channel.send(f'Incorrect it was **{flag_name_original}**! \n**Final Score: {score}** \nFind out more about **{flag_name_original}** at: https://en.wikipedia.org/wiki/{flag_name_for_url} \n \n Type **!flag** or **!flag-team**')
            if msg.author.name in list(score_dict.keys()):
                if score_dict[msg.author.name] < score:
                    score_dict[msg.author.name] = score
                else:
                    pass
            else:
                score_dict[msg.author.name] = score
            
            alive = False
            print(score_dict)
            flag_dict_temp.update(temp_storage_dict)

            playagain_button_yes = Button(label = 'Yes',style = ButtonStyle.green)
            async def button_interaction_yes(interaction):
                await interaction.response.send_message("** Let's go! **")
                await team(ctx)

            playagain_button_no = Button(label = 'No',style = ButtonStyle.red)

            async def button_interaction_no(interaction):
                await interaction.response.send_message("** See you soon! **")

            playagain_button_yes.callback = button_interaction_yes
            playagain_button_no.callback = button_interaction_no

            myview = View(timeout=180)
            myview.add_item(playagain_button_yes)
            myview.add_item(playagain_button_no)

            await new_channel.send('\n**Play again?**',view=myview)
# ---------------------------------------------------------------------------------------------------------------------------------------------#
@client.command(name = 'flag-team')
async def team(ctx):
    alive = True
    score = 0
    flag_dict_temp = flag_dict
    temp_storage_dict = {}
    guild = ctx.message.guild

    while alive == True:
       
        url, flag_name, flag_initial_url_input, flag_name_original = flag_output()
        await ctx.send(url)
        print(flag_name)
        msg = await client.wait_for('message', check=lambda message: message.author == ctx.author)
        print(type(msg.author.name))
        check_list = input_checker(flag_name)

        print(check_list)
        
        if msg.content in check_list:
            temp_storage_dict[flag_initial_url_input] = flag_dict[flag_initial_url_input]
            del flag_dict_temp[flag_initial_url_input]
            await ctx.send('Correct!')
            score += 1
            print(len(flag_dict_temp.keys()))
            print(temp_storage_dict)
        else:
            try:
                flag_name_for_url = flag_name_original.replace(' ','_')
            except:
                flag_name_for_url = flag_name_original[0].replace(' ','_')
            await ctx.send(f'Incorrect it was **{flag_name_original}**! \n**Final Score: {score}** \nFind out more about **{flag_name_original}** at: https://en.wikipedia.org/wiki/{flag_name_for_url} \n \n Type **!flag** or **!flag-team**')
            if 'team' in list(score_dict.keys()):
                if score_dict['team'] < score:
                    score_dict['team'] = score
                else:
                    pass
            else:
                score_dict['team'] = score
            
            alive = False
            print(score_dict)
            flag_dict_temp.update(temp_storage_dict)
            
            
            
            playagain_button_yes = Button(label = 'Yes',style = ButtonStyle.green)
            async def button_interaction_yes(interaction):
                await interaction.response.send_message("** Let's go! **")
                await team(ctx)

            playagain_button_no = Button(label = 'No',style = ButtonStyle.red)

            async def button_interaction_no(interaction):
                await interaction.response.send_message("** See you soon! **")

            playagain_button_yes.callback = button_interaction_yes
            playagain_button_no.callback = button_interaction_no

            myview = View(timeout=180)
            myview.add_item(playagain_button_yes)
            myview.add_item(playagain_button_no)

            await ctx.send('\n**Play again?**',view=myview)
# ---------------------------------------------------------------------------------------------------------------------------------------------#
@client.command(name = 'leaderboard')
async def leaderboard(ctx):
    score_dict_order = {k: v for k, v in sorted(score_dict.items(), key=lambda item: item[1],reverse=True)}
    score_dict_key = list(score_dict_order.keys())
    score_dict_value = list(score_dict_order.values())
    mystring = ''
    for i in range(len(score_dict_key)):
        mystring += f'\n**{score_dict_key[i]}: {score_dict_value[i]}**' 
    await ctx.send('**Flag-Bot Leaderboard:**'+'\n---------------' + mystring)
    # await ctx.send(f'**Flag Leaderboard:** \n{score_dict_order}')
        
client.run('discord-token-here')
# ---------------------------------------------------------------------------------------------------------------------------------------------#

