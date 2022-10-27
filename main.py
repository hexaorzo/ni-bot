import os
import discord
import datetime
from discord.ext import commands
from discord_components import Button, Select, SelectOption, ComponentsBot, interaction
from discord_components.component import ButtonStyle
from deta import Deta

deta = Deta("d03885d1_ncJGXaE2wzDhh4gMvMP8osk9Hz8ofYyv")
async_db = deta.AsyncBase("onboarding")

#Bot prefix
bot = ComponentsBot('ni!', help_command=None)
embed_color = 0xfcd005


@bot.event
async def on_ready():
    print('Ready ✅')

#Ticket command
@bot.command()
@commands.has_permissions(administrator=True)
async def onboard(ctx):
    await ctx.message.delete()
    emoji = await ctx.guild.fetch_emoji(936698473267490816)
    #Embed title and description
    embed = discord.Embed(title ='Welcome to Neverinstall Discord server!', description ="**Press the button below** 👇 to gain access to the server" , color=embed_color) 

    await ctx.send(
        embed = embed,

        #Embed button
        components = [
            Button(
                custom_id = 'Onboard',
                label = "Let's go!",
                style = ButtonStyle.blue,
                emoji = emoji)
        ]
    )

@bot.event
async def on_button_click(interaction):

    #Select function
    if interaction.component.custom_id == "Onboard":
        user = interaction.user
        # Step 1
        await interaction.send(
            f'> **STEP 1/4** Would you like to get notified for announcements and community events? 📢',
            components = [[
                    Button(custom_id = 'yes_notif', label = "Ping me anytime", style = ButtonStyle.green, emoji = '🥳'),
                    Button(custom_id = 'no_notif', label = "No pings, thank you!", style = ButtonStyle.red, emoji = '🙂')
            ]])
    elif interaction.component.custom_id == 'yes_notif':
        user = interaction.user
        role = discord.utils.get(user.guild.roles, name="📢 Updates")
        await user.add_roles(role)

        # Step 2
        await interaction.edit_origin(
            f'> **STEP 2/4** What describes you the best? 👀',
        components = [
                Select(
                    max_values = 4,
                    placeholder = "Choose as many options you want",
                    options = [
                        SelectOption(label="Programmer", value="programmer", emoji='👨‍💻'),
                        SelectOption(label="Designer", value="designer", emoji='🎨'),
                        SelectOption(label="Student", value="student", emoji='👨‍🎓'),
                        SelectOption(label="Casual User", value="casual", emoji='😀')
                    ],
                    custom_id = "role_menu")])
      
    elif interaction.component.custom_id == 'no_notif':
        user = interaction.user
        role = discord.utils.get(user.guild.roles, name="📢 Updates")
        if role in interaction.user.roles:
            await user.remove_roles(role)
        # Step 2
        await interaction.edit_origin(
            f'> **STEP 2/4** What describes you the best? 👀',
        components = [
                Select(
                    max_values = 4,
                    placeholder = "Choose as many options you want",
                    options = [
                        SelectOption(label="Programmer", value="programmer", emoji='👨‍💻'),
                        SelectOption(label="Designer", value="designer", emoji='🎨'),
                        SelectOption(label="Student", value="student", emoji='👨‍🎓'),
                        SelectOption(label="Casual User", value="casual", emoji='😀')
                    ],
                    custom_id = "role_menu")])

   

