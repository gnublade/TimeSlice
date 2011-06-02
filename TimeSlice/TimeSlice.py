"""
    *******************************************************************************
    * Copyright 2009 Rafael Marques Martins
    *
    * This file is part of TimeSlice python module.
    * 
    * TimeSlice is free software; you can redistribute it and/or modify
    * it under the terms of the GNU General Public License as published by
    * the Free Software Foundation; either version 2 of the License, or
    * (at your option) any later version.
    * 
    * TimeSlice is distributed in the hope that it will be useful,
    * but WITHOUT ANY WARRANTY; without even the implied warranty of
    * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    * GNU General Public License for more details.
    * 
    * You should have received a copy of the GNU General Public License
    * along with Foobar; if not, write to the Free Software
    * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
    * 
    *******************************************************************************/
"""

import datetime
import calendar

DAYLY = 1
MONTHLY = 2
YEARLY = 3

class TimeSliceException(Exception):
    pass

class TimeSlice:
    start = None
    end = None

    def __init__( self, start = None, end = None ):
        if not ( isinstance( start, datetime.date ) ):
            raise TimeSliceException('start argument must be instance of datetime.datetime or datetime.date')

        if not ( isinstance( end, datetime.date ) ):
            raise TimeSliceException('end argument must be instance of datetime.datetime or datetime.date')

        if not ( isinstance( start, datetime.datetime ) ):
            start = datetime.datetime( start.year, start.month, start.day )

        if not ( isinstance( end, datetime.datetime ) ):
            end = datetime.datetime( end.year, end.month, end.day )


        if start > end:
            raise TimeSliceException('start time could not be greater than end time')

        self.start = start
        self.end = end

    def __contains__( self, x ):
        if isinstance( x, datetime.date ) and not isinstance( x, datetime.datetime ):
            x = datetime.datetime( *x.timetuple()[:3] )

        if isinstance( x, datetime.datetime ):
            if x >= self.start and x < self.end:
                return True
            return False

        if x.duration() == self.intersect( x ).duration():
            return True

        return False

    def __eq__( self, x ):
        if isinstance( x, TimeSlice ):
            return self.start == x.start and self.end == x.end
        return False

    def __ge__( self, x ):
        if not ( isinstance( x, TimeSlice ) ):
            return NotImplemented

        return self.duration() >= x.duration()

    def __gt__( self, x ):
        if not ( isinstance( x, TimeSlice ) ):
            raise TimeSliceException('Invalid operand type. Expected TimeSlice')

        return self.duration() > x.duration()

    def __le__( self, x ):
        if not ( isinstance( x, TimeSlice ) ):
            raise TimeSliceException('Invalid operand type. Expected TimeSlice')

        return self.duration() <= x.duration()

    def __lt__( self, x ):
        if not ( isinstance( x, TimeSlice ) ):
            raise TimeSliceException('Invalid operand type. Expected TimeSlice')

        return self.duration() < x.duration()

    def __ne__( self, x ):
        if isinstance( x, TimeSlice ):
            return not ( self.start == x.start and self.end == x.end )

        return True


    def timedelta( self ):
        return self.end - self.start

    def duration( self ):
        timedelta = self.timedelta()
        return timedelta.days * 86400 + timedelta.seconds

    def seconds( self ):
        return self.duration()

    def intersect( self, arg ):
        if not arg:
            return None

        if isinstance( arg, TimeSet ):
            return arg.intersect( self )

        timeSlice = arg
        s1 = self.start
        e1 = self.end

        s2 = timeSlice.start
        e2 = timeSlice.end
        
        if e1 < s2 or e2 < s1:
            return None

        start = max( [ s1, s2 ] )
        end   = min( [ e1, e2 ] )

        # Intersection of a point and a point is a point!
        if start == end:
            return None

        return TimeSlice( start, end )

    def __repr__( self ):
        return '<TimeSlice instance ' + str( ( self.start, self.end ) ) + ' >'

    def difference( self, timeSlice, absolute = False ):
        if not isinstance( timeSlice, TimeSlice ):
            raise TimeSliceException('Invalid argument type. Expected TimeSlice')

        if ( not absolute ) and ( timeSlice.start <= self.start and timeSlice.end >= self.end ):
            return TimeSet()


        if self == timeSlice:
            return TimeSet()

        intersection = self.intersect( timeSlice )

        if intersection:
            if intersection.start > self.start and intersection.end < self.end:
                s1 = self.start
                e1 = intersection.start

                s2 = intersection.end
                e2 = self.end
                return TimeSet( [ TimeSlice( s1, e1 ), TimeSlice( s2, e2 ) ] )
 
            if absolute and intersection.start > timeSlice.start and intersection.end < timeSlice.end:
                s1 = timeSlice.start
                e1 = intersection.start

                s2 = intersection.end
                e2 = timeSlice.end
                return TimeSet( [ TimeSlice( s1, e1 ), TimeSlice( s2, e2 ) ] )

                
            if intersection == self:
                return TimeSet()

           
            if intersection.start == self.start:
                s1 = intersection.end
                e1 = self.end
                return TimeSet( [ TimeSlice( s1, e1 ) ] )


            s1 = self.start
            e1 = intersection.start
            return TimeSet( [ TimeSlice( s1, e1 ) ] )


        return TimeSet( [ self ] )


    def __sub__( self, arg ):
        if isinstance( arg, TimeSet ):
            tmp = TimeSet( [ self ] )
            return tmp - arg

        return self.difference( arg )

    def __add__( self, arg ):
        if isinstance( arg, TimeSet ):
            return arg + self

        if isinstance( arg, int ) or isinstance( arg, int ):
            return self.duration() + arg

        if not isinstance( arg, TimeSlice ):
            raise TimeSliceException('Invalid argument type. Expected TimeSlice')

        intersection = self.intersect( arg ) 

        if intersection:
            s1 = min( [ self.start, arg.start ] )
            e1 = intersection.start

            s2 = intersection.end
            e2 = max( [ self.end, arg.end ] )

            return TimeSet( [ TimeSlice( s1, e2 ) ] )
           
        return TimeSet( [ self, arg ] )

    #def __radd__( self, arg ):
    #    return self + arg

