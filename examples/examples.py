"""
TimeSlice module contains 2 classes:
    TimeSlice.TimeSlice: represents a range of time.
    TimeSlice.TimeSet: represents a list of TimeSlices without intersection (Intersections are removed when a TimeSlice is added to a TimeSet.
"""

import datetime
import TimeSlice

#=========================================================================================================
#Slices creation
#=========================================================================================================

slice1 = TimeSlice.TimeSlice( start = datetime.datetime( 2009, 1, 1, 0, 0, 0 ), end = datetime.datetime( 2009, 1, 2, 0, 0, 0 ) )
slice2 = TimeSlice.TimeSlice( start = datetime.datetime( 2009, 1, 1, 22, 33, 44 ), end = datetime.datetime( 2009, 1, 2, 22, 33, 44 ) )


#=========================================================================================================
#Operations with TimeSlices
#=========================================================================================================

#Duration: returns duration (in seconds) of a TimeSlice
#
print slice1.duration()
#Out: 86400

# --------------------------

#Sum: Returns a TimeSet with a TimeSlice with total time
#
print slice1 + slice2
#Out: [<TimeSlice intance (datetime.datetime(2009, 1, 1, 0, 0), datetime.datetime(2009, 1, 2, 22, 33, 44)) >]

# --------------------------

#Subtract: Returns a TimeSet with 1 or more TimeSlices, removing intersections. Important: slice2 - slice1 != slice1 - slice2
#
print slice1 - slice2
#Out: [<TimeSlice intance (datetime.datetime(2009, 1, 1, 0, 0), datetime.datetime(2009, 1, 2, 22, 33, 44)) >]

print slice2 - slice1
#Out: [<TimeSlice intance (datetime.datetime(2009, 1, 2, 0, 0), datetime.datetime(2009, 1, 2, 22, 33, 44)) >]

# --------------------------

#Intersect: Returns a TimeSlice containing intersection between slices
#
print slice1.intersect( slice2 )
#Out: <TimeSlice intance (datetime.datetime(2009, 1, 1, 22, 33, 44), datetime.datetime(2009, 1, 2, 0, 0)) >

# --------------------------

#Contains: returns True if a date, datetime or timeslice is "inside" the slice range, False instead:
#
print datetime.datetime( 2009, 1, 1, 12, 13, 14 ) in slice1
#Out: True

print slice2 in slice1
#Out: False

print TimeSlice.TimeSlice( start = datetime.datetime( 2009, 1, 1, 9, 0, 0 ), end = datetime.datetime( 2009, 1, 1, 15, 0, 0 ) ) in slice1
#Out: True

# --------------------------





#=========================================================================================================
# TimeSet creation
#=========================================================================================================

#Empty TimeSet
set1 = TimeSlice.TimeSet()

#TimeSet with a list of slices:
set2 = TimeSlice.TimeSet( [ slice1, slice2 ] )

#Creating TimeSet containing all days of a month
set3 = TimeSlice.TimeSet.fromRange( start = datetime.date( 2009, 1, 1 ), end = datetime.date( 2009, 2, 1 ), repeat = TimeSlice.DAYLY )


#=========================================================================================================
#Operations with TimeSets
#=========================================================================================================

#Duration: returns sum of duration (in seconds) of all slices in a timeset
#
print set3.duration()
#Out: 2592000

# --------------------------

#Append: adds slices into a timeset (removing intersections)
#
print set1.append( slice1 )

# --------------------------

#Iteration: interates over all TimeSlices in a TimeSet
#
for x in set2:
    print x
#Out: <TimeSlice intance (datetime.datetime(2009, 1, 1, 0, 0), datetime.datetime(2009, 1, 2, 0, 0)) >
#     <TimeSlice intance (datetime.datetime(2009, 1, 2, 0, 0), datetime.datetime(2009, 1, 2, 22, 33, 44)) >

# --------------------------

#Sum: Returns a TimeSet, summing TimeSlices from both sets
#
set3 + set2

#Subtract: Returns a TimeSet removing from the first TimeSet all intersection with TimeSlices of second TimeSet
#
set3 - set1

#Intersect: Returns a TimeSet with TimeSlices containing intersections
#           it could be done between 2 TimeSets or betweeen a slice and a set
set3.intersect( slice2 )
set3.intersect( set2 )
slice2.intersect( set3 )

# --------------------------

#Contains: returns True if a date, datetime, TimeSlice or TimeSet is "inside" the TimeSet range. False instead.
#          date or datetime test returns True if date/datetime is inside any TimeSet in the Slice
#          TimeSlice test returns True if all parts of given TimeSlice is inside intersections between the TimeSlice and TimeSet
#          TimeSet test returns True if all TimeSlices tests returns true
#
datetime.datetime( 2009, 1, 1, 12, 13, 14 ) in set1
slice2 in set3
set1 in set3

# --------------------------

