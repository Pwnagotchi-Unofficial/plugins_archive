# hashespwnagotchi
credit to PwnPeter for their work with the conversions

original repo: https://github.com/PwnPeter/pwnagotchi-plugins
                        
## How to use

Add to `/etc/pwnagotchi/config.toml` :
```bash
main.custom_plugin_repos = [
 "https://github.com/evilsocket/pwnagotchi-plugins-contrib/archive/master.zip",
 "https://github.com/jjensn/hashespwnagotchi/archive/master.zip",
]
```

Next, `sudo pwnagotchi plugins update`, `sudo pwnagotchi plugins list`, and `sudo pwnagotchi install hashespwnagotchi`

Finally, edit `/etc/pwnagotchi/config.toml`:
```bash
main.plugins.hashespwnagotchi.api_key = "<api key>"
main.plugins.hashespwnagotchi.api_url = "https://hashes.pw/api"
main.plugins.hashespwnagotchi.enabled = true
```

## Plugins

### hashespwnagotchi.py

upload EAPOL captures to hashes.pw

