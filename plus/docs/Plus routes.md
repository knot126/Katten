# Plus+ routes

General info, according to the android version JS found from We Rule:

* request POST bodies are form encoded (usually)
* responses are json (ios may accept plists but handles json too)
* `error_msg` field is used for error message strings, existence used to indicate errors
* response codes are always 200 or 304
