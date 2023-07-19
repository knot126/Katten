# ngCore Engine

**ngCore** was a game engine for social games. It was developed by Ngmoco, and was capable of using a few different social APIs under the Mobage brand.

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

1. https://www.pocketgamer.com/ngcore-game-tech/ngmoco-launches-javascript-based-ngcore-game-tech-framework-for-ios-and-android/
2. https://www.slideshare.net/mootoh/ngcore-8553686
3. https://docs.mobage.com/public/ngcore/index.html (Archived: https://drive.google.com/file/d/1dkXqK2DFy1qoXNtrBNbN_FzMOiZf2Y4T/view)
4. https://www.android-group.jp/abc2011w/conference/android/docs/dena/ngcore_engine_for_mobage_platform.pdf