class TimeSet:
    slices = []

    def __init__( self, list = [] ):
        self.slices = []
        for element in list:
            if not isinstance( element, TimeSlice ):
                raise TimeSliceException('Invalid type. Expected TimeSlice instance')

            self.append( element )

    def __contains__( self, x ):
        if isinstance( x, datetime.date ) and not isinstance( x, datetime.datetime ):
            x = datetime.datetime( *x.timetuple()[:3] )

        if isinstance( x, datetime.datetime ):
            for s in self:
                if x in s:
                    return True
            return False

        if not ( x - self ).duration():
            return True

        return False
    
    @classmethod
    def fromRange( self, repeat = 1, start = DAYLY, end = None ):
        slices = []
        
        if not ( isinstance( start, datetime.datetime ) ):
            start = datetime.datetime( start.year, start.month, start.day )

        if not ( isinstance( end, datetime.datetime ) ):
            end = datetime.datetime( end.year, end.month, end.day )

        
        if repeat == DAYLY:
            e = start
            while 1:
                s = e
                d1 = datetime.datetime( s.year, s.month, s.day, s.hour, s.minute, s.second ) + datetime.timedelta( 1 )
                e = datetime.datetime( d1.year, d1.month, d1.day, s.hour, s.minute, s.second )
                if e < end:
                    slices.append( TimeSlice( s, e )  ) 
                else:
                    break
            return TimeSet( slices )

        elif repeat == MONTHLY:
            e = start
            while 1:
                s = e
                d1 = datetime.datetime( s.year, s.month, 1, s.hour, s.minute, s.second ) + datetime.timedelta( 35 )
                tmpDay = min( [ calendar.monthrange( d1.year, d1.month )[ 1 ], start.day ] )

                e = datetime.datetime( d1.year, d1.month, tmpDay, s.hour, s.minute, s.second )
                if e <= end:
                    slices.append( TimeSlice( s, e )  ) 
                else:
                    break
            return TimeSet( slices )

        elif repeat == YEARLY:
            pass
        
        return []

    def max( self ):
        return max( [ x.end for x in self.slices ] ) or None

    def min( self ):
        return min( [ x.start for x in self.slices ] ) or None

    def seconds( self ):
        return self.duration()
    
    def duration( self ):
        return sum( [ x.duration() for x in self.slices ] )

    @classmethod
    def sliceCmp( self, a, b ):
        if a.start == b.start:
            return 0

        if a.start < b.start:
            return -1

        return 1

    def append( self, element ):
        newTimeSet = TimeSet()
        newTimeSet.slices.extend( self.slices )
        newTimeSet += element

        self.slices = []
        self.slices.extend( newTimeSet.slices )

        self.slices.sort( cmp = TimeSet.sliceCmp )

    def intersectSlice( self, arg ):
        intersections = []
        if isinstance( arg, TimeSlice ):
            for item in self.slices:
                tmpIntersection = item.intersect( arg )
                if tmpIntersection:
                    intersections.append( tmpIntersection )

            return TimeSet( intersections )

        raise TimeSliceException('Invalid argument type. Expected TimeSlice or TimeSet')


    def differenceSlice( self, arg ):
        newTimeSet = TimeSet()
        newTimeSet.slices.extend( self.slices )

        i = 0
        while i < len( newTimeSet.slices ):
            slice = newTimeSet[ i ]
            
            intersection = slice.intersect( arg ) if slice != arg else slice
            
            if intersection:
                newTimeSet.slices.remove( slice )
                i = -1

                if not ( intersection.start == slice.start and intersection.end == slice.end ):
                    newTimeSet.slices.extend( ( slice - intersection ).slices )

            i += 1

        
        newTimeSet.slices.sort( cmp = TimeSet.sliceCmp )

        return newTimeSet


    def __sub__( self, arg ):
        if isinstance( arg, TimeSet ):
            newTimeSet = TimeSet()
            newTimeSet.slices.extend( self.slices )

            for slice in arg.slices:
                newTimeSet = newTimeSet.differenceSlice( slice )

            return newTimeSet

        if isinstance( arg, TimeSlice ):
            return self.differenceSlice( arg )

        raise TimeSliceException('Invalid argument type. Expected TimeSlice or TimeSet')
        

    def intersect( self, arg ):
        newTimeSet = TimeSet()

        if isinstance( arg, TimeSet ):
            intersections = []
            for slice in arg:
                intersections.extend( self.intersectSlice( slice ).slices )
            return TimeSet( intersections )
            
        if isinstance( arg, TimeSlice ):
            return self.intersectSlice( arg )

        raise TimeSliceException('Invalid argument type. Expected TimeSlice or TimeSet')

    
    def addSlice( self, arg ):
        slices = [ arg ]
        i = 0
        while i < len( slices ):
            j = 0
            while j < len( self.slices ):
                if slices[ i ].intersect( self.slices[ j ] ):
                    tmpSlice = slices[ i ]
                    if tmpSlice in slices:
                        slices.remove( slices[ i ] )
                        slices.extend( tmpSlice.difference( self.slices[ j ], True ).slices )
                        i = -1
                        j = len( self.slices )
                j += 1
            i += 1
        
        newTimeSet = TimeSet()
        newTimeSet.slices.extend( self.slices )
        newTimeSet.slices.extend( slices )

        newTimeSet.slices.sort( cmp = TimeSet.sliceCmp )
        return newTimeSet
           


    def __add__( self, arg ):
        if isinstance( arg, TimeSet ):
            newTimeSet = TimeSet()
            newTimeSet.slices.extend( self.slices )

            for slice in arg.slices:
                newTimeSet = newTimeSet.addSlice( slice )

            return newTimeSet

        if isinstance( arg, TimeSlice ):
            return self.addSlice( arg )

        raise TimeSliceException('Invalid argument type. Expected TimeSlice or TimeSet')
        
    def __len__( self ):
        return len(self.slices)

    def __repr__( self ):
        return "[" + ",\n".join( [ str( x ) for x in self ] ) + "]"

    def __getitem__( self, index ):
        return self.slices[ index ]
