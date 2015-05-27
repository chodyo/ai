#!/usr/bin/python -tt

from bzrc import BZRC, Command
import sys, math, time
from potentialField import PotentialField

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

# time to wait between ticks in milliseconds
sleepTime = 20
# number of bots to control
botCount = 1
# should the bots fire uncontrollably?
shootOnCooldown = True

class Agent(object):

    def __init__(self, bzrc):
        self.bzrc = bzrc
        self.constants = self.bzrc.get_constants()
        self.commands = []

        obstacles = bzrc.get_obstacles()
        worldsize = self.constants['worldsize']

        mytanks = bzrc.get_mytanks()
        self.mycolor = mytanks[0].callsign[:-1]
        bases = bzrc.get_bases()
        mybase = None
        for base in bases:
            if base.color == self.mycolor:
                mybase = base

        self.pf = PotentialField(obstacles, worldsize, mybase)

    def tick(self, time_diff):
        '''Some time has passed; decide what to do next'''
        # Get information from the BZRC server
        mytanks, othertanks, flags, shots = self.bzrc.get_lots_o_stuff()
        self.mytanks = mytanks
        self.othertanks = othertanks
        self.flags = flags
        self.shots = shots
        self.enemies = [tank for tank in othertanks if tank.color !=
                self.constants['team']]

        # Reset my set of commands (we don't want to run old commands)
        self.commands = []

        # Decide what to do with each of my tanks
        # for bot in mytanks:
        #     self.attack_enemies(bot)

        # Chase/capture the flag
        for bot in mytanks:
            if bot.index >= botCount:
                continue
            if bot.flag == "-":
                self.get_flag(bot)
            else:
                self.return_to_base(bot)

        # Send the commands to the server
        results = self.bzrc.do_commands(self.commands)

    def get_flag(self, bot):
        '''Find the closest flag and move to its location'''
        self.pf.get_flag = True

        closest_flag = None
        closest_dist = 2 * float(self.constants['worldsize'])
        for flag in self.flags:
            if flag.color == self.mycolor:
                continue
            dist = math.sqrt((flag.x - bot.x)**2 + (flag.y - bot.y)**2)
            if dist < closest_dist:
                closest_dist = dist
                closest_flag = flag
        if closest_flag is None:
            command = Command(bot.index, 0, 0, False)
            self.commands.append(command)
        else:
            goal = Misc()
            goal.x = closest_flag.x
            goal.y = closest_flag.y
            goal.r = 0

            self.pf.set_goal(goal)
            desired_x, desired_y = self.pf.get_vector(bot)
            self.move_from_vector(bot, desired_x, desired_y, closest_dist)

    def return_to_base(self, bot):
        '''Move to my base's location'''
        self.pf.get_flag = False

        goal = Misc()
        goal.x = self.pf.home_x
        goal.y = self.pf.home_y
        goal.r = 10

        dist = math.sqrt((goal.x-bot.x)**2+(goal.y-bot.y)**2)

        self.pf.set_goal(goal)
        desired_x, desired_y = self.pf.get_vector(bot)
        self.move_from_vector(bot, desired_x, desired_y, dist)

        pass

    def attack_enemies(self, bot):
        '''Find the closest enemy and chase it, shooting as you go'''
        best_enemy = None
        best_dist = 2 * float(self.constants['worldsize'])
        for enemy in self.enemies:
            if enemy.status != 'alive':
                continue
            dist = math.sqrt((enemy.x - bot.x)**2 + (enemy.y - bot.y)**2)
            if dist < best_dist:
                best_dist = dist
                best_enemy = enemy
        if best_enemy is None:
            command = Command(bot.index, 0, 0, False)
            self.commands.append(command)
        else:
            self.move_to_position(bot, best_enemy.x, best_enemy.y)

    def move_from_vector(self, bot, vx, vy, distance):
        target_angle = math.atan2(vy, vx)
        relative_angle = self.normalize_angle(target_angle - bot.angle)

        v = distance/20
        omega = 5*relative_angle / math.pi

        print bot.index, v, omega, bot.flag

        command = Command(bot.index, v, omega, shootOnCooldown)
        self.commands.append(command)

    def move_to_position(self, bot, target_x, target_y):
        target_angle = math.atan2(target_y - bot.y,
                target_x - bot.x)
        relative_angle = self.normalize_angle(target_angle - bot.angle)
        command = Command(bot.index, 1, 2 * relative_angle, True)
        self.commands.append(command)

    def normalize_angle(self, angle):
        '''Make any angle be between +/- pi.'''
        angle -= 2 * math.pi * int (angle / (2 * math.pi))
        if angle <= -math.pi:
            angle += 2 * math.pi
        elif angle > math.pi:
            angle -= 2 * math.pi
        return angle

class Misc(object):
    pass


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
            agent.tick(time_diff)
            time.sleep(sleepTime / 1000)
    except KeyboardInterrupt:
        print "Exiting due to keyboard interrupt."
        bzrc.close()


if __name__ == '__main__':
    main()

# vim: et sw=4 sts=4
