# News, project status and changelog

## 2024-10-31

**Katten can now host a basic game of Touch Pets: Cats!** While there is still a LOT of work to do (e.g. anything multiplayer related including Plus+ related stuff, player events, fixing furniture loot, making Katten easier to setup, etc) you can play the game now and have basic progress (like level, coins, inventory and of course your pets) saved.

I plan to write some documentation on how the Touch Pets server works, though at the moment it's sort of hard to describe. :P

It's worth noting that most of the progress was done in the past two days, since I both figured out:

1. how to run Touch Pets in a debugger (I just used GDB from the Cydia repos to jankily lanuch the app - debugserver was always fucking shit up and I never got it to work) leading me to find where exactly the game was crashing\* when trying to load the "Town" view (called the neighbourhood in the game), and
2. how the majority\*\* of the data was being loaded into objects (in short: in the XML parser it uses objective-c's property system to convert the running string into the proper type and then set it to the value of the current element name. I had initally just thought this was decompiler noise since the decompilation wasn't great. I was wrong :P).

\* To be specific the game was crashing when trying to do something related to getting profile pictures. The player's username was being set to NIL since I didn't provide (because I didn't know how!). It was trying to use the username as a dictionary key which throws an exception since it's NIL - providing the username in the player data actually made it work without doing anything else!

\*\* There are also some special cases where data is represented differently in the response XML. For example, inventory items use the attributes of an `inventory` tag in the `player` tag.

## 2024-07-24

The flask implementations of Plus+ and the Touch Pets server can now replace the older mess written in PHP.

### Plus+

In the `plus` folder, there is a reimplementation of the Plus+ server which supports making user accounts, some profile updates and preforming basic user data operations (mostly used for cloud saves). No other part of Plus+ is implemented, at the moment.

It has been tested to allow *Rolando*, *Topple* and *Touch Pets Cats* to start up. *Rolando* is frequently used for testing, so other games might have more subtle bugs I didn't notice.

Currently the primary focus is on older Plus+ games, since they seem easier to test with.

### Touch Pets

For Touch Pets, a placeholder implementation needed to get the game booting is available in `touchpet`.

### Router

I hacked together a small router (in `router`) so you can proxy all requests for the Plus+ and Touch Pets server to that.

## 2024-02-26

There is currently a very basic reimplementation of the server written in PHP in the php folder. It can get the games to boot, but doesn't save any progress and the code is a mess.

Once I am able to start this project again, I plan to switch to using a more modern web framework and to split Plus+ and Touch Pets server so that the Plus+ reimplementation can be used for any game.
