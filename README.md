dnsputter
=========

dnsputter is a DNS server that hangs for 60 seconds before returning responses. It's useful for testing applications that take user-supplied URLs as input to make sure they're not vulnerable to DOS attack.

Dependencies
----

* python
* Twisted

Usage
---
1. Point some domain name to your IP address
2. Run `sudo ./runserver.sh` to start the DNS server
3. Try to resolve a random subdomain of that domain name
