#!/usr/bin/python

import gtfs
import sys
import struct
import time
import sqlalchemy
from optparse import OptionParser
import logging

usage = "usage: %prog [options] <gtfs db>"
parser = OptionParser(usage)
parser.add_option("-v", action="store_true", dest="verbose", 
                  help='Verbose (turn on debugging messages)')
parser.add_option("-i", action="store_true", dest="id_as_code", 
                  help='Use stop id as stop code')
(options, args) = parser.parse_args()

if len(args) < 1:
    parser.error("incorrect number of arguments")
    exit(1)

logger = logging.getLogger(sys.argv[0])
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
logger.addHandler(ch)
if options.verbose:
    logger.setLevel(logging.DEBUG)

logger.debug("Loading schedule")
sched = gtfs.Schedule(args[0])

logger.debug("Creating route index")

routemap = {}
for route in sched.routes:
    routemap[route.route_id] = route.route_short_name

logger.debug("Creating stop index")
for trip in sched.trips:
    for stop_time in trip.stop_times:
        stop_id = stop_time.stop_id
        if not routemap.get(stop_id):
            routemap[stop_id] = set([])
        routemap[stop_id].add(routemap[trip.route_id])

logger.debug("Writing stops")
for stop in sched.stops:
    routes_for_stop = ''
    if routemap.get(stop.stop_id):
        routes_for_stop = ' '.join(routemap[stop.stop_id])
    routes_for_stop = routes_for_stop[0:100].replace(',','\,')

    stop_name = stop.stop_name
    if stop.stop_code:
        stop_name = (stop.stop_code + ': ' + stop.stop_name)
    elif options.id_as_code:
        stop_name = (stop.stop_id + ': ' + stop.stop_name)
    stop_name = stop_name[0:40].replace(',','\,')

    # FIXME: For type, we hardcode to bus station (0037), but trekker supports
    # rail (0036) and a general "transit" category which I guess we should
    # use for ferries or whatever else

    print "%s,%s,%s,0,0037,%s,,,,,,,,1," % (stop.stop_lon, stop.stop_lat, 
                                            stop_name, 
                                            routes_for_stop)
