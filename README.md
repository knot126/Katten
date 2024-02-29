<img src="res/KattenLogo.svg" width="100%"/>

# Katten Project

Katten is a reverse engineering, documentation and attempt at a full reimplementation of the server software for the *Touch Pets* series of games. It is also a partial reimplementation for games which require or use the Plus+ network. These games were shut down over 10 years ago on 31 March 2013, but we would like to play them again.

## Status

There is currently a very basic reimplementation of the server written in PHP in the `php` folder. It can get the games to boot, but doesn't save any progress and the code is a mess.

Once I am able to start this project again, I plan to switch to using a more modern web framework and to split Plus+ and Touch Pets server so that the Plus+ reimplementation can be used for any game.
