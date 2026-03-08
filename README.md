<img src="res/KattenLogo.svg" width="100%"/>

# Katten Project

Katten is a reverse engineering and reimplementation of the server software for the Plus+ social gaming network and the *Touch Pets* series of games.

If you want to discuss or help with reverse engineering Plus+, please consider [joining the Plus+ Discord server](https://discord.gg/Y6KwXfM6at).

## Status

Katten is currently in its early stages. See [the project news](NEWS.md) and the [Plus+ server readme](plus/README.md) for status updates and what works.

### Game Status

These games are tested. Other games may work, but YMMV.

<table>
  <tr>
    <th>Game</th>
    <th>Notes</th>
  </tr>
  <tr>
    <td>
    Touch Pets Cats (2010)<br/>
    Touch Pets Dogs 2 (2010)<br/>
    Touch Pets Dogs<sup>1</sup> (2009)
    </td>
    <td>
    Relies on <code>touchpet</code> server
    </td>
  </tr>
  <tr>
    <td>
    Rolando 2 (2009)<br/>
    Topple 2 Plus (2009)<br/>
    Rolando (2008)
    </td>
    <td>
    Only needs Plus+ server, mostly working
    </td>
  </tr>
</table>

<sup>1</sup> Not actually tested, but very similar to supported games and should work with minor tweaking.

## Setup

### Requirements

 * Up to date Linux distro
 * Jailbroken iPhone running iOS 6 or older with AppSync Unified installed
   * Newer iOS versions are not generally compatible with Plus+ games
   * Plus+ games don't run on touchHLE (yet)
   * You can probably jailbreak your device with [Legacy iOS Kit](https://github.com/LukeZGD/Legacy-iOS-Kit)
 * An IPA for the game you want to play, if it's not already installed
   * If you have the app on an old device, [please consider dumping the IPA](https://www.reddit.com/r/LegacyJailbreak/wiki/guides/crackingapps/) of the app before starting if you already have it on your device.
   * If it's not already installed, you will also need the Terminal and the command line version of `installipa` installed. You may also want to use iFile to upload the IPA to your device.

### Server

#### Clone repo

Firstly, in a terminal, clone the Katten repo and enter the directory:

```sh
git clone https://github.com/knot126/Katten
cd Katten
```

#### Install dependencies

Install:

 * flask
 * sqlalchemy
 * argon2-cffi (optional)
 * mitmproxy (optional, for development)

On Arch Linux, you can run:

```sh
sudo pacman -Syu python-flask python-sqlalchemy python-argon2_cffi mitmproxy
```

#### Starting the server

Use `run.py` which will start all needed servers:

```sh
./run.py
```

To start the server using mitmproxy, use the `--mitm` argument with the mitmproxy command you prefer:

```sh
./run.py --mitm mitmweb
```

You can also start only the Plus+ server:

```sh
./run.py --no-touch-pets
```

#### Configuration and file storage

By default, Katten will use SQLite for its database, and everything will be stored in the `.katten` folder of your home directory.

Currently Katten cannot be easily confiured without editing each server's `config.py`.

### Game

Games need to have a slight patch applied so they don't use HTTPS. There is a generic patch script provided in the tools directory that can do this. To patch a game:

 * Extract your game's main binary from the IPA; this is usually a file with the same name as the `.app` folder with no extension
 * Open a terminal in the [`tools`](tools) folder
 * Run the patch script on your game's binary: `./nohttpspatch.py <path to game binary>`
 * This puts out one file for each architecture the game binary supports. Choose the one that matches what your phone has.
 * Either:
   * Replace the binary in the IPA with the patched one and install it
   * Upload the binary directly to the installed app dir using iFile (just make sure it's correctly named and has the execute bit set after uploading)
