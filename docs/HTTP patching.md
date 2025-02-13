# Game Patches

Katten requires a patch to disable using HTTPS for Plus+ API requests, since using custom CAs on iOS can be messy.<sup>\[Note 1\]</sup>

More specifically, the string `https` needs to be changed to `http`, and the assocaited cfstring structure needs to be updated so that the length of the string is 4 (otherwise you will get "bad URL" errors).

If you don't want to do this manually, there is an automated script in the [tools folder](../tools) which can automatically patch most games given it's binary, even if it's not explicitly supported.

---

1. (or at least I couldn't get it to work)
