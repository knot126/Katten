# PlusPlus SDK (iOS) notes

## `NGPlatformAPIOperationResult`

Really lightweight class which holds info about a API request result. 

## `NGPlatformAPIOperation`

Mostly the same as `PlusRequest` in ngCore except Objective-C-ified.

Notable methods:

### `NGPlatformAPIOperation::synchronouslyPerformAction:method:data:`

Does the meat of the response handling afaict. Creates the `NGPlatformAPIOperationResult` object containing response data.

Parses the response body (plist or json) for "error" key, an integer error code.
