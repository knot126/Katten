# ngCore Engine

**ngCore** was a game engine for social games. It was developed by Ngmoco, and was capable of using a few different social APIs under the Mobage brand.

## Game data

On Android, game scripts and data are downloaded remotely after the APK is installed and updated on the fly. This means that even if you have an APK, you don't actually have the game data, just the engine the game was built in.

On iOS, the game data is packaged with the IPA for App Store licencing reasons.

## Social support

ngCore supports two social platforms: the Mobage West platform and the Mobage Japan platform. Mobage West is based on the Plus+ backend and is used for most countries; Mobage Japan is based on Mobage Town and is available mainly from Japan.

To simplify development for all regions, an abstrction from the specific APIs is provided via `Social.Common`. It is compatible with both social platforms, but only provides features the two have in common.

### Feature comparision

| Feature | Mobage Japan | Mobage West | More info |
| ------- | ------------ | ----------- | --------- |
| API     | `Social.JP`  | `Social.US` | The name of the class providing social services in ngCore. |
| Auth | ✓            | ✓           |  |
| Guest Accounts |              | ✓           |  |
| Profiles and Social | ✓            | ✓           |  |
| App Data | ✓            | ✓           | Provides app data storage. |
| Leaderboard | ✓            | ✓           |  |
| User Blocking | ✓            | ✓           |  |
| Config | ✓            | ✓           |  |
| Profanity Checking | ✓            | ✓           | Checks for profanity in the platform's respective language. |
| Notifications | ✓            | ✓           | Send push notifications |
| TextData | ✓            |             | For implementing forum/BB system. |
| Diary | ✓            |             |  |
| Avatar API | ✓            |             |  |
| Messages | ✓            |             | Called "minimail" in Japanese platform |

## References

* https://www.pocketgamer.com/ngcore-game-tech/ngmoco-launches-javascript-based-ngcore-game-tech-framework-for-ios-and-android/
* https://www.pocketgamer.biz/news/26032/ngmoco-launches-javascript-based-ngcore-game-tech-framework-for-ios-and-android/
* https://www.slideshare.net/mootoh/ngcore-8553686
* https://www.businesswire.com/news/home/20110602006382/en/ngmoco-Opens-Sandbox-Developer-Environment-to-Build-and-Ready-Games-for-Mobage-Launch
* https://docs.mobage.com/public/ngcore/index.html (Archived: https://drive.google.com/file/d/1dkXqK2DFy1qoXNtrBNbN_FzMOiZf2Y4T/view)
* https://www.android-group.jp/abc2011w/conference/android/docs/dena/ngcore_engine_for_mobage_platform.pdf
* https://xdaforums.com/t/q-request-app-we-rule.1206230/
