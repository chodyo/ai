#!/usr/bin/python -tt

# Control BZFlag tanks remotely with synchronous communication.

####################################################################
# NOTE TO STUDENTS:
# You CAN and probably SHOULD modify this code.  Just because it is
# in a separate file does not mean that you can ignore it or that
# you have to leave it alone.  Treat it as your code.  You are
# required to understand it enough to be able to modify it if you
# find something wrong.  This is merely a help to get you started
# on interacting with BZRC.  It is provided AS IS, with NO WARRANTY,
# express or implied.
####################################################################

from __future__ import division
import math, sys, socket, time, numpy

class BZRC:
    '''Class which handles queries and responses with remote control bots.'''

    def __init__(self, host, port, debug=False):
        '''Given a hostname and port number, connect to the RC tanks.'''

        self.debug = debug

        # Note that AF_INET and SOCK_STREAM are defaults.
        sock = socket.socket()
        sock.connect((host, port))
        # Make a line-buffered "file" from the socket.
        self.conn = sock.makefile(bufsize=1)

        self.handshake()

    def close(self):
        '''Close the socket.'''
        self.conn.close()

    def read_arr(self):
        '''Read a response from the RC tanks as an array split on
        whitespace.'''

        try:
            line = self.conn.readline()
        except socket.error:
            print 'Server Shut down. Aborting'
            sys.exit(1)
        if self.debug:
            print 'Received: %s' % line.split()
        return line.split()

    def sendline(self, line):
        '''Send a line to the RC tanks.'''
        #print 'sending',line
        print >>self.conn, line

    def die_confused(self, expected, got_arr):
        '''When we think the RC bots should have responded differently, call
        this method with a string explaining what should have been sent and
        with the array containing what was actually sent.'''

        raise UnexpectedResponse(expected, ' '.join(got_arr))

    def expect(self, expected, full=False):
        if type(expected) == str:
            expected = (expected,)
        line = self.read_arr()
        good = True
        if full and len(expected) != len(line):
            good = False
        else:
            for a,b in zip(expected,line):
                if a!=b:
                    good = False
                    break
        if not good:
            self.die_confused(' '.join(expected), line)
        if full:
            return True
        return line[len(expected):]
    
    def expect_multi(self, *expecteds, **kwds):
        '''Verify the server's response looks like one of
        several possible responses. Return the index of the matched response,
        and the server's line response'''

        line = self.read_arr()
        for i,expected in enumerate(expecteds):
            for a,b in zip(expected, line):
                if a!=b:
                    break
            else:
                if not kwds.get('full',False) or len(expected) == len(line):
                    break
        else:
            self.die_confused(' or '.join(' '.join(one) for one in expecteds),
                    line)
        return i, line[len(expected):]

    def handshake(self):
        '''Perform the handshake with the remote bots.'''

        self.expect(('bzrobots', '1'), True)
        print >>self.conn, 'agent 1'

    def read_ack(self):
        '''Expect an "ack" line from the remote tanks.

        Raise an UnexpectedResponse exception if we get something else.'''

        self.expect('ack')

    def read_bool(self):
        '''Expect a boolean response from the remote tanks.

        Return True or False in accordance with the response.  Raise an
        UnexpectedResponse exception if we get something else.'''

        i, rest = self.expect_multi(('ok',),('fail',))
        return (True, False)[i]

    def read_teams(self):
        self.expect('begin')

        teams = []
        while True:
            i, rest = self.expect_multi(('team',),('end',))
            if i == 1:
                break
            team = Answer()
            team.color = rest[0]
            team.count = float(rest[1])
            team.base = [(float(x), float(y)) for (x, y) in
                    zip(rest[2:10:2], rest[3:10:2])]
            teams.append(team)
        return teams

    def read_obstacles(self):
        self.expect('begin')

        obstacles = []
        while True:
            i, rest = self.expect_multi(('obstacle',),('end',))
            if i == 1:
                break
            obstacle = [(float(x), float(y)) for (x, y) in
                    zip(rest[::2], rest[1::2])]
            obstacles.append(obstacle)
        return obstacles
    
    def read_occgrid(self):
        response = self.read_arr()
        if 'fail' in response:
            return None
        pos = tuple(int(a) for a in self.expect('at')[0].split(','))
        size = tuple(int(a) for a in self.expect('size')[0].split('x'))
        grid = numpy.zeros(size)
        for x in range(size[0]):
            line = self.read_arr()[0]
            for y in range(size[1]):
                if line[y] == '1':
                    grid[x, y] = 1
        self.expect('end', True)
        return pos, grid

    def read_flags(self):
        line = self.read_arr()
        if line[0] != 'begin':
            self.die_confused('begin', line)

        flags = []
        while True:
            line = self.read_arr()
            if line[0] == 'flag':
                flag = Answer()
                flag.color = line[1]
                flag.poss_color = line[2]
                flag.x = float(line[3])
                flag.y = float(line[4])
                flags.append(flag)
            elif line[0] == 'end':
                break
            else:
                self.die_confused('flag or end', line)
        return flags

    def read_shots(self):
        line = self.read_arr()
        if line[0] != 'begin':
            self.die_confused('begin', line)

        shots = []
        while True:
            line = self.read_arr()
            if line[0] == 'shot':
                shot = Answer()
                shot.x = float(line[1])
                shot.y = float(line[2])
                shot.vx = float(line[3])
                shot.vy = float(line[4])
                shots.append(shot)
            elif line[0] == 'end':
                break
            else:
                self.die_confused('shot or end', line)
        return shots

    def read_mytanks(self):
        line = self.read_arr()
        if line[0] != 'begin':
            self.die_confused('begin', line)

        tanks = []
        while True:
            line = self.read_arr()
            if line[0] == 'mytank':
                tank = Answer()
                tank.index = int(line[1])
                tank.callsign = line[2]
                tank.status = line[3]
                tank.shots_avail = int(line[4])
                tank.time_to_reload = float(line[5])
                tank.flag = line[6]
                tank.x = float(line[7])
                tank.y = float(line[8])
                tank.angle = float(line[9])
                tank.vx = float(line[10])
                tank.vy = float(line[11])
                tank.angvel = float(line[12])
                tanks.append(tank)
            elif line[0] == 'end':
                break
            else:
                self.die_confused('mytank or end', line)
        return tanks

    def read_othertanks(self):
        line = self.read_arr()
        if line[0] != 'begin':
            self.die_confused('begin', line)

        tanks = []
        while True:
            line = self.read_arr()
            if line[0] == 'othertank':
                tank = Answer()
                tank.callsign = line[1]
                tank.color = line[2]
                tank.status = line[3]
                tank.flag = line[4]
                tank.x = float(line[5])
                tank.y = float(line[6])
                tank.angle = float(line[7])
                tanks.append(tank)
            elif line[0] == 'end':
                break
            else:
                self.die_confused('othertank or end', line)
        return tanks

    def read_bases(self):
        bases = []
        line = self.read_arr()
        if line[0] != 'begin':
            self.die_confused('begin', line)
        while True:
            line = self.read_arr()
            if line[0] == 'base':
                base = Answer()
                base.color = line[1]
                base.corner1_x = float(line[2])
                base.corner1_y = float(line[3])
                base.corner2_x = float(line[4])
                base.corner2_y = float(line[5])
                base.corner3_x = float(line[6])
                base.corner3_y = float(line[7])
                base.corner4_x = float(line[8])
                base.corner4_y = float(line[9])
                bases.append(base)
            elif line[0] == 'end':
                break
            else:
                self.die_confused('othertank or end', line)
        return bases

    def read_constants(self):
        line = self.read_arr()
        if line[0] != 'begin':
            self.die_confused('begin', line)

        constants = {}
        while True:
            line = self.read_arr()
            if line[0] == 'constant':
                constants[line[1]] = line[2]
            elif line[0] == 'end':
                break
            else:
                self.die_confused('constant or end', line)
        return constants

    # Commands:

    def shoot(self, index):
        '''Perform a shoot request.'''

        self.sendline('shoot %s' % index)
        self.read_ack()
        return self.read_bool()

    def speed(self, index, value):
        '''Set the desired speed to the specified value.'''

        self.sendline('speed %s %s' % (index, value))
        self.read_ack()
        return self.read_bool()

    def angvel(self, index, value):
        '''Set the desired angular velocity to the specified value.'''

        self.sendline('angvel %s %s' % (index, value))
        self.read_ack()
        return self.read_bool()

    def accelx(self, index, value):
        '''Set the desired x acceleration to the specified value.'''

        self.sendline('accelx %s %s' % (index, value))
        self.read_ack()
        return self.read_bool()

    def accely(self, index, value):
        '''Set the desired x acceleration to the specified value.'''

        self.sendline('accely %s %s' % (index, value))
        self.read_ack()
        return self.read_bool()

    # Information Requests:

    def get_teams(self):
        '''Request a list of teams.'''

        self.sendline('teams')
        self.read_ack()
        return self.read_teams()

    def get_obstacles(self):
        '''Request a list of obstacles.'''

        self.sendline('obstacles')
        self.read_ack()
        return self.read_obstacles()
    
    def get_occgrid(self, tankid):
        '''Request an occupancy grid for a tank'''

        self.sendline('occgrid %d' % tankid)
        self.read_ack()
        return self.read_occgrid()

    def get_flags(self):
        '''Request a list of flags.'''

        self.sendline('flags')
        self.read_ack()
        return self.read_flags()

    def get_shots(self):
        '''Request a list of shots.'''

        self.sendline('shots')
        self.read_ack()
        return self.read_shots()

    def get_mytanks(self):
        '''Request a list of our robots.'''

        self.sendline('mytanks')
        self.read_ack()
        return self.read_mytanks()

    def get_othertanks(self):
        '''Request a list of tanks that aren't our bots.'''

        self.sendline('othertanks')
        self.read_ack()
        return self.read_othertanks()

    def get_bases(self):
        '''Request a list of bases.'''

        self.sendline('bases')
        self.read_ack()
        return self.read_bases()

    def get_constants(self):
        '''Request a dictionary of game constants.'''

        self.sendline('constants')
        self.read_ack()
        return self.read_constants()

    # Optimized queries

    def get_lots_o_stuff(self):
        '''Network-optimized request for mytanks, othertanks, flags, and shots.

        Returns a tuple with the four results.'''

        self.sendline('mytanks')
        self.sendline('othertanks')
        self.sendline('flags')
        self.sendline('shots')

        self.read_ack()
        mytanks = self.read_mytanks()
        self.read_ack()
        othertanks = self.read_othertanks()
        self.read_ack()
        flags = self.read_flags()
        self.read_ack()
        shots = self.read_shots()

        return (mytanks, othertanks, flags, shots)

    def do_commands(self, commands):
        '''Send commands for a bunch of tanks in a network-optimized way.'''

        for cmd in commands:
            if isinstance(cmd, GoodrichCommand):
                self.sendline('accelx %d %s' % (cmd.index, cmd.accelx))
                self.sendline('accely %d %s' % (cmd.index, cmd.accely))
            else:
                self.sendline('speed %s %s' % (cmd.index, cmd.speed))
                self.sendline('angvel %s %s' % (cmd.index, cmd.angvel))
                if cmd.shoot:
                    self.sendline('shoot %s' % cmd.index)

        results = []
        for cmd in commands:
            if isinstance(cmd, GoodrichCommand):
                self.read_ack()
                accelx = self.read_bool()
                self.read_ack()
                accely = self.read_bool()
                results.append((accelx, accely))
            else:
                self.read_ack()
                result_speed = self.read_bool()
                self.read_ack()
                result_angvel = self.read_bool()
                if cmd.shoot:
                    self.read_ack()
                    result_shoot = self.read_bool()
                else:
                    result_shoot = False
                results.append( (result_speed, result_angvel, result_shoot) )
        return results

class Answer(object):
    '''BZRC returns an Answer for things like tanks, obstacles, etc.

    You should probably write your own code for this sort of stuff.  We
    created this class just to keep things short and sweet.'''

    pass


class Command(object):
    '''Class for setting a command for a bot.'''

    def __init__(self, index, speed, angvel, shoot):
        self.index = index
        self.speed = speed
        self.angvel = angvel
        self.shoot = shoot

class GoodrichCommand(object):
    def __init__(self, index, accelx, accely):
        self.index = index
        self.accelx = accelx
        self.accely = accely

class UnexpectedResponse(Exception):
    '''Exception raised when the BZRC gets confused by a bad response.'''

    def __init__(self, expected, got):
        self.expected = expected
        self.got = got

    def __str__(self):
        return 'BZRC: Expected "%s".  Instead got "%s".' % (self.expected,
                self.got)


# vim: et sw=4 sts=4
