# Flag Guessing game in Discord
# ---------------------------------------------------------------------------------------------------------------------------------------------#
# Imports
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
# Flag Output Function
# This function is used to collect a flag from the flag API along with its name.
# This is what the user will guess from...
def flag_output():
    # Search through all the keys in the flag dictionary 
    flag_intial_list = list(flag_dict.keys())
    # Choose a random index from the length of the flag dictionary
    random_index = randrange(len(flag_intial_list))
    # Collect the flag's abbreviated name (used to collect the flag image from the API) 
    flag_initial_url_input = flag_intial_list[random_index]
    # Collect the flag's original name in  full
    flag_name_original = flag_dict[flag_initial_url_input]
    # Storing the flag's name
    flag_name = flag_name_original

    # Checks to see if there are multiple accepted answers for the flag's name
    if type(flag_name) == list:
        for i in range(len(flag_name)):
            flag_name[i] = unidecode.unidecode(flag_name[i])
    else:
        flag_name = unidecode.unidecode(flag_name)

    # The URL used to collect the image of the flag
    url = f'https://flagcdn.com/w320/{flag_initial_url_input}.png'

    # This function returns:
        # url: the url to collect the flag
        # flag_name: the name/s of the flag after being "unidecoded"
        # flag_initial_url_input: the abbravaiated name for the flag as stored in the flag dictionary
        # flag_name_original: the original name/s of the flag
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
# This section is used to initialise and play the flag guessing game

# Intialisation of the Nextcord module
intents = nextcord.Intents.default()
intents.message_content = True

#  Defining the prefix for our discord commands, in this case I used '!'
client = commands.Bot(command_prefix = '!',intents = intents)
# Keeps track on players scores
score_dict = {}

# Initialisation of the program
@client.event
# The program listens out for !flag or !flag-team to begin the game 
async def on_ready():
    await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name='!flag or !flag-team'))

# ---------------------------------------------------------------------------------------------------------------------------------------------#
# The !flag command
@client.command(name = 'flag')
async def flag(ctx):
    alive = True
    score = 0
    # Used to reduce the flag dictionary after each correctly guessed flag within an iteration of a game
    flag_dict_temp = flag_dict
    temp_storage_dict = {}
    # Identifies the discord server that the bot is present in 
    guild = ctx.message.guild

    # Defines the user specific channel name
    user_specific_channel = ctx.message.author.display_name.lower() + ctx.message.author.discriminator
    # Tests to see if the channel already exists
    channel_test = nextcord.utils.get(guild.channels, name=f'{user_specific_channel}')

    if channel_test is None:
        channel_name = ctx.author
        new_channel = await guild.create_text_channel(f'{channel_name}')
        print('This is our new channel name' , new_channel)
    else:
        new_channel = channel_test

    while alive == True:
       
        # Collecting a flag
        url, flag_name, flag_initial_url_input, flag_name_original = flag_output()
        if score == 0:
            await new_channel.send('Lets Play!!')

        # Sending the URL into the channel
        await new_channel.send(url)
        print(flag_name)
        # Waiting for the user's guess
        msg = await client.wait_for('message', check=lambda message: message.author == ctx.author and message.channel == new_channel)
        # Checking if the answer is correct
        check_list = input_checker(flag_name)
    # ---------------------------------------------------------------------------------------------------------------------------------------------#
        # Admin Checks
        # print(check_list)

    # ---------------------------------------------------------------------------------------------------------------------------------------------#
        # If the user guesses correctly...
        if msg.content in check_list:
            # Store the correct answer in the temporary dictionary
            temp_storage_dict[flag_initial_url_input] = flag_dict[flag_initial_url_input]
            # Delete the correct answer from the cloned dictionary
            del flag_dict_temp[flag_initial_url_input]
            # Send the "CORRECT" message to the user
            await new_channel.send('Correct!')
            # Increment the score by 1
            score += 1

    # ---------------------------------------------------------------------------------------------------------------------------------------------#
            # Admin Checks
            # print(len(flag_dict_temp.keys()))
            # print(temp_storage_dict)

    # ---------------------------------------------------------------------------------------------------------------------------------------------#
        # If the user guesses incorrectly...
        else:
            # Begin formatting the correct flag name to be used in a Wikipedia URL
            try:
                flag_name_for_url = flag_name_original.replace(' ','_')
            except:
                # If the flag has multiple correct solutions we only need one of them
                flag_name_for_url = flag_name_original[0].replace(' ','_')
            # Send the user the "INCORRECT" message along with their SCORE and a Wikipedia link to the origin of the flag
            await new_channel.send(f'Incorrect it was **{flag_name_original}**! \n**Final Score: {score}** \nFind out more about **{flag_name_original}** at: https://en.wikipedia.org/wiki/{flag_name_for_url} \n \n Type **!flag** or **!flag-team**')
            # Update the leaderboard with the user's score
            if msg.author.name in list(score_dict.keys()):
                if score_dict[msg.author.name] < score:
                    score_dict[msg.author.name] = score
                else:
                    pass
            else:
                score_dict[msg.author.name] = score
            
            alive = False

            # Reformat the flag dictionary by adding back all the corerct guesses
            flag_dict_temp.update(temp_storage_dict)

            # Send the user buttons to play again (yes / no)
            # Yes button
            playagain_button_yes = Button(label = 'Yes',style = ButtonStyle.green)
            async def button_interaction_yes(interaction):
                await interaction.response.send_message("** Let's go! **")
                await flag(ctx)
            # No Button
            playagain_button_no = Button(label = 'No',style = ButtonStyle.red)

            async def button_interaction_no(interaction):
                await interaction.response.send_message("** See you soon! **")

            playagain_button_yes.callback = button_interaction_yes
            playagain_button_no.callback = button_interaction_no

            myview = View(timeout=180)
            myview.add_item(playagain_button_yes)
            myview.add_item(playagain_button_no)

            # Sends the user the "PLAY AGAIN" message
            await new_channel.send('\n**Play again?**',view=myview)
