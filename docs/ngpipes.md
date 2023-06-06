# ngpipes.ngmoco.com

This is the main social API used for Touch Pets: Cats.

This API might also be the same one used in PlusPlus as they are both by ngmoco, though I don't know if it is.

## General info

`POST` requests are submitted to the given endpoint using standard URL encoding for the body and it either responds with a JSON (`application/json`) or apple binary plist (`application/binary-plist`) body.

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

### `POST` `{service}/users`

Creates a new user account. Expects the following parameters when creating a lite account:


