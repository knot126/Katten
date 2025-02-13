# Notes from Cohost

This contains misc. notes from my account on Cohost where I sometimes talk about the game.

## response element names for TPC server stuff (part 0)

> More up to date: https://cohost.org/knot126/post/2528864-response-element-nam/776481bc38274dd9a2b333774e032d82

The game parses the XML response from the server by using `SERemoteMgr`, which is both responsible for network operations and for being an `NSXMLParserDelegate`, which is basically an event driven XML parser.

As part of parsing the data, the game keeps a current working object `this->currentObject` and a running string (when XML text e.g. `<abc>text</abc>` is found) `this->runningString`.

* elements matching with `[delegate acceptablePluralClasses]`
  * (i think) this basically means `cats`, `players`, `results` etc
  * ignored
  * ex: `<cats><!-- cats here --></cats>`
* `dataversion`
  * integer version number
  * `<dataversion>124</dataversion>`
  * the game will panic if this is lower than the current version
  * maybe you can get away with not specifying this since the game only checks if the element exists
* `mega`
  * counts for friend and followers and their requests in both TouchPets and Plus+
  * sets them
  * not much else
* `result`
  * allocates an object of the class that corresponds to the expected class as the current object
  * takes the current running string
* `property`
  * `<property category="0" id="0">0</property>`
* `inventory`
  * Expects the current object to be a player object
  * Attributes:
    * `inventoryID`: int
    * `known`: bool
    * `rewarded`: bool
    * `owned`: bool
    * `gifted`: bool
    * `timeacquired`: int
    * `quantity`: int
    * `decaystate`: int
    * `fromdogID`: int | null
    * `todogID`: int | null
    * `timegifted`: int | null
    * `isnew`: bool | null
