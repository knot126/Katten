Edit: It seems like this doesn't matter, see patch.md :P

# Defeating antitamper

Symbols that seem to mention pirate checking and cracks:

* `NGPlatform::performPirateCheck`
* `NGPlatform::_pirateHax`
* `MCEnvironment::isPirated` (function and label)
* `MCEnvironment::setPirated:`
* `SEGame::isPirated`
* `SEInitialInfoView::showPirateError`
* `SEPlayerStats::recordPiratedCurrentSKU`
* `SESKUInfo::shouldShowPirateError`
* `Heartbeat::isCracked` (just returns `false`)
* `Mobclix::isApplicationCracked`

There are also some checks for jailbreaking:

* `MCEnvironment::isJailbroken`

## Resources

* https://www.zdziarski.com/blog/?p=2172
* https://www.theiphonewiki.com/wiki/Main_Page
* https://www.reddit.com/r/LegacyJailbreak/
