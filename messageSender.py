#HELLO FRIENDS
#That a simple script for sending messages to telegram
#how to use:
#1. install telethon - pip install telethon
#2. get your api_id and api_hash from https://my.telegram.org/auth
#3. run the script
#4. enter the recipient username
#5. press enter to start
#input number like this: +380123456789
#you have conect yout client to telegram
import asyncio
import sys
import random
import traceback
from telethon import TelegramClient
import time

# Configuration
api_hash = 'ae72eecbcf1a6f7a35fd1d4ac1dfda70'  # Your API hash
api_id = 26044482  # API id
phone = '+380 96 935 16 44'  # Your phone number
defaultRecipient = 'default recipient'

mesaga = 'Hello world!'
interval = 1  # Interval in seconds

async def message(client, recipient):
    while True:
        try:
            message = mesaga
            print('Sending message:', message)
            await client.send_message(recipient, message)
            await asyncio.sleep(interval)
        except Exception as e:
            print(f"Error sending message: {e}")
            await asyncio.sleep(5)

async def main():
    async with TelegramClient('session_name', api_id, api_hash) as client:
        print("Connecting to Telegram...")
        await client.connect()
        
        if not await client.is_user_authorized():
            print('User not authorized. Please sign in.')
            await client.send_code_request(phone)
            await client.sign_in(phone, input('Enter the code you received: '))
        
        print("Client connected.")
        
        # Ask user for recipient type
        recipient_type = input('Send to user or group? (u/g): ').lower()
        
        if recipient_type == 'g':
            # Get list of available groups
            print("Fetching your groups...")
            dialogs = await client.get_dialogs()
            groups = []
            
            print("\nAvailable groups:")
            for i, dialog in enumerate(dialogs):
                if dialog.is_group:
                    groups.append(dialog)
                    print(f"{i}. {dialog.name}")
            
            if not groups:
                print("No groups found. Will use default or user recipient.")
                recipient_type = 'u'
            else:
                choice = input('\nEnter group number or press enter for manual input: ')
                if choice and choice.isdigit() and int(choice) < len(groups):
                    recipient = groups[int(choice)]
                    print(f'Selected group: {recipient.name}')
                else:
                    group_input = input('Enter group username or ID: ')
                    if group_input:
                        recipient = group_input
                    else:
                        print("No group specified. Using default recipient.")
                        recipient = defaultRecipient
        
        if recipient_type != 'g':
            recipient = input('Enter recipient username: ')
            if not recipient:
                recipient = defaultRecipient
        
        print('Sending messages to:', getattr(recipient, 'name', recipient))
        
        # Customize message
        custom_message = input('Enter custom message (press enter to use default): ')
        if custom_message:
            global mesaga
            mesaga = custom_message
        
        # Set custom interval
        try:
            custom_interval = input('Enter message interval in seconds (press enter to use default): ')
            if custom_interval:
                global interval
                interval = float(custom_interval)
        except ValueError:
            print("Invalid interval. Using default interval.")
        
        print('Press enter to start')
        input()
        
        print('Starting... (Press Ctrl+C to stop)')
        await message(client, recipient)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Stopped by user')
    except Exception as e:
        print('Error:', e)
        traceback.print_exc()
    sys.exit(0)