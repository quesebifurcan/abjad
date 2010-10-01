from fractions import Fraction
from abjad.components.Tuplet._TupletDurationInterface import _TupletDurationInterface


class _FixedDurationTupletDurationInterface(_TupletDurationInterface):

   def __init__(self, _client, target):
      #_TupletDurationInterface.__init__(self, _client)
      ## new ##
      dummy_multiplier = 1
      _TupletDurationInterface.__init__(self, _client, dummy_multiplier)
      ## end ##
      self.target = target

   ## PUBLIC ATTRIBUTES ##

   @property
   def multiplied(self):
      return self.target

#   @property
#   def multiplier(self):
#      if 0 < len(self._client):
#         return self.target / self.contents
#      else:
#         return None

   @apply
   def multiplier( ):
      def fget(self):
         if 0 < len(self._client):
            return self.target / self.contents
         else:
            return None
      def fset(self, expr):
         pass
      return property(**locals( ))

   @apply
   def target( ):
      def fget(self):
         return self._target
      def fset(self, expr):
         if isinstance(expr, (int, long)):
            rational = Fraction(expr)
         elif isinstance(expr, tuple):
            rational = Fraction(*expr)
         #elif isinstance(expr, Fraction):
         elif hasattr(expr, 'numerator') and hasattr(expr, 'denominator'):
            rational = Fraction(expr)
         else:
            raise ValueError('Can not set tuplet rational from %s.' % 
               str(expr))
         if 0 < rational:
            self._target = rational
         else:
            raise ValueError('Tuplet rational %s must be positive.' %
               rational)
      return property(**locals( ))
