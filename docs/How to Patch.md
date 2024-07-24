# How to patch

## Set up iphone

1. Jailbreak the iphone. Good luck!
2. Install iFile and the terminal app.
3. Install AppSync Unified to bypass signature requirements.
4. Download ldid on your PC. (You could get it on the phone but it's better to have on PC.)
5. Use `ldid` to extract entitlements from a normal TPC binary. (`ldid -e <bin>`)
6. Put those entitlements in a UTF-8 encoded text plist file. (Remove the duplicate of the plist code!!!)

## Do a patch

1. Patch the binary however you want to.
2. Use `ldid` to regenerate hashes with TPC default entitlements. (`ldid -S"ent.plist" PetCat`)
3. Navigate to the app folder in iFile's http file browser.
4. In the terminal also go to that folder and delete `PetCat` file.
5. Upload the `PetCat` binary to the folder using http file browser.
6. In terminal run `su; chmod 777 PetCat` (or `chmod +x PetCat` may also work)
7. It should run!!!

> Note: `su` password is usually `alpine`
