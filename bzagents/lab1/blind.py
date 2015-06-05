#!/usr/bin/env python
import sys
if not len(sys.argv)>1:
    print 'usage: blind.py [agent_name]'
    sys.exit()
name = sys.argv[1].split('.')[0]
sys.argv.pop(0)
__import__(name).main()

# vim: et sw=4 sts=4
