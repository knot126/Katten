# Patches need for `PetCat` to run the server

Change the string `https` (exactly that string) to `http` so `ngpipes.ngmoco.com` service doesn't try using https. (Also make sure to update the length becuase Objective C stores the length somewhere in the binary too.)
