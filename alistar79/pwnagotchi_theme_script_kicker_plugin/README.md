# Pwnagotchi theme/script kicker plugin

This is my first try at a pwnagotchi plugin hacked together with code from [PersephoneKarnstein](https://github.com/PersephoneKarnstein/egirl-pwnagotchi), [sixt0o](https://github.com/sixt0o/f0xtr0t) and [tjbishop07](https://github.com/tjbishop07/pwnagotchi-plugins/blob/main/wardrive.py).

When you click on the plugin name after enabling it, it displays a webpage with buttons that call scripts I wrote that change the looks of the UI and led.

## Requirements

For the faces stuff to work you will need to follow this comment [here](https://github.com/PersephoneKarnstein/egirl-pwnagotchi/issues/1#issuecomment-1397549459)

## Installation

1. Copy the contents of the root folder to /root

2. Copy the contents of installed-plugins folder to /usr/local/share/pwnagotchi/installed-plugins

3. Copy the contents of pwnagotchi folder to /etc/pwnagotchi

## Usage

1. Add the following text to /etc/pwnagotchi/config.toml:

`main.plugins.themes.enabled = true`

2. Navigate to [http://pwnagotchi.local:8080/plugins/themes](http://pwnagotchi.local:8080/plugins/themes).  You may need this to be the IP of your pwnagotchi in some cases.

3. Click on one of the buttons as you desire then wait till the pwnagotchi process restarts to see your changes.

## Improvements

This could be a lot more sophisticated and allow for multiple aspects to be changed simultaniously and selection of image sets for faces or led pattern sets rather than flip flow between two option or cycle through many.

## Additional plugins

I've also started adding my modified plugins to installed-plugins here too.  Currently telegram.py with additional functionality.
