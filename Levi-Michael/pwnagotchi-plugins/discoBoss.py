import discord, logging, subprocess
from os import remove
from pwnagotchi.utils import StatusFile
import pwnagotchi.ui.components as components
import pwnagotchi.ui.view as view
import pwnagotchi.ui.fonts as fonts
import pwnagotchi.plugins as plugins

class discoBoss(plugins.Plugin):
    __author__ = 'A1buS'
    __version__ = '1.0.0'
    __license__ = 'GPL3'
    __description__ = '''
    discoBoss Discord bot for pwnagotchi manage
    '''
    def __init__(self):
        self.ready = False
        self.TOKEN = '<TOKEN>'
        self.DEFAULT_MESSAGES_LIMIT = 100

        self.discoBoss_channel = dict({
                                'name': 'discoboss',
                                'channel_id': '<CHANNEL_ID>',
                                'webhook_name':'discoBoss_WH'
                                })

        self.discoHash_channel = dict({
                                'name': 'disco-hashes',
                                'channel_id': '<CHANNEL_ID>',
                                'webhook_name':'discohash_WH'
                                })
        logging.info("[discoBoss]: discoBoss plugin initialize")

    def handle_response(self,message)->str:
        p_message = message.lower()
        if p_message == '!dumphelp' or p_message == '!dumphash':
            return f"`Hi Im your HASH DUMPER Bot for using me please go to {self.discoBoss_channel['name']} channel and write !dumphash also you can choose how many hashes with !dumphash 5 for example`"

    async def send_message(self, message, user_message, is_private):
        try:
            response = self.handle_response(user_message)
            await message.author.send(response) if is_private else await message.channel.send(response)
        except Exception:
            pass

    def run_discord_bot(self):
        intents = discord.Intents.default()
        intents.messages = True
        try:
            intents.message_content = True
        except:
            pass
        client = discord.Client(intents=intents)
        @client.event
        async def on_ready():
            logging.info(f"[discoBoss]: {client.user} is now ready!.")
            print(f'{client.user} is now ready!')
        
        async def on_unload():
            logging.info('[discoBoss]: successfully Unloaded.')
            exit()

        @client.event
        async def on_message(message):
            if message.author == client.user:
                return
            username = str(message.author)
            user_message = str(message.content)
            channel = str(message.channel)
            
            logging.info(f"[discoBoss]: {username} Said: '{user_message}' on channel:'{channel}'.")
            print(f"{username} Said: '{user_message}' on channel:'{channel}'.")

            if '!exit' in user_message and channel == self.discoBoss_channel['name']:
                    logging.info('[discoBoss]: successfully Unloaded.')
                    exit()

            elif '!dumphash' in user_message and channel == self.discoBoss_channel['name']:
                logging.info("[discoBoss]: !dumphash - kickin")
                try:
                    limit_messages = int(user_message.split(' ')[1])
                except:
                    limit_messages = self.DEFAULT_MESSAGES_LIMIT
                with open('hashes.22000', 'w') as f:
                    o_cahnnel = client.get_channel(int(self.discoHash_channel['channel_id']))
                    if limit_messages > self.DEFAULT_MESSAGES_LIMIT:
                        limit = limit_messages*2
                    else:
                        limit = self.DEFAULT_MESSAGES_LIMIT
                    messages = o_cahnnel.history(limit=limit)
                    count = 0
                    async for i in messages:
                        if self.discoHash_channel['webhook_name'] in str(i):
                            count +=1
                            try:
                                hash_dict = i.embeds[0].to_dict() 
                                hash = hash_dict['fields'][0]['value']
                                f.write(hash[1:-1])
                                if count == limit_messages:
                                    break
                            except:
                                pass
                with open('hashes.22000', 'r') as f:
                    await message.channel.send(f'''Gathering up to last {limit_messages} hashes.\n\nWPA\WPA2 is minimum 8 chars. \nFor BruteForce from 8 to 11 digits use this: \n  hashcat -m 22000 -a 3 hashcat.22000.txt ?d?d?d?d?d?d?d?d?d?d?d -i --increment-min=8 \n\nFor BruteForce from 8 to 11 chars use this: \n  hashcat -m 22000 -a 3 hashcat.22000.txt ?a?a?a?a?a?a?a?a?a?a?a -i --increment-min=8 \n\n'''
                                            ,file=discord.File(f, 'hashcat.22000.txt'))
                    print('send file!')
                remove("hashes.22000")

            elif '!status' in user_message and channel == self.discoBoss_channel['name']:
              logging.info("[discoBoss]: !status - kickin")

            elif '!reboot' in user_message and channel == self.discoBoss_channel['name']:
                logging.info("[discoBoss]: !reboot - kickin")
                subprocess.call(["shutdown", "-r", "-t", "0"])  # Reboot the the pi

            elif '!poweroff' in user_message and channel == self.discoBoss_channel['name']:
                logging.info("[discoBoss]: !poweroff - kickin")
                subprocess.call(["shutdown", "-h", "now"])  # Poweroff the the pi

            elif '!hc' in user_message and channel == self.discoBoss_channel['name']:
                logging.info("[discoBoss]: !hc - healthcheck kickin")
                print("[discoBoss]: !hc - healthcheck")

            elif user_message[0] == '?':
                user_message = user_message[1:]
                await self.send_message(message=message,user_message=user_message, is_private=True)
            else:
                await self.send_message(message=message,user_message=user_message, is_private=False)
        client.run(self.TOKEN)

    def on_loaded(self):
        self.run_discord_bot()
        logging.info("[discoBoss]: plugin loaded.")
