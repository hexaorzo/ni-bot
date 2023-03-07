import os
import discord
import datetime
from discord.ext import commands

embed_color = 0xfcd005
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='ni!', intents=intents)

@bot.event
async def on_ready():
    print("Bot is ready!")

#Ticket command
@bot.command()
@commands.has_permissions(administrator=True)
async def ticket(ctx):
    await ctx.message.delete()

    embed = discord.Embed(title='Neverinstall Support!',
                            description="**Press the button below** 👇 to create a ticket", color=embed_color)

    await ctx.send(
        embed=embed,
        view=discord.ui.View().add_item(discord.ui.Button(custom_id='ticket_button', label="Create a Ticket", style=discord.ButtonStyle.green, emoji='🎫'))
    )

# Onboard command
@bot.command()
@commands.has_permissions(administrator=True)
async def onboard(ctx):
    await ctx.message.delete()
    # emoji = await ctx.guild.fetch_emoji(936698473267490816)
    embed = discord.Embed(title='Welcome to Neverinstall Discord server!',
                          description="**Press the button below** 👇 to gain access to the server", color=embed_color)
    emoji = await ctx.guild.fetch_emoji(936698473267490816)

    await ctx.send(
        embed=embed,
        view=discord.ui.View().add_item(discord.ui.Button(custom_id='Onboard', label="Let's Go!", style=discord.ButtonStyle.blurple, emoji=emoji)))

