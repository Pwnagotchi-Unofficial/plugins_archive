# Installation Guide for Plugins via Custom Repository Link with Web UI

This guide explains how to install these plugins for the Pwnagotchi device: **AGE**, **EXP**, **SIGSTR**, and **gameifyXP**.

## Prerequisites

Before installing these plugins, ensure you have the following:

- A Pwnagotchi device set up and running.
- Basic knowledge of working with the Pwnagotchi device.
- Access to the internet to download plugin files.

## Installation Steps

### 1. Access Config.toml
1. sudo nano /etc/pwnagotchi/config.toml

### 2. Add Custom Repository Link

1. Add a custom repository link.Add EXACTLY This--> "https://github.com/bryzz42o/Pwnagotchi-fsociety-plugins/archive/master.zip",

### 3. Update Plugins
1. sudo pwnagotchi plugins update && upgrade
2. sudo pwnagotchi plugins list
3. sudo pwnagotchi plugins install (what plugin you want)

4. Add the following lines to the `config.toml` file under the `main.plugins` section to enable the plugins:

```toml
main.plugins.AGE.enabled = true

main.plugins.EXP.enabled = true

main.plugins.SIGSTR.enabled = true

main.plugins.gameifyXP.enabled = true

NOW REBOOT and Enable with WebUI 
