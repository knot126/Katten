# Touch Pets Server

The **Touch Pet Server** is the server originally hosted at `cats.ngmoco.com` and takes care of all *Touch Pets: Cats* game specific server actions and storage. Most notably, it handles player and cat actions.

All interaction happens using a single route: `http://cats.ngmoco.com/touchpet/`. This route expects a `cmd` parameter which determines the actual command that will be executed.

Data is returned in an XML format, which is parsed in `SERemoteMgr::parseObjectsFromXMLData:forType:model:`. This function takes the data, passes it to a `NSXMLParser` and returns the object at the first index (probably the first tree) if it succeedes.

## Commands

### `player`

This presumably gets player info as well as sets the session secret.

### `setplayerproperty`

Sets a property value on a player.

See: `SELoginMgr::setupInitialPlayerModel:`
