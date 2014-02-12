from twisted.application import internet, service
from twisted.names import server, dns, hosts, common
from twisted.internet import reactor, defer
from functools import partial

port = 53

def delay_deferred(dfr, delay):
    res = defer.Deferred()
    dfr.addErrback(res.errback)
    def got_result(*args):
        reactor.callLater(delay, partial(res.callback, *args))

    dfr.addCallback(got_result)
    return res

class DelayResolver(common.ResolverBase):

    def __init__(self, backing_resolver, delay=60):
        self.backing_resolver = backing_resolver
        self.delay = delay
        common.ResolverBase.__init__(self)

    def lookupAddress(self, name, timeout=None):
        return delay_deferred(self.backing_resolver.lookupAddress(name, timeout=timeout), self.delay)

    def lookupIPV6Address(self, name, timeout=None):
        return delay_deferred(self.backing_resolver.lookupIPV6Address(name, timeout=timeout), self.delay)

# Create a MultiService, and hook up a TCPServer and a UDPServer to it as
# children.
dnsService = service.MultiService()
hostsResolver = DelayResolver(hosts.Resolver('/etc/hosts'))
tcpFactory = server.DNSServerFactory([hostsResolver])
internet.TCPServer(port, tcpFactory).setServiceParent(dnsService)
udpFactory = dns.DNSDatagramProtocol(tcpFactory)
internet.UDPServer(port, udpFactory).setServiceParent(dnsService)

# Create an application as normal
application = service.Application("DNSExample")

# Connect our MultiService to the application, just like a normal service.
dnsService.setServiceParent(application)
