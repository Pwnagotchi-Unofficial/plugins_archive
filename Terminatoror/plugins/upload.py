import os
import logging
import requests
from datetime import datetime
from threading import Lock
from pwnagotchi.utils import StatusFile, remove_whitelisted
from pwnagotchi import plugins
from json.decoder import JSONDecodeError
import shutil
import time


class WpaSec(plugins.Plugin):
    __author__ = 'Terminatoror + Artemio + 33197631+dadav@users.noreply.github.com'
    __version__ = '2.1.0'
    __license__ = 'GPL3'
    __description__ = 'This plugin automatically uploads handshakes to https://wpa-sec.stanev.org'

    def __init__(self):
        self.ready = False
        self.lock = Lock()
        self.sorted_folder = '/root/sorted_folder'
        self.uploaded_folder = '/root/uploaded_folder'
        self.options = dict()
        

        try:
            self.report = StatusFile('/root/.wpa_sec_uploads', data_format='json')
        except JSONDecodeError:
            os.remove("/root/.wpa_sec_uploads")
            self.report = StatusFile('/root/.wpa_sec_uploads', data_format='json')
        self.options = dict()
        self.skip = list()

    def _upload_to_wpasec(self, path, timeout=30):
        """
        Uploads the file to https://wpa-sec.stanev.org, or another endpoint.
        """
        with open(path, 'rb') as file_to_upload:
            cookie = {'key': self.options['api_key']}
            payload = {'file': file_to_upload}

            try:
                result = requests.post(self.options['api_url'],
                                       cookies=cookie,
                                       files=payload,
                                       timeout=timeout)
                if ' already submitted' in result.text:
                    logging.debug("%s was already submitted.", path)
            except requests.exceptions.RequestException as req_e:
                raise req_e

    def _download_from_wpasec(self, output, timeout=30):
        """
        Downloads the results from wpasec and safes them to output

        Output-Format: bssid, station_mac, ssid, password
        """
        api_url = self.options['api_url']
        if not api_url.endswith('/'):
            api_url = f"{api_url}/"
        api_url = f"{api_url}?api&dl=1"

        cookie = {'key': self.options['api_key']}
        try:
            result = requests.get(api_url, cookies=cookie, timeout=timeout)
            with open(output, 'wb') as output_file:
                output_file.write(result.content)
        except requests.exceptions.RequestException as req_e:
            raise req_e
        except OSError as os_e:
            raise os_e


    def on_loaded(self):
        """
        Gets called when the plugin gets loaded
        """
        if 'api_key' not in self.options or ('api_key' in self.options and not self.options['api_key']):
            logging.error("WPA_SEC: API-KEY isn't set. Can't upload to wpa-sec.stanev.org")
            return

        if 'api_url' not in self.options or ('api_url' in self.options and not self.options['api_url']):
            logging.error("WPA_SEC: API-URL isn't set. Can't upload, no endpoint configured.")
            return

        if 'whitelist' not in self.options:
            self.options['whitelist'] = list()

        self.ready = True
        logging.info("WPA_SEC: plugin loaded")

    def on_webhook(self, path, request):
        from flask import make_response, redirect
        response = make_response(redirect(self.options['api_url'], code=302))
        response.set_cookie('key', self.options['api_key'])
        return response
    
    def find_largest_files(self, files_dict, source_folder_path):
        largest_files = {}
        for name, files in files_dict.items():
            logging.debug(f"Group '{name}': Files {files}")
            if files:  
                largest_file = max(files, key=lambda x: os.path.getsize(os.path.join(source_folder_path, x)))
                largest_files[name] = largest_file
                logging.debug(f"Largest file for group '{name}': {largest_file}")
            else:
                logging.warning(f"No files found for group '{name}'.")
        return largest_files


    def copy_largest_files(self, handshake_dir):
        files_dict = {}

        all_files = os.listdir(handshake_dir)
        logging.info(all_files)

        for file in all_files:
            name = file.split('_')[0]
            if name not in files_dict:
                files_dict[name] = []
                logging.info("checkpoint 1")
            files_dict[name].append(file)

        largest_files = self.find_largest_files(files_dict, handshake_dir)

        for name, largest_file in largest_files.items():
            logging.info("checkpoint 2")
            source_path = os.path.join(handshake_dir, largest_file)
            destination_path = os.path.join(self.sorted_folder, largest_file)

            logging.info(f"Source path: {source_path}")
            logging.info(f"Destination path: {destination_path}")

            if not os.path.exists(destination_path):
                logging.info("checkpoint 3")

                uploaded_path = os.path.join(self.uploaded_folder, largest_file)
                if not os.path.exists(uploaded_path):

                    shutil.copyfile(source_path, destination_path)
                    logging.info(f"File '{largest_file}' copied to '{self.sorted_folder}'.")
                else:
                    logging.info(f"File '{largest_file}' already exists in '{self.uploaded_folder}'. Skipped.")
            else:
                logging.info(f"File '{largest_file}' already exists in '{self.sorted_folder}'. Skipped.")

    def on_internet_available(self, agent):


        if not os.path.exists(self.sorted_folder):
            os.makedirs(self.sorted_folder)
            logging.info(f"Directory '{self.sorted_folder}' created.")
        else:
            logging.info(f"Directory '{self.sorted_folder}' already exists.")
        
        if not os.path.exists(self.uploaded_folder):
            os.makedirs(self.uploaded_folder)
            logging.info(f"Directory '{self.uploaded_folder}' created.")
        else:
            logging.info(f"Directory '{self.uploaded_folder}' already exists.")


        config = agent.config()
        handshake_dir = config['bettercap']['handshakes']
        self.copy_largest_files(handshake_dir)
        logging.info("moved sorted files to /root/sorted_folder")

        config = agent.config()
        display = agent.view()
        logging.info("checkpoint 4")
        
        sorted_folder = '/root/sorted_folder'    
        sorted_filenames = os.listdir(sorted_folder)
        sorted_paths = [os.path.join(sorted_folder, filename) for filename in sorted_filenames if
                        filename.endswith('.pcap')]
        sorted_paths = remove_whitelisted(sorted_paths, self.options['whitelist'])
        handshake_new = set(sorted_paths) - set(self.skip)
        logging.info("handshakes: %s", handshake_new)


        if handshake_new:
            logging.info("WPA_SEC: Internet connectivity detected. Uploading new handshakes to wpa-sec.stanev.org")
            for idx, handshake in enumerate(handshake_new):
                display.set('status', f"Uploading handshake to wpa-sec.stanev.org ({idx + 1}/{len(handshake_new)})")
                display.update(force=True)
                try:
                    logging.info("checkpoint 5")
        
                    self._upload_to_wpasec(handshake)
                    logging.info("WPA_SEC: Successfully uploaded %s", handshake)
                    destination_path = os.path.join('/root/uploaded_folder', os.path.basename(handshake))
                    shutil.move(handshake, destination_path)
                    logging.info("WPA_SEC: Moved file into uploaded_folder after successful upload: %s", handshake)
                except requests.exceptions.RequestException as req_e:
                    self.skip.append(handshake)
                    logging.info("WPA_SEC: %s", req_e)
                    continue
                except OSError as os_e:
                    logging.info("WPA_SEC: %s", os_e)
                    continue

        if 'download_results' in self.options and self.options['download_results']:
            cracked_file = os.path.join(handshake_dir, 'wpa-sec.cracked.potfile')
            if os.path.exists(cracked_file):
                last_check = datetime.fromtimestamp(os.path.getmtime(cracked_file))
                if last_check is not None and ((datetime.now() - last_check).seconds / (60 * 60)) < 1:
                    return
            try:
                self._download_from_wpasec(os.path.join(handshake_dir, 'wpa-sec.cracked.potfile'))
                logging.info("WPA_SEC: Downloaded cracked passwords.")
            except requests.exceptions.RequestException as req_e:
                logging.debug("WPA_SEC: %s", req_e)
            except OSError as os_e:
                logging.debug("WPA_SEC: %s", os_e)
