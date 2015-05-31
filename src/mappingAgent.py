#!/usr/bin/python -tt

from bzrc import BZRC, Command
from gridfilter import GridFilter
import sys, math, time
#from potentialFieldUpdate import PotentialField
from potentialFieldForDrawing import PotentialField
import drawgridfilter 
import numpy as np

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
sleepTime = 4000
# number of bots to control
botCount = 9
# should the bots fire uncontrollably?
shootOnCooldown = False

class Agent(object):

    def __init__(self, bzrc):
        self.bzrc = bzrc
        self.constants = self.bzrc.get_constants()
        self.commands = []
        self.gridFilter = GridFilter(self.constants['truepositive'],self.constants['truenegative']);
        self.pfArrx = []
        self.pfArry = []
        self.distArr = []
        obstacles = bzrc.get_obstacles()
        worldsize = self.constants['worldsize']

        self.mytanks = bzrc.get_mytanks()
        self.mycolor = self.mytanks[0].callsign[:-1]
        bases = bzrc.get_bases()
        mybase = None
        for base in bases:
            if base.color == self.mycolor:
                mybase = base
        self.myBase = mybase
        self.pf = PotentialField(obstacles, worldsize, mybase)

        #set the goal and potential field for each tank
        for bot in self.mytanks:
            if bot.index >= botCount:
                continue
            elif bot.index<botCount:
                self.map_area(bot)

    def tick(self, time_diff):
        '''Some time has passed; decide what to do next'''
        # Get information from the BZRC server
        mytanks, othertanks, flags, shots = self.bzrc.get_lots_o_stuff()
        self.mytanks = mytanks
        self.othertanks = othertanks
        self.flags = flags
        self.shots = 0
        self.enemies = [tank for tank in othertanks if tank.color !=
                self.constants['team']]

        # Reset my set of commands (we don't want to run old commands)
        self.commands = []

       #for each bot, call makeMap on the bot
        for bot in self.mytanks:
            if bot.index >= botCount:
                continue
            elif bot.index<botCount:
                self.makeMap(bot)


        self.update_map()
       
        drawgridfilter.draw_grid()

        # Send the commands to the server
        results = self.bzrc.do_commands(self.commands)

    def update_map(self):
        for bot in self.mytanks:
            if bot.index <=botCount:
                self.gridFilter.update_grid(self.bzrc.get_occgrid(1)[0],self.bzrc.get_occgrid(1)[1])
                drawgridfilter.update_grid(self.gridFilter.get_grid())
                

    def map_area(self, bot):
        #print bot.index
        pointx = bot.x
        pointy = bot.y
        
        bot.pf = PotentialField(self.bzrc.get_obstacles(), self.constants['worldsize'], self.myBase)
        if bot.index == 0:
            goal = Misc()
            goal.x = 267
            goal.y = 267
            goal.r = 0
        elif bot.index == 1:
            goal = Misc()
            goal.x = -267
            goal.y = -267
            goal.r = 0
        elif bot.index == 2:
            goal = Misc()
            goal.x = -267
            goal.y = 0
            goal.r = 0
        elif bot.index == 3:
            goal = Misc()
            goal.x = -267
            goal.y = 267
            goal.r = 0
        elif bot.index == 4:
            goal = Misc()
            goal.x = 0
            goal.y = -267
            goal.r = 0
        elif bot.index == 5:
            goal = Misc()
            goal.x = 0
            goal.y = 0
            goal.r = 0
        elif bot.index == 6:
            goal = Misc()
            goal.x = 0
            goal.y = 267
            goal.r = 0
        elif bot.index == 7:
            goal = Misc()
            goal.x = 267
            goal.y = -267
            goal.r = 0
        elif bot.index == 8:
            goal = Misc()
            goal.x = 267
            goal.y = 0
            goal.r = 0
        

        
        
        dist = math.sqrt((goal.x - bot.x)**2 + (goal.y - bot.y)**2)
        self.pf.set_goal(goal)

        
        # generate grid
        x=np.linspace(-400, 400, 80)
        myx = x
        y=np.linspace(400, -400, 80)
        myy = y
        x, y=np.meshgrid(x, y)

        # calculate vector field
        vx, vy = self.pf.get_vector(bot, myx, myy)
        print bot.index

        #set the arrays for x and y potential fields, as well as dist
        #TODO dist shouldn't be set in an array here, as it constantly changes

        self.pfArrx.append(vx)
        self.pfArry.append(vy)
        self.distArr.append(dist)
        
        
    def makeMap(self, bot):
        #get the potential field value at the position in the arrays doing the following math
            #add 400 to get the range to be 0->800
            #divide by 80 (number of position samples in the linespace)
            #multiply the modified x and y values to get the position in a single dimension array

        desired_x = (self.pfArrx[bot.index][int(((bot.x+400)/80)*((bot.y+400) / 80))])
        desired_y = (self.pfArry[bot.index][int(((bot.x+400)/80)*((bot.y+400) / 80))])

        #print "Bot:(",bot.x,",",bot.y,")   Desired:(",desired_x,",",desired_y,")    "
        self.move_from_vector(bot, desired_x, desired_y, self.distArr[bot.index])

            
    def move_from_vector(self, bot, vx, vy, distance):
        target_angle = math.atan2(vy, vx)
        relative_angle = self.normalize_angle(target_angle - bot.angle)

        v = distance/20
        omega = 5*relative_angle / math.pi

        #print bot.index, v, omega, bot.flag

        command = Command(bot.index, v, omega, False)
        self.commands.append(command)

    def move_to_position(self, bot, target_x, target_y):
       
        target_angle = math.atan2(target_y - bot.y,
                target_x - bot.x)
        relative_angle = self.normalize_angle(target_angle - bot.angle)
        
        command = Command(bot.index, 1, 2 * relative_angle, False)
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
    drawgridfilter.init_window(800, 800)
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
