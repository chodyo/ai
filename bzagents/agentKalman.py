#!/usr/bin/python -tt

from bzrc import BZRC, Command
from kalmanFilter import kalmanFilter
import sys, math, time

# A kalman agent

class Agent(object):

    def __init__(self, bzrc):
        self.bzrc = bzrc
        self.constants = self.bzrc.get_constants()
        self.commands = []
        self.futureTime = 0.0
        self.kalman = kalmanFilter()
        self.dist_match = False
        self.timer = 2.0

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

        # should only be two tanks on the battlefield
        assert len(self.mytanks) == 1
        assert len(self.enemies) == 1


        # Reset my set of commands (we don't want to run old commands)
        self.commands = []
        '''print "Current:",time_diff'''
        self.kalman.calc_kalman(self.enemies[0])

        # Decide what to do with my tank
        self.attack_enemies(self.mytanks[0])

        # Send the commands to the server
        results = self.bzrc.do_commands(self.commands)

    # use the KALMAN FILTER to target & attack enemies
    def attack_enemies(self, bot):
        fire = False
        enemy = self.enemies[0]
        '''Calculate update here'''
        

        if self.dist_match != True:
            future_enemy = self.kalman.more_kalman(.01)
            enemy.x = float(future_enemy[0])
            enemy.y = float(future_enemy[3])
            rotate = self.kalman.rotate(bot, enemy)
            self.dist_match = self.kalman.fire(bot, enemy)
        else:
            future_enemy = self.kalman.more_kalman(self.timer)
            self.timer = 0.0
            enemy.x = float(future_enemy[0])
            enemy.y = float(future_enemy[3])
            rotate = self.kalman.rotate(bot, enemy)
            fire = self.kalman.lead_and_wait(bot, enemy)

        command = Command(0, 0, rotate, fire)
        self.commands.append(command)
        self.futureTime+=.02


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


def main():
    # Process CLI arguments.
    try:
        execname, host, port = sys.argv
    except ValueError:
        execname = sys.argv[0]
        print >>sys.stderr, '%s: incorrect number of arguments' % execname
        print >>sys.stderr, 'usage: %s hostname port' % sys.argv[0]
        sys.exit(-1)

    bzrc = BZRC(host, int(port))
    agent = Agent(bzrc)
    prev_time = time.time()
    time_diff = 0
    # Run the agent
    try:
        #time.sleep(3)
        while True:
            #time_diff = time.time() - prev_time
            
            agent.tick(time_diff)
            time.sleep(.05)
            time_diff += .05
    except KeyboardInterrupt:
        print "Exiting due to keyboard interrupt."
        bzrc.close()


if __name__ == '__main__':
    main()

# vim: et sw=4 sts=4

