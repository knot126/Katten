# Katten Plus+ server

This is the module which replicates the Plus+ server's API.

## Project Status

### What works

- Most account related actions: Register, log in, continue a session, update account details
- Games list
- Key-value storage (cloud save)
- Buddies (friends and enimies - WIP implementation)
- Leaderboards
- User flagging (but no admin UI yet)

### What does not work yet

- Admin features
- Gamer score
- Custom friends-only photo
- Direct messages (for later versions of Plus+/Mobage)
- Password resetting
- Achievements
- Invitations to join Plus+

### What will probably never be supported

- Anything that relies on push notifications, like challenges
- Anything that relies on purchases or real-world money
- Anything related to social media accounts (most of these social medias are dead or have fallen out of use anyway)

### Notes

- Plus+ uses OAuth 1.0 to grant games access to parts of a User's Plus account, but currently there is a hack that just uses the session token instead of an oauth token.
- Some integer error codes are not accurate and probably completely lost to time

## Depends

You need to install `flask`, `sqlalchemy` and `argon2-cffi`.

### Arch Linux

```sh
sudo pacman -Syu python-flask python-argon2_cffi python-sqlalchemy
```

### Using pip

```sh
python3 -m pip install flask argon2-cffi sqlalchemy
```

## Design

*TODO: Write this.*
