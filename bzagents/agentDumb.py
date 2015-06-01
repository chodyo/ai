#!/usr/bin/python -tt

# An incredibly simple agent.  All we do is find the closest enemy tank, drive
# towards it, and shoot.  Note that if friendly fire is allowed, you will very
# often kill your own tanks with this code.

#################################################################
# NOTE TO STUDENTS
# This is a starting point for you.  You will need to greatly
# modify this code if you want to do anything useful.  But this
# should help you to know how to interact with BZRC in order to
# get the information you need.
#
# After starting the bzrflag server, this is one way to start
# this code:
# python agent0.py [hostname] [port]
#
# Often this translates to something like the following (with the
# port name being printed out by the bzrflag server):
# python agent0.py localhost 49857
#################################################################

import sys
import math
import time

from bzrc import BZRC, Command

class Agent(object):
    """Class handles all command and control logic for a teams tanks."""

    def __init__(self, bzrc):
        self.bzrc = bzrc
        self.constants = self.bzrc.get_constants()
        self.commands = []
        self.flipped = True;
    
    def dumbTick(self, time_diff):
        mytanks, othertanks, flags, shots = self.bzrc.get_lots_o_stuff()
        self.mytanks = mytanks
        flipped = self.flipped
        if time_diff % 3 < 1 and flipped==True:
            if time_diff % 9 < 1:
                self.turnBlind(mytanks[1])
                self.flipped = False
            else:
                self.goStraight(mytanks[1])
        elif ((time_diff % 9) > 1):
            self.flipped = True;
                  
        if(time_diff % 2 < 1):
            for tank in mytanks:
                self.justShoot(mytanks[1])
                
        
        results = self.bzrc.do_commands(self.commands)

    def turnBlind(self, tank):
        print tank.callsign
        self.bzrc.speed(tank.index, .2)
        self.bzrc.angvel(tank.index, .44)  
            
    def justShoot(self, tank):
        self.bzrc.shoot(tank.index)
       
    def goStraight(self, tank):
        self.bzrc.speed(tank.index, 1)
        self.bzrc.angvel(tank.index, 0)    



def main():
    # Process CLI arguments.
    try:
        execname, host, port = sys.argv
    except ValueError:
        execname = sys.argv[0]
        print >>sys.stderr, '%s: incorrect number of arguments' % execname
        print >>sys.stderr, 'usage: %s hostname port' % sys.argv[0]
        sys.exit(-1)

    # Connect.
    #bzrc = BZRC(host, int(port), debug=True)
    bzrc = BZRC(host, int(port))

    agent = Agent(bzrc)

    prev_time = time.time()

    # Run the agent
    try:
        while True:
            time_diff = time.time() - prev_time
            agent.dumbTick(time_diff)
            time.sleep(.1)
    except KeyboardInterrupt:
        print "Exiting due to keyboard interrupt."
        bzrc.close()


if __name__ == '__main__':
    main()

# vim: et sw=4 sts=4
