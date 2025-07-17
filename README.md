<img src="res/KattenLogo.svg" width="100%"/>

# Katten Project

Katten is a reverse engineering and reimplementation of the server software for the Plus+ social gaming network and the *Touch Pets* series of games.

If you want to discuss or help with reverse engineering Plus+, please consider [joining the Plus+ Discord server](https://discord.gg/Y6KwXfM6at).

## Status

Katten is currently in its early stages. See [the project news](NEWS.md) and the [Plus+ server readme](plus/README.md) for status updates and what works.

### Supported Games

These games are tested. Other games may work, but YMMV.

 * Touch Pets Dogs 2<sup>1</sup> (2010)
 * Touch Pets Cats (2010)
 * Touch Pets Dogs<sup>1</sup> (2009)
 * Rolando 2 (2009)
 * Topple 2 Plus (2009)
 * Rolando (2008)

<sup>1</sup> Not actually tested, but very similar to supported games and should work with minor tweaking.

## Setup

### Requirements

 * Up to date Linux distro
 * Jailbroken iPhone running iOS 7 or older with AppSync Unified installed
   * Newer iOS versions are not generally compatible with Plus+ games
   * Plus+ games don't run on touchHLE (yet)
 * An IPA for the game you want to play, if it's not already installed
   * You will also need the Terminal and the command line version of `installipa` installed
   * You may also want to use iFile to upload the APK

### Server

#### Clone repo

Firstly, in a terminal, clone the Katten repo and enter the directory:

```sh
git clone https://github.com/knot126/Katten
cd Katten
```

#### Install dependencies

Install:

 * [MongoDB](https://www.mongodb.com/try/download/community-edition/releases)
 * mitmproxy
 * Flask
 * pymongo
 * argon2-cffi (for Python, optional)

Note: MongoDB is not generally available in most distros' repos. It's fine to use a "portable" version that has been extracted from one of the tarballs instead of properly installing it. (We will probably switch away from MongoDB soon anyway.)

On Arch Linux, you can run:

```sh
sudo pacman -Syu mitmproxy python-flask python-pymongo python-argon2_cffi
```

Then download MongoDB and extract it somewhere.

#### Configuration

The is a script (`run.py`) which starts all of the needed servers automatically. It needs `runconfig.toml` to tell it where `mongod` is, where the database is, and which `mitmproxy` command to use.

```toml
mongo_exec = "mongod"
mongo_db = "/home/dragon/Documents/katten-data"
mitmproxy_exec = "mitmweb"
```

 * `mongo_exec` is the command (or path) for `mongod` (the MongoDB server)
 * `mongo_db` is the path to the MongoDB database
 * `mitmproxy_exec` is the command (or path) for `mitmproxy`

#### Starting the server

To start the server, just run:

```sh
./run.py
```

... in the Katten directory.

### Game

Games need to have a slight patch applied so they don't use HTTPS. There is a generic patch script provided in the tools directory that can do this. To patch a game:

 * Extract your game's main binary from the IPA; this is usually a file with the same name as the `.app` folder with no extension
 * Open a terminal in the [`tools`](tools) folder
 * Run the patch script on your game's binary: `./nohttpspatch.py <path to game binary>`
 * This puts out one file for each architecture the game binary supports. Choose the one that matches what your phone has.
 * Either:
   * Replace the binary in the IPA with the patched one and install it
   * Upload the binary directly to the installed app dir using iFile (just make sure it's correctly named and has the execute bit set after uploading)
