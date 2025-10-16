# Minecraft Tools

Welcome to Minecraft Tools by Rooh2os!

## Feature overview:

### Ping a server

Pinging a server has two methods
1. Using [mcsrvstat.us](https://mcsrvstat.us)
1. Using a standard ping (using the pythonping module)

[mcsrvstat.us](https://mcsrvstat.us) gives a more detailed view and includes info like
* MoTD
* Player count
* Version
* Mods
* Plugins
* And many more

Pythonping just pings the server to see if it is online.

### Make a template resource pack

Making a template pack retrieves the data from Mojang and turns it into an editable resource pack for you.

### Get a user's skin

Getting a user's skin downloads a viewable skin from [mineskin.eu](https://mineskin.eu).

### Get a user's head

Getting a user's head downloads a viewable head from [mineskin.eu](https://mineskin.eu).

### Get a user's usable skin

Getting a user's skin downloads a usable skin from [mineskin.eu](https://mineskin.eu) so that it can be used in game.

### Making a server alias

Making a server alias takes a name (e.g. Hypixel) and registers a server address to it (e.g. [mc.hypixel.net](https://hypixel.net)) so that it can be used to ping a server.

### Calculate \# of items to stacks

This one is pretty self explanatory, number of items in number of stacks out.

### Calculate \# of stacks to items

This one is pretty self explanatory, number of stacks in number of items out.

## Config

To configure Minecraft Tools open config.txt (Gets generated when first running the program.)

### "Open images": true/false

Open images can be used to disable the opening of images when the download is complete.

### "Save individual icons": true/false

Save individual icons is used to enable the saving of each server icon separately.

### "Use advanced ping": true/false

Use advanced ping is used to switch between using [mcsrvstat.us](https://mcsrvstat.us) or Pythonping

### "Max saved servers": above 0 integer

Max saved servers is used to change how many servers can be saved to your history

### "Starting value for lists": string

Starting value for lists is used to change how much lists are indented

### "Debug mode": true/false

### Default config

```
{
        "Open images": true,
        "Save individual icons": false,
        "Use advanced ping": true,
        "Max saved servers": 10,
        "Starting value for lists": "    ",
        "Debug mode": false
}
```