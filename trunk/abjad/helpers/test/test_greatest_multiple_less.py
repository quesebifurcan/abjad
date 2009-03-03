from abjad.helpers.greatest_multiple_less import _greatest_multiple_less
from abjad import *


def test_greatest_multiple_less_01( ):
   '''Return the least multiple of m greater than or equal to n.'''

   assert _greatest_multiple_less(10, 0) == 0
   assert _greatest_multiple_less(10, 1) == 0
   assert _greatest_multiple_less(10, 2) == 0
   assert _greatest_multiple_less(10, 13) == 10
   assert _greatest_multiple_less(10, 28) == 20
   assert _greatest_multiple_less(10, 40) == 40
   assert _greatest_multiple_less(10, 41) == 40
   

def test_greatest_multiple_less_02( ):
   '''Return the least multiple of m greater than or equal to n.'''

   assert _greatest_multiple_less(7, 0) == 0
   assert _greatest_multiple_less(7, 1) == 0
   assert _greatest_multiple_less(7, 2) == 0
   assert _greatest_multiple_less(7, 13) == 7
   assert _greatest_multiple_less(7, 28) == 28
   assert _greatest_multiple_less(7, 40) == 35
   assert _greatest_multiple_less(7, 41) == 35
