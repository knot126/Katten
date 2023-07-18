# Plus+

This is the main social API used for *Touch Pets: Cats* (in addition to some other games!) and takes care of most of the game's online features.

## General info

For most routes, `POST` requests are submitted to the given endpoint using standard query encoding for the body and it either responds with a JSON (`application/json`) or apple binary plist (`application/binary-plist`) body. Some games do not accept the binary plists, namely android games, so JSON is probably better to use.

> **See also**: `NGNetworkOperation::_parseResponse:body:error:`

## API URL format

```
/{version}/{game_name}/{route_params ...}
```

* `version`: The version of the API, probably `1`.
* `game_name`: The human name of the game we are making the request as, for example `PetCat`.
* Route info follows this.

I will use `{service}` to represent the path to the service for the given game.

## Users

### Regular vs Lite users

Regular users have a Gamer Tag(tm) and a password, each at least four characters long, and can interact with the full featureset for any given game. Lite users, on the other hand, seem to be per-device and are restricted from using social features. This is very similar to the Geometry Dash yellow/green user system, with yellow users being the regular users and green users being the lite users.

### Create new user

Creates a new user account.

`POST` `{service}/users`

Request:

*N/A*

Response:

*N/A*

## Sessions

Plus+ seems to use oauth to start a login. This makes some sense as you can use oauth to sign in for many things.

### Base login info

* `timezone`: Current user timezone as `Country/Name (TLA) offset +0000`
* `device_type`: Operating system the device is running
* `os_version`: Version of the operating system being run
* `id`: UDID of the device (or simiar value)
* `locale`: Locale in standard format (`{language}_{COUNRTY}` e.g. `en_GB`)

### Log in using auth token

Log in using a given auth token.

```
POST /session
```

Request:

* \[*Base login info*\]
* `auth_token`: The auth token to log in with.

Response:

*N/A*

### Log in using username and password

Log in using the user's username and password.

```
POST /1/{appname}/session
```

Request:

* \[*Base login info*\]
* `gamertag`: The username of the user
* `password`: The user's password

Response:

*N/A*

### Authorise session for a game using oauth

```
POST /1/{appname}/oauth/authorize_new
```

Request:

* `key`: The app's oauth consumer key

Response:

*N/A*

### Check session status

Check if a session is still valid.

```
GET /session
```

Request:

* \[*Base login info*\]

Response:

*N/A*

### Update device token

Device tokens are used for push notifications.

```
POST /session
```

Request:

* `device_token`

Response:

*N/A*

> **See**: `PlusRequest.updateSessionDeviceToken`