@bot.event
async def on_interaction(interaction):
    global ticket_type
    logs = interaction.guild.get_channel(1082275606835761213)

    if interaction.data['custom_id'] == 'ticket_button':
        await interaction.response.send_message(
            delete_after=120.0,
            content=f'> **What type of ticket would you like to create? 📢**',
            ephemeral=True,
            view=discord.ui.View().add_item(discord.ui.Select(custom_id='ticket_menu', options=[
                discord.SelectOption(label="Spaces issues", description="Build time, app installation, collaboration, OS", value="spaces_issues", emoji='🚀'),
                discord.SelectOption(label="Authentication issues", description="Not able to login/signup", value="auth_issues", emoji='🔑'),
                discord.SelectOption(label="Billing issues", description="Auto renewal, one time subscriptions,payment, invoices", value="billing_issues", emoji='💳'),
                discord.SelectOption(label="Account security & privacy ", description="Account deletion, notifications", value="privacy_issues", emoji='🔒'),
                discord.SelectOption(label="Upcoming features", value="upcoming", emoji='🔮'),
                discord.SelectOption(label="Other issues", description="Something else", value="other_issues", emoji='❓')
                ])))


    if interaction.data['custom_id'] == 'ticket_menu':
        ticket_type = interaction.data['values'][0]
        # create a Modal 
        view = discord.ui.Modal(title="Create a Ticket", custom_id="ticket_modal")
        view.add_item(discord.ui.TextInput(label="Email Address", placeholder="Email address linked with Neverinstall account", custom_id="email"))
        view.add_item(discord.ui.TextInput(label="Subject", placeholder="Subject of your ticket", custom_id="subject"))
        view.add_item(discord.ui.TextInput(label="Description", placeholder="Describe your issue in detail", custom_id="description", style=discord.TextStyle.paragraph))
        await interaction.response.send_modal(view)


    if interaction.data['custom_id'] == 'ticket_modal':
        user = interaction.user
        user_id = user.id
        userID = str(user_id)

        # get email
        for component in interaction.data['components']:
            if component['components'][0]['custom_id'] == 'email':
                email = component['components'][0]['value']
            elif component['components'][0]['custom_id'] == 'subject':
                subject = component['components'][0]['value']
            elif component['components'][0]['custom_id'] == 'description':
                description = component['components'][0]['value']

        # create a ticket channel
        guild = interaction.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            user: discord.PermissionOverwrite(read_messages=True),
        }
        ticket_types = ['spaces_issues', 'auth_issues', 'billing_issues', 'privacy_issues', 'upcoming', 'other_issues']
        ticket_types_name = ['Spaces issues', 'Authentication issues', 'Billing issues', 'Account security & privacy', 'Upcoming features', 'Other issues']
        ticket_types_emoji = ['🚀', '🔑', '💳', '🔒', '🔮', '❓']
        ticket_emoji = ticket_types_emoji[ticket_types.index(ticket_type)]
        ticket_type_name = ticket_types_name[ticket_types.index(ticket_type)]

        category = discord.utils.get(guild.categories, id=1082247198059802644)
        channel = await guild.create_text_channel(f'{ticket_emoji} t-{user.name}', category=category, overwrites=overwrites)
        await channel.set_permissions(user, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
        await channel.set_permissions(discord.utils.get(interaction.guild.roles, id = 906249753598255176), send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
        
        await channel.send(embed=discord.Embed(title=f'**Ticket information**', description=f'**Created by:** {user.mention}\n**Type:** {ticket_type_name}\n**Email:** {email}\n**Subject:** {subject}\n**Description:** {description}', color=embed_color), view=discord.ui.View().add_item(discord.ui.Button(custom_id='close_ticket', label="Close Ticket", style=discord.ButtonStyle.red, emoji='🔒')))
        await channel.send(f'<@&906249753598255176>')
    
        await interaction.response.edit_message(
            content=f'> {channel.mention} has been created for you! 🎉',
            view=discord.ui.View().clear_items(),
            delete_after=20.0)

        # send a message to logs channel
        await logs.send(embed=discord.Embed(title=f'**Ticket created**', description=f'',timestamp = datetime.datetime.utcnow(), color=embed_color).add_field(name=f'**Ticket information**', value=f'**Created by:** {interaction.user.mention}\n**Type:** {ticket_type_name}\n**Email:** {email}\n**Subject:** {subject}\n**Description:** {description}').add_field(name=f'**Ticket channel**', value=f'{channel.name}').set_footer(text=f'User ID: {interaction.user.id}').set_thumbnail(url=interaction.user.display_avatar.url))
        

    if interaction.data['custom_id'] == 'close_ticket':
        channel = interaction.channel
        await channel.send(embed=discord.Embed(description=f'⚠️ Are you sure you want to close the ticket?', color=embed_color), view=discord.ui.View().add_item(discord.ui.Button(custom_id='confirm_close', label="Yes, close it!", style=discord.ButtonStyle.red, emoji='🔒')).add_item(discord.ui.Button(custom_id='cancel_close', label="No, keep it open!", style=discord.ButtonStyle.green, emoji='🔓')))
        await interaction.response.defer()

    if interaction.data['custom_id'] == 'confirm_close':
        channel = interaction.channel
        await logs.send(embed=discord.Embed(title=f'**Ticket closed**', description=f'',timestamp = datetime.datetime.utcnow(), color=embed_color).add_field(name=f'**Ticket channel**', value=f'{channel.name}').add_field(name=f'**Closed by:**', value=f'{interaction.user.mention}').set_footer(text=f'User ID: {interaction.user.id}').set_thumbnail(url=interaction.user.display_avatar.url))
        await channel.delete()
        
    elif interaction.data['custom_id'] == 'cancel_close':
        await interaction.message.delete()
    
    if interaction.data['custom_id'] == 'Onboard':   
        # Step 1  
        await interaction.response.send_message(
            content=f'> **STEP 1/4** Would you like to get notified for announcements and community events? 📢',
            ephemeral=True,
            view=discord.ui.View().add_item(discord.ui.Button(custom_id='yes_notif', label="Ping me anytime", style=discord.ButtonStyle.green, emoji='🥳')).add_item(discord.ui.Button(custom_id='no_notif', label="No pings, thank you!", style=discord.ButtonStyle.red, emoji='🙂'))
        )
    elif interaction.data['custom_id'] == 'yes_notif':
        user = interaction.user
        role = discord.utils.get(user.guild.roles, name="📢 Updates")
        await user.add_roles(role)

        # Step 2
        await interaction.response.edit_message(
            content=f'> **STEP 2/4** What describes you the best? 👀',
            view=discord.ui.View().add_item(discord.ui.Select(custom_id='role_menu', max_values=4, options=[
                discord.SelectOption(label="Developer", value=1020360163997270067, emoji='👨‍💻'),
                discord.SelectOption(label="Designer", value=1020360346583703683, emoji='👨‍🎨'),
                discord.SelectOption(label="Student", value=1020360307744460801, emoji='👨‍🎓'),
                discord.SelectOption(label="Casual User", value=1019855736370642965, emoji='😀')]
            ))
        )
    
    elif interaction.data['custom_id'] == 'no_notif':
        user = interaction.user
        role = discord.utils.get(user.guild.roles, name="📢 Updates")
        if role in interaction.user.roles:
            await user.remove_roles(role)

        # Step 2
        await interaction.response.edit_message(
            content=f'> **STEP 2/4** What describes you the best? 👀',
            view=discord.ui.View().add_item(discord.ui.Select(custom_id='role_menu', max_values=4, options=[
                discord.SelectOption(label="Developer", value=1020360163997270067, emoji='👨‍💻'),
                discord.SelectOption(label="Designer", value=1020360346583703683, emoji='👨‍🎨'),
                discord.SelectOption(label="Student", value=1020360307744460801, emoji='👨‍🎓'),
                discord.SelectOption(label="Casual User", value=1019855736370642965, emoji='😀')]
            ))
        )

    elif interaction.data['custom_id'] == 'role_menu':
        user = interaction.user

        for option in interaction.data['values']:
            role = discord.utils.get(user.guild.roles, id=int(option))
            if role not in user.roles:
                await user.add_roles(role)
                

        for role in user.roles:
            if role.id in [1020360163997270067, 1020360346583703683, 1020360307744460801, 1019855736370642965]:
                if role.id not in interaction.data['values']:
                    await user.remove_roles(role)

        # Step 3
        await interaction.response.edit_message(
            content=f'> **STEP 3/4** How did you hear about Neverinstall? 👂',
            view=discord.ui.View().add_item(discord.ui.Select(custom_id='refer_menu', options=[
                discord.SelectOption(label="Social Media", value="social_media", emoji='📱'),
                discord.SelectOption(label="Friend/Colleague", value="colleague", emoji='🧑‍💼'),
                discord.SelectOption(label="Search Engine", value="search_engine", emoji='🔎')]
            ))
        )

    if interaction.data['custom_id'] == 'refer_menu':
        user = interaction.user
        user_id = user.id
        userID = str(user_id)

        #Done
        role = discord.utils.get(user.guild.roles, name="🥳 Online")
        await user.add_roles(role)
        await interaction.response.edit_message(
            content= f'Thank you {user.mention}! Welcome to Neverinstall and we\'re looking forward to take your computing to next level.\n\n**How to get started?**\n- Do read and follow the <#886878476190228490>\n- Check out our upcoming updates in <#1022176837251641454>\n- Feel free to have fun and discussions in our <#886864304903712800>\n- Please share your feedback in our <#886905658736267274>\n- Please report bugs and ask for help in <#886905619091697734>\n\nYour Neverinstall Team',
            view=discord.ui.View().clear_items(),
            delete_after=20.0
            )

token = os.environ.get("BOT_TOKEN")
bot.run(token)
