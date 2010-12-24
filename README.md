gtfs2trekker
============

This is a simple utility to convert a GTFS to a comma seperated value file
suitable for importation into the trekker GPS. The data converted includes
stop names, their GPS position, and a list of route short names servicing
that stop (e.g. 7, 10, etc.)

Requirements
------------

 - Python GTFS Library (http://github.com/bmander/gtfs)

Usage
-----

You will first need to convert your GTFS file into a GTFS database file. Use
the compile_gtfs program installed with the GTFS library to do this:
  
    compile_gtfs gtfsfile.zip -o gtfsfile.db

Then, just run gtfs2trekker.py against the generated file and redirect output
to a file of your choosing.

    gtfs2trekker.py <gtfs db file> > output.csv

Known limitations
-----------------

 - No support for alternate forms of transit (rail, ferry, etc.)