# ---------------------------------------------------------------------------------------------------------------------------------------------#
# The !flag-team command
@client.command(name = 'flag-team')
async def team(ctx):
    alive = True
    score = 0
    # Used to reduce the flag dictionary after each correctly guessed flag within an iteration of a game
    flag_dict_temp = flag_dict
    temp_storage_dict = {}
    # Identifies the discord server that the bot is present in 
    guild = ctx.message.guild

    while alive == True:
       # Collecting a flag
        url, flag_name, flag_initial_url_input, flag_name_original = flag_output()
        # Sending the URL into the channel
        await ctx.send(url)
        print(flag_name)
        # Waiting for the user's guess
        msg = await client.wait_for('message', check=lambda message: message.author == ctx.author)
        # Checking if the answer is correct
        check_list = input_checker(flag_name)

    # ---------------------------------------------------------------------------------------------------------------------------------------------#
        # If the user guesses correctly...
        if msg.content in check_list:
            # Store the correct answer in the temporary dictionary
            temp_storage_dict[flag_initial_url_input] = flag_dict[flag_initial_url_input]
            # Delete the correct answer from the cloned dictionary
            del flag_dict_temp[flag_initial_url_input]
            # Send the "CORRECT" message to the user
            await ctx.send('Correct!')
            # Increment the score by 1
            score += 1

    # ---------------------------------------------------------------------------------------------------------------------------------------------#
        # If the user guesses incorrectly...
        else:
            # Begin formatting the correct flag name to be used in a Wikipedia URL
            try:
                flag_name_for_url = flag_name_original.replace(' ','_')
            except:
                # If the flag has multiple correct solutions we only need one of them
                flag_name_for_url = flag_name_original[0].replace(' ','_')
            # Send the user the "INCORRECT" message along with their SCORE and a Wikipedia link to the origin of the flag
            await ctx.send(f'Incorrect it was **{flag_name_original}**! \n**Final Score: {score}** \nFind out more about **{flag_name_original}** at: https://en.wikipedia.org/wiki/{flag_name_for_url} \n \n Type **!flag** or **!flag-team**')
            # Update the leaderboard with the team's score
            if 'team' in list(score_dict.keys()):
                if score_dict['team'] < score:
                    score_dict['team'] = score
                else:
                    pass
            else:
                score_dict['team'] = score
            
            alive = False
            # Reformat the flag dictionary by adding back all the corerct guesses
            flag_dict_temp.update(temp_storage_dict)
            
            # Send the user buttons to play again (yes / no)
            # Yes button
            playagain_button_yes = Button(label = 'Yes',style = ButtonStyle.green)
            async def button_interaction_yes(interaction):
                await interaction.response.send_message("** Let's go! **")
                await team(ctx)

            # No Button
            playagain_button_no = Button(label = 'No',style = ButtonStyle.red)

            async def button_interaction_no(interaction):
                await interaction.response.send_message("** See you soon! **")

            playagain_button_yes.callback = button_interaction_yes
            playagain_button_no.callback = button_interaction_no

            myview = View(timeout=180)
            myview.add_item(playagain_button_yes)
            myview.add_item(playagain_button_no)

            # Sends the team the "PLAY AGAIN" message
            await ctx.send('\n**Play again?**',view=myview)
# ---------------------------------------------------------------------------------------------------------------------------------------------#
# The !leaderboard function
@client.command(name = 'leaderboard')
async def leaderboard(ctx):
    # Collects all the scores in the leaderboard database amd rearranges them in descending order
    score_dict_order = {k: v for k, v in sorted(score_dict.items(), key=lambda item: item[1],reverse=True)}
    score_dict_key = list(score_dict_order.keys())
    score_dict_value = list(score_dict_order.values())
    mystring = ''
    # Sends the leaderboard to the specific discord channel
    for i in range(len(score_dict_key)):
        mystring += f'\n**{score_dict_key[i]}: {score_dict_value[i]}**' 
    await ctx.send('**Flag-Bot Leaderboard:**'+'\n---------------' + mystring)
    
# ---------------------------------------------------------------------------------------------------------------------------------------------#
# This runs the discord flag bot :)
client.run('MTAxNDQ3NzkxNjU4OTAwNjg3MA.GvA4iG.vmZVTj5HIAYhAKNn4CMpJDlbM8tf_uCRz6v_n0')
# ---------------------------------------------------------------------------------------------------------------------------------------------#

