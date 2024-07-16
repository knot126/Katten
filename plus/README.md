# Katten Plus+ server

This is the module which replicates the Plus+ server's API.

Notes:

* This only works with earlier games at the moment, Touch Pets will be a later focus.
* If you want to see the old work for Katten which can kind of get Touch Pets booting check out the `php` folder.

## Depends

You need to install flask, pymongo and argon2-cffi.

### Arch Linux

```sh
sudo pacman -Syu python-flask python-pymongo python-argon2_cffi
```

### Using pip

```sh
python3 -m pip install flask pymongo argon2-cffi
```

## Design

*TODO: Write this.*

## Testing

Testing can be done (hopefully!) without a jailbroken iPhone by using mitmproxy as a reverse proxy to the Plus server:

*start plus server:*

```sh
# In plus folder:
$ flask run --debug
```

*start reverse proxy:*

```sh
$ mitmweb --mode reverse:http://localhost:5000
```

Then set your iPhone to use a proxy at your computer's IP on port 8080 (mitmproxy default).
