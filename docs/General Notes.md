# General notes

## Linux

Always allow python to use port 80:

```sh
sudo setcap CAP_NET_BIND_SERVICE=+eip /usr/bin/python3.11
```
