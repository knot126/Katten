# Touch Pets Server

The **Touch Pet Server** is the server originally hosted at `cats.ngmoco.com` and takes care of all *Touch Pets: Cats* game specific server actions and storage. Most notably, it handles player and cat actions.

Most interaction happens using a single route: `http://cats.ngmoco.com/touchpet/`. This route expects a `cmd` parameter which determines the actual command that will be executed. Data is returned in an XML format, which is parsed in `SERemoteMgr`, which is an `NSXMLParserDelegate` that processes responses as you would expect it to.

## Commands

### `player`

This presumably gets player info as well as sets the session secret.

> **Note**
> 
> Katten Server does not use OAuth, so any session tokens or secrets are set to the session ID on the katten server.

#### Request example

```
version=1&cmd=player&playerID=12&playerID=12&sessionToken=d2d4a592700b0920658e5d56ed50ebfaa82b1f4a3e105e9bcfd8bcbb081c2e87&sessionSecret=d2d4a592700b0920658e5d56ed50ebfaa82b1f4a3e105e9bcfd8bcbb081c2e87
```

### `setplayerproperty`

Sets a property value on a player.

See: `SELoginMgr::setupInitialPlayerModel:`

#### Request example

```
version=1&cmd=setplayerproperty&categoryID=10&propertyID=0&propertyvalue=1&ifgreaterthan=0&playerID=12&sessionToken=d2d4a592700b0920658e5d56ed50ebfaa82b1f4a3e105e9bcfd8bcbb081c2e87
```

### `pets`

Presumably gets the player's pets.

#### Request example

```
version=1&cmd=pets&selectID=12&playerID=12&sessionToken=d2d4a592700b0920658e5d56ed50ebfaa82b1f4a3e105e9bcfd8bcbb081c2e87
```

### `mega`

#### Request example

```
version=1&cmd=mega&count=25&pluscount=25&followercount=25&playerID=12&sessionToken=d2d4a592700b0920658e5d56ed50ebfaa82b1f4a3e105e9bcfd8bcbb081c2e87
```

### `missionsmega`

#### Request example

```
version=1&cmd=missionsmega&typeID=0&count=25&pluscount=25&followercount=25&playerID=12&sessionToken=d2d4a592700b0920658e5d56ed50ebfaa82b1f4a3e105e9bcfd8bcbb081c2e87
```

## DLC

There are some other php files at `http://cats.ngmoco.com/touchpet/gamedata/` that are mostly responsible for DLC and basic game messages. It seems like they can be ignored safely and returning a blank page is enough to get the game past this point.

> I have some idea of what get_dlc.php is doing: https://cohost.org/knot126/post/2159659-i-am-now-hosting-a-c/
