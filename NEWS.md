# News, project status and changelog

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
