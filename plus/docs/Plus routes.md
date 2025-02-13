# Plus+ routes

General info, according to the android version JS found from We Rule:

* request POST bodies are form encoded (usually)
* responses are json (ios may accept plists but handles json too)
* `success` + `error` + `error_msg` fields are used for error messages
* response codes are always 200 or 304