@bot.event
async def on_select_option(interaction):
    # Step 2
    if interaction.component.custom_id == "role_menu":
        user = interaction.user
        role = user.guild.get_role(1020360163997270067)
        if "programmer" in interaction.values:
            await user.add_roles(role)
        elif role in interaction.user.roles:
            await user.remove_roles(role)

        role = user.guild.get_role(1020360346583703683)
        if "designer" in interaction.values:
            await user.add_roles(role)
        elif role in interaction.user.roles:
            await user.remove_roles(role)

        role = user.guild.get_role(1020360307744460801)
        if "student" in interaction.values:
            await user.add_roles(role)
        elif role in interaction.user.roles:
            await user.remove_roles(role)

        role = user.guild.get_role(1019855736370642965)
        if "casual" in interaction.values:
            await user.add_roles(role)
        elif role in interaction.user.roles:
            await user.remove_roles(role)

        # Step 3
        await interaction.edit_origin(
            f'> **STEP 3/4** How did you hear about Neverinstall? 👂',
        components = [
                Select(
                    placeholder = "Choose one of the options",
                    options = [
                        SelectOption(label="Social Media", value="social_media", emoji='📱'),
                        SelectOption(label="Friend/Colleague", value="colleague", emoji='🧑‍💼'),
                        SelectOption(label="Search Engine", value="search_engine", emoji='🔎')
                    ],
                    custom_id = "refer_menu")])

    # Step 3
    if interaction.component.custom_id == "refer_menu":
        user = interaction.user
        user_id = user.id
        userID = str(user_id)
        item = await async_db.get(userID)
        if "social_media" in interaction.values:
            if item is None:
                await async_db.put({"refer": "social_media", "key": userID})
            else:
                await async_db.update({"refer": "social_media"}, userID)
        elif "colleague" in interaction.values:
            if item is None:
                await async_db.put({"refer": "colleague", "key": userID})
            else:
                await async_db.update({"refer": "colleague"}, userID)
        elif "search_engine" in interaction.values:
            if item is None:
                await async_db.put({"refer": "search_engine", "key": userID})
            else:
                await async_db.update({"refer": "search_engine"}, userID)
        
        # Step 4
        await interaction.edit_origin(
            f'> **STEP 4/4** What\'s your preferred location? 🌍',
        components = [
                Select(
                    placeholder = "Choose one of the options",
                    options = [
                        SelectOption(label="India", description="Bangalore, Delhi, Mumbai, Pune", value="in", emoji='🇮🇳'),
                        SelectOption(label="Singapore", value="sg", emoji='🇸🇬'),
                        SelectOption(label="USA", description="California, Dallas, North Virginia", value="us", emoji='🇺🇸'),
                        SelectOption(label="UK", description="London", value="gb", emoji='🇬🇧'),
                        SelectOption(label="Canada", description="Montreal", value="ca", emoji='🇨🇦'),
                        SelectOption(label="Japan", description="Tokyo", value="jp", emoji='🇯🇵'),
                        SelectOption(label="Australia", description="Melbourne", value="au", emoji='🇦🇺'),
                        SelectOption(label="Indonesia", description="Jakarta", value="id", emoji='🇮🇩'),
                        SelectOption(label="Spain", description="Madrid", value="es", emoji='🇪🇸'),
                        SelectOption(label="Israel", description="Tel Aviv", value="is", emoji='🇮🇱'),
                        SelectOption(label="Brazil", value="br", emoji='🇧🇷'),
                        SelectOption(label="Finland", value="fl", emoji='🇫🇮'),
                        SelectOption(label="Netherlands", value="nl", emoji='🇳🇱')
                    ],
                    custom_id = "preferred_location_menu")])

    if interaction.component.custom_id == "preferred_location_menu":
        user = interaction.user
        user_id = user.id
        userID = str(user_id)
        item = await async_db.get(userID)
        if "in" in interaction.values:
            if item is None:
                await async_db.put({"location": "in", "key": userID})
            else:
                await async_db.update({"location": "in"}, userID)
        elif "sg" in interaction.values:
            if item is None:
                await async_db.put({"location": "sg", "key": userID})
            else:
                await async_db.update({"location": "sg"}, userID)
        elif "us" in interaction.values:
            if item is None:
                await async_db.put({"location": "us", "key": userID})
            else:
                await async_db.update({"location": "us"}, userID)
        elif "gb" in interaction.values:
            if item is None:
                await async_db.put({"location": "gb", "key": userID})
            else:
                await async_db.update({"location": "gb"}, userID)
        elif "ca" in interaction.values:
            if item is None:
                await async_db.put({"location": "ca", "key": userID})
            else:
                await async_db.update({"location": "ca"}, userID)
        elif "jp" in interaction.values:
            if item is None:
                await async_db.put({"location": "jp", "key": userID})
            else:
                await async_db.update({"location": "jp"}, userID)
        elif "au" in interaction.values:
            if item is None:
                await async_db.put({"location": "au", "key": userID})
            else:
                await async_db.update({"location": "au"}, userID)
        elif "id" in interaction.values:
            if item is None:
                await async_db.put({"location": "id", "key": userID})
            else:
                await async_db.update({"location": "id"}, userID)
        elif "es" in interaction.values:
            if item is None:
                await async_db.put({"location": "es", "key": userID})
            else:
                await async_db.update({"location": "es"}, userID)
        elif "is" in interaction.values:
            if item is None:
                await async_db.put({"location": "is", "key": userID})
            else:
                await async_db.update({"location": "is"}, userID)
        elif "br" in interaction.values:
            if item is None:
                await async_db.put({"location": "br", "key": userID})
            else:
                await async_db.update({"location": "br"}, userID)
        elif "fl" in interaction.values:
            if item is None:
                await async_db.put({"location": "fl", "key": userID})
            else:
                await async_db.update({"location": "fl"}, userID)
        elif "nl" in interaction.values:
            if item is None:
                await async_db.put({"location": "nl", "key": userID})
            else:
                await async_db.update({"location": "nl"}, userID)
        
        
        # Done
        role = discord.utils.get(user.guild.roles, name="🥳 Online")
        await user.add_roles(role)
        await interaction.edit_origin(
            f'Thank you {interaction.author.mention}! Welcome to Neverinstall and we\'re looking forward to take your computing to next level.\n\n**How to get started?**\n- Do read and follow the <#886878476190228490>\n- Check out our upcoming updates in <#1022176837251641454>\n- Feel free to have fun and discussions in our <#886864304903712800>\n- Please share your feedback in our <#886905658736267274>\n- Please report bugs and ask for help in <#886905619091697734>\n\nYour Neverinstall Team',
        components = [],
        delete_after = 20.0)
# 
token = os.getenv('BOT_TOKEN')
bot.run(token)
