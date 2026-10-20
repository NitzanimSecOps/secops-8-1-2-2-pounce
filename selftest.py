"""Local tester for solution.py — not the hidden grader.

    python3 selftest.py              # a tiny fake network: no internet and no sudo needed
    sudo python3 selftest.py google.com   # the real thing (raw packets need sudo)

Edit ROUTE / DESTINATION to try other networks, or make a router silent with SILENT = {1}.
"""
import sys

ROUTE = ["192.168.1.1", "10.20.0.1", "172.16.5.9"]
DESTINATION = "198.51.100.7"
SILENT = set()  # indexes of routers that never answer, e.g. {1}


def fake_network():
    """Replace Scapy's sr1/sr with a simulated network before solution.py is imported."""
    import scapy.all as scapy_all
    from scapy.all import ICMP, IP

    def respond(probe):
        ttl = probe[IP].ttl
        if probe[IP].dst != DESTINATION:
            return None
        if ttl <= len(ROUTE):  # the TTL runs out at this router
            if ttl - 1 in SILENT:
                return None
            return IP(src=ROUTE[ttl - 1], dst="192.168.1.50") / ICMP(type=11, code=0)
        return IP(src=DESTINATION, dst="192.168.1.50") / ICMP(type=0, code=0)

    def sr1(packets, *args, **kwargs):
        for probe in packets:
            reply = respond(probe)
            if reply is not None:
                return reply
        return None

    scapy_all.sr1 = sr1


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else DESTINATION
    if len(sys.argv) == 1:
        fake_network()
    from solution import traceroute

    hops = traceroute(target)
    print(f"traceroute({target!r}) returned:")
    for number, hop in enumerate(hops, 1):
        print(f"  {number:>2}  {hop}")


if __name__ == "__main__":
    main()
