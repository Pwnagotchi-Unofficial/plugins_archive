
# Birthday Plugin for Pwnagotchi

The Birthday Plugin is a plugin for your Pwnagotchi that automatically calculates and displays either the age or the birthday of your Pwnagotchi! It provides a customizable UI element that shows either the age in years, months, and days, or the birthday in a formatted date. 

--Age is based on the born_at value in the brain.json file.

**Inspired by Age/Strength Plugin originally written by HannaDiamond.**

------------------------------------------------------------------------------------------------------------------------------------------------------------------------
<img width="1436" alt="Screenshot 2023-06-17 at 8 22 44 PM" src="https://github.com/nullm0ose/pwnagotchi-plugins/assets/77137650/9835f8ca-edc0-4556-941f-2a3dc916f43b">

------------------------------------------------------------------------------------------------------------------------------------------------------------------------
<img width="1438" alt="Screenshot 2023-06-17 at 11 06 18 PM" src="https://github.com/nullm0ose/pwnagotchi-plugins/assets/77137650/518356f6-38f8-4363-9e03-703a5208dcdb">


------------------------------------------------------------------------------------------------------------------------------------------------------------------------


## Requirements

- RTC (Real-Time Clock) synced to the correct time.
- I2C interface configured.

## Compatibility

The Birthday Plugin has been tested on Pwnagotchi version 1.5.3 and 1.5.5, and it works with Raspberry Pi Zero W and WaveShare 2.13inch V3 (Black and White) display. It also functions in the WebUI.

## Installation

1. Create custom plugins directory if you havent already:
   ```
   mkdir /etc/pwnagotchi/custom-plugins
   ```

2. Download the pluglin:
   ```
   cd /etc/pwnagotchi/custom-plugins
   ```
   ```
   git clone https://github.com/nullm0ose/pwnagotchi-plugin-birthday.git
   ```

4. Copy the `birthday.py` file to the custom plugins directory:
   ```
   cp /etc/pwnagotchi/custom-plugins/pwnagotchi-plugin-birthday/birthday.py /etc/pwnagotchi/custom-plugins
   ```

3. Add the plugin configuration to the `config.toml` file:
   ```toml
   main.plugins.birthday.enabled = true
   main.plugins.birthday.age_x_coord = 0
   main.plugins.birthday.age_y_coord = 32
   main.plugins.birthday.show_age = true
   main.plugins.birthday.show_birthday = false
   ```

   Adjust the `age_x_coord` and `age_y_coord` values to customize the position of the age display on the Pwnagotchi UI.

4. Fully reboot Pwnagotchi:
   ```
   sudo reboot
   ```

## Usage

By default, the plugin is configured to display the age. To switch to displaying the birthday, modify the `show_age` and `show_birthday` options in the `config.toml` file as follows:

- To show the age:
  ```toml
  show_age = true
  show_birthday = false
  ```

- To show the birthday:
  ```toml
  show_age = false
  show_birthday = true
  ```

## Customization

You can customize the position of the displayed age or birthday on the Pwnagotchi UI by modifying the following options in the `config.toml` file:

- `age_x_coord`: X-coordinate of the age or birthday display.
- `age_y_coord`: Y-coordinate of the age or birthday display.

Feel free to adjust these values according to your preference.

## Important Notes

Anytime you switch the config.toml to show its age or its birthday you must perform a full reboot of your Pwnagotchi!!

As of now this plugin is configured to display either the birthday OR the age. I personally found it to be redundant to display both. This could be pushed in the next version if theres a reasonable amount of requests for this implementation 


## Author

- Author: nullm0ose

## Version

- Version: 1.0.2

## License

This plugin is licensed under the MIT License.
