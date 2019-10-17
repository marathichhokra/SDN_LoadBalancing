#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    net = Mininet( topo=None,
                   link=TCLink,
                   build=False,
                   ipBase='10.0.0.0/8'
                   )

    info( '------------Adding controller------------\n' )
    c0=net.addController(name='c0',
                      controller=RemoteController,
                      ip='127.0.0.1',
                      protocol='tcp',
                      port=6633)

    info( '------------Adding switches------------\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch) #the switch at client side. Normal Regular one. XXX Todo: cls = ?
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch) #the openflow switch @right. Servers will be connected via this switch

    info( '------------Adding hosts(clients)------------\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None) #client 1
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None) #client 2
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None) #client 3
    info( '------------Adding Servers------------\n')
    h4 = net.addHost('h4', cls=Host, ip='10.0.0.89', defaultRoute=None) #server 1
    h5 = net.addHost('h5', cls=Host, ip='10.0.0.90', defaultRoute=None) #server 2

    info( '------------Adding links (clients)------------\n')
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s1)
    info( '------------Adding links between Switches------------\n')
    net.addLink(s1,s2)
    info( '------------Adding links (D.C.)------------\n')
    net.addLink(h4, s2)
    net.addLink(h5, s2)

    info( '------------Starting network------------\n')
    net.build()
    info( '------------Starting controllers------------\n')
    for controller in net.controllers:
        controller.start()

    info( '------------Starting switches------------\n')
    net.get('s2').start([c0])
    net.get('s1').start([c0])

    info( '------------Post configure switches and hosts------------\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

