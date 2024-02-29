# Plus+

Plus+ is the main social API used for *Touch Pets: Cats* (in addition to some other games!) and takes care of most of the game's online features.

## History

It's helpful to have a bit of history about these APIs before we begin to talk about them.

The Plus+ social gaming service was launched by Ngmoco on 15 June 2009, when they were still an independent company. It was provided to third party developers via an SDK, and used a custom API for interacting with the server.

On 12 October 2010, Ngmoco was accquired by DeNA, a Japanese game developer and publisher. DeNA had its own social gaming service, *Mobage Town*, which launched in 2006 and was mainly restricted to Japan.

> **Note**: There are two services named Mobage: *Mobage Town* (later renamed to just *Mobage*) and *Yahoo! Mobage*. I'm not currently sure what the difference between them is, other than the site hinting that Mobage => Phones and Yahoo => PC.

"Mobage Town" was renamed to simply Mobage in March 2011, and the Plus+ service was also rebranded to Mobage. Internally, these seem to be called "Mobage East" and "Mobage West" respectively, since they have different APIs and features.

> **Note**: There is also a third API for China, which is split into two different APIs for simple and traditional Chinese. Yes, it seems like it's actually different from the Japanese one. Don't ask me why they did this, they must have been insane.



### References

* https://en.wikipedia.org/wiki/Plus%2B
* https://en.wikipedia.org/wiki/Ngmoco
* https://en.wikipedia.org/wiki/DeNA
* https://en.wikipedia.org/wiki/Mobage
* https://www.mbga.jp/
* https://docs.mobage.com/display/cnspapp/ngcore
* https://web.archive.org/web/20130401161156/http://www.plusplus.com/
* ngCore docs (see 'Resources' section)
* Some original research into ngCore engine

## General info

For most routes, `POST` requests are submitted to the given endpoint using standard query encoding for the body and it either responds with a JSON (`application/json`) or apple binary plist (`application/binary-plist`) body. Some games do not accept the binary plists, namely android games, so JSON is probably better to use.

> **See also**: `NGNetworkOperation::_parseResponse:body:error:`

> **Note**: Some games may also have a seprate server used for the actual gameplay events (e.g. real time network multiplayer movement info).

## API URL format

```
/{version}/{appname}/
```

* `version`: The version of the API, this is only ever `1`.
* `appname`: Name of the app, for example `PetCat`.

## Users

### Regular vs Lite users

Regular users have a Gamer Tag(tm) (called a gamername in the UI) and a password, each at least four characters long, and can interact with the full featureset for any given game. Lite users, on the other hand, seem to be per-device and are restricted from using social features.

> **Note**: This is somewhat similar to the Geometry Dash yellow/green user system, with yellow users being the regular users and green users being the lite users.

### Create new user

Creates a new user account.

```
POST /{version}/{appname}/users
```

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
POST /{version}/{appname}/session
```

Request:

* \[*Base login info*\]
* `auth_token`: The auth token to log in with.

Response:

*N/A*

### Log in using username and password

Log in using the user's username and password.

```
POST /{version}/{appname}/session
```

Request:

* \[*Base login info*\]
* `gamertag`: The username of the user
* `password`: The user's password

Response:

*N/A*

### Authorise session for a game using oauth

```
POST /{version}/{appname}/oauth/authorize_new
```

Request:

* `key`: The app's oauth consumer key

Response:

*N/A*

### Check session status

Check if a session is still valid.

```
GET /{version}/{appname}/session
```

Request:

* \[*Base login info*\]

Response:

*N/A*

### Update device token

Device tokens are used for push notifications.

```
POST /{version}/{appname}/session
```

Request:

* `device_token`

Response:

*N/A*

> **See**: `PlusRequest.updateSessionDeviceToken`

## Resources

* https://docs.mobage.com/public/ngcore/ &mdash; Original documentation for NgCore engine, still up! You might want to make a local mirror of it just in case.
* *We Rule* (Android)
* *Transformers: Legends* (Android)
* *Touch Pets: Cats* (iOS v1.4)

### Wanted docs and SDKs

* Plus+ SDK and docs
