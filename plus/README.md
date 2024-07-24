# Katten Plus+ server

This is the module which replicates the Plus+ server's API.

Notes:

* This only works with earlier games at the moment, Touch Pets will be a later focus.
* If you want to see the old work for Katten which can kind of get Touch Pets booting check out the `php` folder.

## Status

- [ ] Users and sessions
  - [x] Create an account
  - [x] Log in with username and password
  - [x] Log in with existing session
  - [ ] Query session status for device and game combonation
  - [ ] Update device token
  - [ ] Password reset
  - [ ] OAuth 1.0 support
    - Note: Currently there is a hack that just uses the session token instead of an oauth token. 
  - [ ] ...
- [ ] Friends and enimies
  - [ ] Find users
  - [ ] Add and remove friends
  - [ ] ...
- [ ] Profile
  - [ ] Badges
    - [x] Choice from static selection
    - [ ] Uploading custom badges (for admins)
  - [x] Update profile (badge, name, email, phone number, etc.)
  - [ ] Custom photo
  - [ ] ...
- [ ] Score
- [ ] Achivements
- [ ] User data
  - [x] Set a key to a value
  - [x] Get a value for a key
  - [x] List all keys
  - [ ] Respects privacy setings
  - [ ] ...
- [ ] Game info
- [ ] Leaderboards
- [ ] ...

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

Testing can be done with a jailbroken iPhone and modified game binary by using mitmproxy as a reverse proxy to the Plus server:

*start plus server:*

```sh
# In plus folder:
$ flask run --debug
```

(Also remember to run MongoDB)

*start reverse proxy:*

```sh
$ mitmweb --mode reverse:http://localhost:5000
```

Then set your iPhone to use a proxy at your computer's IP on port 8080 (mitmproxy default).
