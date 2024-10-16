# Touch Pets Server

The **Touch Pet Server** is the server originally hosted at `cats.ngmoco.com` and takes care of all *Touch Pets: Cats* game specific server actions and storage. Most notably, it handles player and cat actions.

Most interaction happens using a single route: `http://cats.ngmoco.com/touchpet/`. This route expects a `cmd` parameter which determines the actual command that will be executed. Data is returned in an XML format, which is parsed in `SERemoteMgr`, which is an `NSXMLParserDelegate` that processes responses as you would expect it to.

## Commands

many command names are of a standard format:

- `{classname}` - query a single object
- `{classname}s` - query multipule objects
- `set{classname}property` - set a property on an object of type [classname]

they accept some standard arguments:

- `{classname}ID={int}` - id of object to manipulate
- `playerID={int}` - id of the player preforming this action
- `categoryID={int}` - the property's category
- `propertyID={int}` - the property's id
- `propertyvalue={int}` - value to set property to
- `ifgreaterthan={int}`

boring ones:

- `version=1` - (probably) api version, always 1
- `sessionToken={sessiontoken}` - the session token

### Notes

- `selectID`: used for selcting things by player ID (and maybe other id's?)

#### SERemotePropertyChange

## DLC

There are some other php files at `http://cats.ngmoco.com/touchpet/gamedata/` that are mostly responsible for DLC and basic game messages. It seems like they can be ignored safely and returning a blank page is enough to get the game past this point.

> I have some idea of what get_dlc.php is doing: https://cohost.org/knot126/post/2159659-i-am-now-hosting-a-c/

## XML responses

Any plural of a class name (`className + "s"`) or the string `"results"` are ignored.

```xml
<mega count="(int)" totalcount="(int)" pluscount="(int)" followercount="(int)" totalpluscount="(int)" totalfollowercount="(int)"/>
```

```xml
<pets> <!-- or any acceptable plural of the class of objects, or "results" -->
	<pet> <!-- or any object -->
		<property id="(int)" category="(int)">(int)</property>
		<relationship ...>...</relationship>
		<playdate ...>...</playdate>
		<inventory inventoryID="(int)" known="(bool)" rewarded="(bool)" owned="(bool)" gifted="(bool)" timeacquired="(int)" quantity="(int)" decaystate="(int)" fromdogID="[int]" todogID="[int]" timegifted="[int]" isnew="[bool]">...</inventory>
		<loot ...>...</loot>
	</pet>
</pets>
```

```xml
<servertime>(int)</servertime>
```

```xml
<dataversion>(int)</dataversion> <!-- see: gDatabaseVersion -->
```

## Startup

`-[SELoginMgr backgroundFetch]` does the initial `setplayerproperty` for cat=10 prop=0. if there is a player object in the response then its values are used, otherwise they are initialised to defaults

`-[SELoginMgr backgroundFetch]` sends message `[SEPetModel fetchItemsForPlayerID: [[SEPlayerModel myPlayer] playerID] cache: NO]`, if no list of pets is returned then it is a login error
