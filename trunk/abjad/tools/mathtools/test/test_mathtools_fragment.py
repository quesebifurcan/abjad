from abjad.tools import mathtools
from fractions import Fraction
import py.test


def test_mathtools_fragment_01( ):
   '''
   fragment can take integers.
   '''
   t = mathtools.fragment(4, [1,2])
   assert len(t) == 3
   assert t[0] == 1
   assert t[1] == 2
   assert t[2] == 1


def test_mathtools_fragment_02( ):
   '''
   fragment can take floats.
   '''
   t = mathtools.fragment(4, [0.5, 2])
   assert len(t) == 3
   assert t[0] == 0.5
   assert t[1] == 2
   assert t[2] == 1.5


def test_mathtools_fragment_03( ):
   '''
   fragment can take rationals.
   '''
   t = mathtools.fragment(1, [Fraction(1, 2), Fraction(1, 3)])
   assert len(t) == 3
   assert t[0] == Fraction(1, 2)
   assert t[1] == Fraction(1, 3)
   assert t[2] == Fraction(1, 6)


## ERRORS ##

def test_mathtools_fragment_04( ):
   '''Raise ValueError when the sum of the fragments is not smaller 
   than the total to be fragmented.'''

   assert py.test.raises(ValueError, 'mathtools.fragment(1, [2])')   

