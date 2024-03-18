import logging
import re
import os
from datetime import datetime
import subprocess
import telegram
import telegram.ext as tg
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import MessageHandler, Filters, CallbackQueryHandler, Updater, CommandHandler, ConversationHandler, \
    CallbackContext
import pwnagotchi.plugins as plugins
from pwnagotchi.voice import Voice
import pwnagotchi
from pathlib import Path
from time import ctime
try:
    from PIL import ImageGrab
except ImportError:
    import pyscreenshot as ImageGrab

MAIN_SCREEN, MANAGE_DEVICE, TOOLBOX, HANDSHAKES_MENU, POWER_MENU = range(5)
HANDSHAKES_FOLDER = '/root/handshakes/'
BACKUP_FILE_PATH = '/root/pwnagotchi-backup.tar.gz'


class Telegram(plugins.Plugin):
    __author__ = 'BlueM3th'
    __version__ = '1.0'
    __license__ = 'GPL3'
    __description__ = 'Pwnagotchi Telegram bot manager'
    __dependencies__ = 'python-telegram-bot==13.15'

    def __init__(self):
        self.updater = None
        self.dispatcher = None
        self.agent = None
        self.handshakes_list = {}

    def on_loaded(self):
        logging.info("[TelegramBot] Plugin loaded.")
        self.logger = logging.getLogger("TelegramBotPlugin")
        self.options['auto_start'] = True
        self.completed_tasks = 0
        self.num_tasks = 8  # Increased for the new pwnkill task
        self.telegram_connected = False

    ############# MAIN SETUP ###############

    def on_agent(self, agent):
        logging.info("[TelegramBot] Starting agent...")
        if 'auto_start' in self.options and self.options['auto_start']:
            self.on_internet_available(agent)

    def init_bot(self):
        self.updater = Updater(token=self.options['bot_token'])
        self.dispatcher = self.updater.dispatcher
        self.dispatcher.add_handler(CallbackQueryHandler(self.button_click))

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.main_scren_menu)],
            states={
                MAIN_SCREEN: [
                    MessageHandler(Filters.regex('^⚙️ Manage device$'), self.manage_device_menu),
                    MessageHandler(Filters.regex('^🧰 Toolbox$'), self.toolbox_menu)
                ],
                MANAGE_DEVICE: [
                    MessageHandler(Filters.regex('^.*?Power$'), self.power_menu),
                    MessageHandler(Filters.regex('^.*?Screenshot$'), self.take_screenshot),
                    MessageHandler(Filters.regex('^.*?Stats$'), self.handle_memtemp),
                    MessageHandler(Filters.regex('^.*?Uptime$'), self.uptime),
                    MessageHandler(Filters.regex('^.*?Backup$'), self.create_backup)
                ],
                TOOLBOX: [
                    MessageHandler(Filters.regex('^.*?Handshakes downloader$'), self.handshakes_menu),
                    MessageHandler(Filters.regex('^.*?Handshakes count$'), self.handshake_count),
                    MessageHandler(Filters.regex('^.*?Pwngrid inbox$'), self.get_pwngrid_inbox),
                    MessageHandler(Filters.regex('^.*?Read WpaSec results (plugin)$'), self.get_pwngrid_inbox)
                ],
                HANDSHAKES_MENU: [
                    MessageHandler(Filters.regex('.*?Back$'), self.toolbox_menu),
                    MessageHandler(Filters.all, self.handshake_list)
                ],
                POWER_MENU: [
                    MessageHandler(Filters.regex('^.*?Shutdown$'), self.shutdown),
                    MessageHandler(Filters.regex('^.*?Reboot$'), self.reboot),
                    MessageHandler(Filters.regex('^.*?Restart (pwnkill)$'), self.pwnkill),
                    MessageHandler(Filters.regex('^.*?Restart (systemctl)$'), self.restart_process),
                    MessageHandler(Filters.regex('.*?Back$'), self.manage_device_menu)
                ],
            },
            fallbacks=[MessageHandler(Filters.regex('.*?Back$'), self.main_scren_menu)]
        )

        # Get the dispatcher to register handlers
        self.dispatcher.add_handler(conv_handler)

        # Start the Bot
        self.updater.start_polling()

    def on_internet_available(self, agent):
        if self.telegram_connected:
            return

        if not self.agent:
            self.agent = agent

        display = agent.view()
        last_session = agent.last_session
        logging.info("[TelegramBot] Internet available, connecting ...")

        try:
            if not self.updater:
                self.init_bot()
            self.telegram_connected = True

        except Exception as e:
            self.logger.error("Error while connecting with Telegram")
            self.logger.error(str(e))

        if last_session.is_new() and last_session.handshakes > 0:
            msg = f"Session started at {last_session.started_at()} and captured {last_session.handshakes} new handshakes"
            self.send_notification(msg)

            last_session.save_session_id()
            display.set('status', 'Telegram notification sent!')
            display.update(force=True)

    ############# MENU NAVIGATION ###############
    def main_scren_menu(self, update: Update, context: CallbackContext) -> int:
        """Start the conversation and ask user for input."""
        keyboard = [
            [KeyboardButton('⚙️ Manage device')],
            [KeyboardButton('🧰 Toolbox')]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

        update.message.reply_text(
            "Welcome to your Pwnagotchi Bot! 👾 \n"
            "Please select an option:",
            reply_markup=reply_markup
        )
        return MAIN_SCREEN

    def toolbox_menu(self, update: Update, context: CallbackContext) -> int:
        keyboard = [
            [KeyboardButton('💾️ Handshakes downloader')],
            [KeyboardButton('📬 Pwngrid inbox')],
            [KeyboardButton('🧩 Read WpaSec results (plugin)')],
            [KeyboardButton('◀️ Back')]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

        update.message.reply_text(
            "🧰 Toolbox ",
            reply_markup=reply_markup
        )
        return TOOLBOX

    def handshakes_menu(self, update: Update, context: CallbackContext) -> int:
        keyboard = [[KeyboardButton('◀️ Back')]]
        reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

        handshake_dir = Path(HANDSHAKES_FOLDER)
        handshakes = [file for file in handshake_dir.iterdir() if (file.is_file() and file.suffix == '.pcap')]

        if len(handshakes) < 1:
            update.effective_message.reply_text(
                '🤝🏻 No handshakes available! 😔',
                reply_markup=reply_markup)
            return TOOLBOX

        response = f'🤝🏻 {len(handshakes)} handshakes available, please type the index of the one you need:\n'
        for index, handshake in enumerate(handshakes):
            response += f'\n{index + 1}\. `{handshake.stem}`'
            self.handshakes_list[index + 1] = os.path.join(handshake_dir, handshake)

        update.message.reply_text(response, reply_markup=reply_markup, parse_mode='MarkdownV2')
        return HANDSHAKES_MENU

    def manage_device_menu(self, update: Update, context: CallbackContext) -> int:
        keyboard = [
            [KeyboardButton('🔌 Power')],
            [KeyboardButton('📸 Screenshot'), KeyboardButton('🖥️ Stats')],
            [KeyboardButton('🕖 Uptime'), KeyboardButton('💾 Backup')],
            [KeyboardButton('◀️ Back')]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

        update.message.reply_text(
            "⚙️ Manage device ",
            reply_markup=reply_markup
        )
        return MANAGE_DEVICE

    def power_menu(self, update: Update, context: CallbackContext) -> int:
        keyboard = [
            [KeyboardButton('☠️ Shutdown')],
            [KeyboardButton('🔄 Reboot')],
            [KeyboardButton('♻️ Restart (pwnkill)'), KeyboardButton('♻️ Restart (systemctl)')],
            [KeyboardButton('◀️ Back')]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

        update.message.reply_text(
            "🔌 Power management",
            reply_markup=reply_markup
        )
        return POWER_MENU

    ############# FUNCTIONS IMPLEMENTATIONS ###############
    ############# MANAGE DEVICE SECTION ###############

    def take_screenshot(self, update: Update, context: CallbackContext) -> int:
        try:
            display = self.agent.view()
            picture_path = '/tmp/display_screenshot.png'

            # Capture screenshot
            screenshot = display.image()
            if self.options['rotate_image']:
                screenshot = screenshot.rotate(180)
            screenshot.save(picture_path, 'png')

            with open(picture_path, 'rb') as photo:
                context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)

            response = "Hello there! 👾"
        except Exception as e:
            response = f"Error taking screenshot: {e}"

        update.effective_message.reply_text(response)
        return MANAGE_DEVICE

    def handle_memtemp(self, update: Update, context: CallbackContext) -> int:
        reply = f"💾 Memory Usage: {int(pwnagotchi.mem_usage() * 100)}%\n\n💿 CPU Load: {int(pwnagotchi.cpu_load() * 100)}%\n\n🌡 CPU Temp: {pwnagotchi.temperature()}°C"
        context.bot.send_message(chat_id=update.effective_chat.id, text=reply)
        return MANAGE_DEVICE

    def uptime(self, update: Update, context: CallbackContext) -> int:
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])

        uptime_minutes = uptime_seconds / 60
        uptime_hours = int(uptime_minutes // 60)
        uptime_remaining_minutes = int(uptime_minutes % 60)

        response = f"🕖 Uptime: {uptime_hours} hours and {uptime_remaining_minutes} minutes"
        update.effective_message.reply_text(response)

        self.completed_tasks += 1
        if self.completed_tasks == self.num_tasks:
            self.terminate_program()
        return MANAGE_DEVICE

    def create_backup(self, update: Update, context: CallbackContext) -> int:
        backup_files = [
            HANDSHAKES_FOLDER,
            '/root/brain.json',
            '/root/.ssh/authorized_keys',
            '/root/peers/',
            '/etc/pwnagotchi/',
            '/usr/local/share/pwnagotchi/'
        ]

        try:
            # Only backup existing files to prevent errors
            existing_files = list(filter(lambda f: os.path.exists(f), backup_files))
            update.effective_message.reply_text('🗄️ Backup in progress...')
            # Create a tarball
            subprocess.run(['sudo', 'tar', 'czf', BACKUP_FILE_PATH] + existing_files)

            logging.info("Backup created successfully. Sending...")
            update.effective_message.reply_text('🗄️ Backup created successfully. \n      Sending...')

            document = open(BACKUP_FILE_PATH, 'rb')
            update.effective_message.reply_document(document, f'Backup_{datetime.today().strftime("%d-%m-%Y")}.tar.gz', timeout=500)

        except Exception as e:
            logging.error(f"Error creating backup: {e}")
            update.effective_message.reply_text(f'🗄️ Error during backup:\n{e}')

        self.completed_tasks += 1
        if self.completed_tasks == self.num_tasks:
            self.terminate_program()
        return MANAGE_DEVICE

    ############# POWER SECTION ###############
    def reboot(self, update: Update, context: CallbackContext) -> int:
        response = "Rebooting now..."
        update.effective_message.reply_text(response)
        subprocess.run(['sudo', 'reboot'])
        return POWER_MENU

    def shutdown(self, update: Update, context: CallbackContext) -> int:
        response = "Shutting down now..."
        update.effective_message.reply_text(response)
        subprocess.run(['sudo', 'shutdown', '-h', 'now'])
        return POWER_MENU

    def restart_process(self, update: Update, context: CallbackContext) -> int:
        response = "Restarting process now..."
        update.effective_message.reply_text(response)
        subprocess.run(['sudo', 'systemctl', 'restart', 'pwnagotchi'])
        return POWER_MENU

    def pwnkill(self, update: Update, context: CallbackContext) -> int:
        try:
            response = "Sending pwnkill to pwnagotchi..."
            update.effective_message.reply_text(response)
            subprocess.run(['sudo', 'killall', '-USR1', 'pwnagotchi'])
        except subprocess.CalledProcessError as e:
            response = f"Error executing pwnkill command: {e}"
            update.effective_message.reply_text(response)
        return POWER_MENU

    ############# TOOLBOX SECTION ###############

    def handshake_count(self, update: Update, context: CallbackContext) -> int:
        count = len(
            [name for name in os.listdir(HANDSHAKES_FOLDER) if os.path.isfile(os.path.join(HANDSHAKES_FOLDER, name))])

        response = f"🤝 Total handshakes captured: {count}"
        update.effective_message.reply_text(response)

        self.completed_tasks += 1
        if self.completed_tasks == self.num_tasks:
            self.terminate_program()
        return TOOLBOX

    def read_handshake_pot_files(self, file_path):
        try:
            content = subprocess.check_output(['sudo', 'cat', file_path])
            content = content.decode('utf-8')
            matches = re.findall(r'\w+:\w+:(?P<essid>[\w\s-]+):(?P<password>.+)', content)
            formatted_output = [f"{match[0]}:{match[1]}" for match in matches]
            chunk_size = 5
            chunks = [formatted_output[i:i + chunk_size] for i in range(0, len(formatted_output), chunk_size)]
            chunk_strings = ['\n'.join(chunk) for chunk in chunks]
            return chunk_strings

        except subprocess.CalledProcessError as e:
            return None

    def read_wpa_sec_cracked(self, update: Update, context: CallbackContext) -> int:
        file_path = HANDSHAKES_FOLDER + "wpa-sec.cracked.potfile"

        chunks = self.read_handshake_pot_files(file_path)
        if not chunks or not any(chunk.strip() for chunk in chunks):
            update.effective_message.reply_text("Cannot read \"wpa-sec.cracked.potfile\" file.")
        else:
            for chunk in chunks:
                update.effective_message.reply_text(chunk)

        self.completed_tasks += 1
        if self.completed_tasks == self.num_tasks:
            self.terminate_program()

    def get_pwngrid_inbox(self, update: Update, context: CallbackContext) -> int:
        command = "sudo pwngrid -inbox"
        output = subprocess.check_output(command, shell=True).decode("utf-8")
        lines = output.split("\n")
        formatted_output = []
        for line in lines:
            if "│" in line:
                message = line.split("│")[1:4]
                formatted_message = "ID: " + message[0].strip().replace('\x1b[2m', '').replace('\x1b[0m', '') + "\n" + \
                                    "Date: " + message[1].strip().replace('\x1b[2m', '').replace('\x1b[0m', '') + "\n" + \
                                    "Sender: " + message[2].strip().replace('\x1b[2m', '').replace('\x1b[0m', '')
                formatted_output.append(formatted_message)

        if len(formatted_output) > 0:
            formatted_output.pop(0)

        reply = "\n".join(formatted_output)

        if reply:
            context.bot.send_message(chat_id=update.effective_chat.id, text=reply)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="No messages found in Pwngrid inbox.")
        return TOOLBOX

    def handshake_list(self, update: Update, context: CallbackContext) -> int:

        message = update.effective_message.text
        if not message.isdecimal() and int(message) < 0 or int(message) > len(self.handshakes_list):
            update.effective_message.reply_text('Invalid index number!')
            return HANDSHAKES_MENU

        try:
            filepath = self.handshakes_list[int(message)]

            modify_date = ctime(os.path.getmtime(filepath))
            filepath = filepath.replace(HANDSHAKES_FOLDER, '')
            # Prevent Button_data_invalid error form telegram, occurring with callback_data length > 64 bytes
            ap = filepath.split('_')[0]

            message = (f"Here you go! :\n\n"
                       f"  📶  {ap} \n"
                       f"  🕜  {modify_date}")
            length = len(f'download_pcap:{filepath}'.encode('utf-8'))
            self.logger.info(f"[TelegramBot] Sending handshake {filepath}. Size: {length}")
            keyboard = [[InlineKeyboardButton("pcap", callback_data=f"pcap:{filepath}"),
                         InlineKeyboardButton("hashcat", callback_data=f"hash:{filepath}"),
                         InlineKeyboardButton("wordlist", callback_data=f"wlst:{filepath}")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            self.updater.bot.sendMessage(chat_id=update.effective_message.chat_id,
                                         text=message,
                                         disable_web_page_preview=True,
                                         reply_markup=reply_markup)
            self.logger.info(f"[TelegramBot] Update sent as reply to chatid {update.effective_message.chat_id}.")
        except :
            self.updater.bot.sendMessage(chat_id=update.effective_message.chat_id,
                                         text='Cannot get the required file, please check logs... 😔')

        self.completed_tasks += 1
        if self.completed_tasks == self.num_tasks:
            self.terminate_program()
        return HANDSHAKES_MENU

    ################## HANDSHAKES ######################

    def button_click(self, update, context):
        query = update.callback_query
        query.answer()
        action, filepath = query.data.split(':')
        filepath = HANDSHAKES_FOLDER + filepath

        try:
            if action == 'pcap':
                if not os.path.isfile(filepath):
                    query.message.reply_text(f'Invalid file path: {filepath}')
                else:
                    logging.info('[TelegramBot] Sending handshake .pcap file.')
                    query.message.reply_document(open(filepath, 'rb'), filename=os.path.basename(filepath))

            elif action == 'hash':
                # Create /handshake_hashes subdir and filename
                filename = os.path.splitext(os.path.basename(filepath))[0]
                basepath = os.path.join(os.path.dirname(os.path.dirname(filepath)), 'handshake_hashes')
                fullpath = os.path.join(basepath, filename) + '.22000'
                if not os.path.exists(basepath):
                    os.makedirs(basepath)

                # Try making the file
                if not os.path.isfile(fullpath):
                    logging.info('[TelegramBot] Converting the pcap file to a hashcat .22000 hash.')
                    output = subprocess.getoutput(f'hcxpcapngtool -o {fullpath} {filepath}')
                    if not os.path.isfile(fullpath):
                        query.message.reply_text(f'Cannot crete hashcat file 🐱‍🚀 ')
                        if output:
                            if "missing frames" in output:
                                query.message.reply_text(
                                    f'Error: The pcap file does not contain needed frames, like authentication, association or reassociation.')
                            logging.info(f'[TelegramBot] Error converting file:\n {output}')
                        return

                query.message.reply_text(f'⏳ Generating... ', quote=False)
                query.message.reply_document(open(fullpath, 'rb'), filename=os.path.basename(fullpath))

            elif action == 'wlst':
                # Create /handshake_hashes subdir and filename
                filename = os.path.splitext(os.path.basename(filepath))[0]
                basepath = os.path.join(os.path.dirname(os.path.dirname(filepath)), 'handshake_hashes')
                fullpath_hash = os.path.join(basepath, filename) + '.22000'
                fullpath_wordlist = os.path.join(basepath, filename) + '.wordlist'

                if os.path.isfile(fullpath_wordlist):
                    query.message.reply_document(open(fullpath_wordlist, 'rb'),
                                                 filename=os.path.basename(fullpath_wordlist))
                else:
                    logging.info('[TelegramBot] Generating hash file .22000 from the captured handshake.')
                    query.message.reply_text(f'⏳ Generating... ', quote=False)

                    hcxpcapngtool_cmd = ['hcxpcapngtool', '-E', fullpath_wordlist, '-R', fullpath_wordlist, '-o',
                                         fullpath_hash, filepath]
                    subprocess.run(hcxpcapngtool_cmd, check=True)

                    if os.path.exists(fullpath_hash) and os.path.getsize(fullpath_hash) > 0:
                        logging.info('[TelegramBot] Generating .wordlist file from the hash file.')
                        hcxeiutool_cmd = ['hcxeiutool', '-i', fullpath_wordlist, '-d', fullpath_wordlist, '-x',
                                          fullpath_wordlist, '-c', fullpath_wordlist, '-s', fullpath_wordlist]
                        msg = subprocess.run(hcxeiutool_cmd, check=True)
                        logging.info(msg)

                        if os.path.exists(fullpath_wordlist) and os.path.getsize(fullpath_wordlist) > 0:
                            query.message.reply_document(open(fullpath_wordlist, 'rb'),
                                                         filename=os.path.basename(fullpath_wordlist))

        except FileNotFoundError as missing_file:
            logging.error(f"Cannot find '{missing_file.filename}'. Please compile and install hcxtools 6.2.7 ")
        except subprocess.CalledProcessError as e:
            logging.error(e)

    def on_handshake(self, agent, filename, access_point, client_station):
        display = agent.view()
        filename = filename.replace(HANDSHAKES_FOLDER, '')
        # Prevent Button_data_invalid error form telegram, occurring with callback_data length > 64 bytes

        try:
            # In case handshake callback gets called before on_internet_available
            if not self.updater:
                self.logger.info("[TelegramBot] Found a new handshake, connecting ...")
                self.init_bot()

            self.logger.info("[TelegramBot] Sending handshake")

            message = (f"New handshake captured by {pwnagotchi.name()}:\n\n"
                       f"  📶  {access_point['hostname']} \n")
            if access_point['vendor']:
                message += f"  🏭  {access_point['vendor']} \n"
            message += (f"  🚦  {access_point['rssi']} dBm\n\n"
                        f"\t 👤 {client_station['mac']} \n")
            if client_station['vendor']:
                message += f"  🏭  {client_station['vendor']}"

            if self.options['send_message']:
                keyboard = [[InlineKeyboardButton("pcap", callback_data=f"pcap:{filename}"),
                             InlineKeyboardButton("hashcat", callback_data=f"hash:{filename}"),
                             InlineKeyboardButton("wordlist", callback_data=f"wlst:{filename}")]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                self.updater.bot.sendMessage(chat_id=self.options['chat_id'],
                                             text=message,
                                             disable_web_page_preview=True,
                                             reply_markup=reply_markup)
                self.logger.info("[TelegramBot] Handshake message sent.")

            display.set('status', '[TelegramBot] handshake sent!')
            display.update(force=True)
        except Exception as e:
            self.logger.exception(f"[TelgramBot] Error while sending handshake: {e}")

    def terminate_program(self):
        logging.info("All tasks completed. Terminating program.")


if __name__ == "__main__":
    plugin = Telegram()
    plugin.on_loaded()
