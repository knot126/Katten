# Katten Plus+ server

This is the module which replicates the Plus+ server's API.

Notes:

* This only works with earlier games at the moment, Touch Pets will be a later focus.
* If you want to see the old work for Katten which can kind of get Touch Pets booting check out the `php` folder.

## Feature status

- [x] Register
- [x] Log in
- [x] Continue a session
- [ ] Password reset
- [x] Update account details
- [x] Badges
  - Note: Could be improved
- [ ] Custom friends-only photo
- [ ] Games list and registration
- [ ] Buddies (friends and enimies)
- [x] Key-value storage (cloud save)
- [ ] Gamer score
- [ ] Leaderboards
- [ ] Achievements
- [ ] Invitations
- [ ] Admin features
- [ ] Flagging

And probably other features too.

### Features that will not be implemented

- Push notifications

### Notes

- Plus+ uses OAuth 1.0 to grant games access to parts of a User's Plus account, but currently there is a hack that just uses the session token instead of an oauth token.
- Some integer error codes are not accurate and probably completely lost to time

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
