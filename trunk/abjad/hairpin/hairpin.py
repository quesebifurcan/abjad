from abjad.spanner.grobhandler import _GrobHandlerSpanner


#class _Hairpin(_GrobHandlerSpanner):
class Hairpin(_GrobHandlerSpanner):

   #def __init__(self, music = None, start = None, stop = None, trim = False):
   def __init__(self, music, descriptor, trim = False):
      _GrobHandlerSpanner.__init__(self, 'DynamicLineSpanner', music)
      start, shape, stop = self._parse_descriptor(descriptor)
      self._shape = shape
      self.start = start
      self.stop = stop
      self.trim = trim
  
   ## PRIVATE ATTRIBUTES ##

   def _right(self, leaf):
      from abjad.chord.chord import Chord
      from abjad.note.note import Note
      result = [ ]
      if not self.trim:
         if self._isMyFirstLeaf(leaf):
            result.append('\\%s' % self._shape)
            if self.start:
               result.append('\\%s' % self.start)
         if self._isMyLastLeaf(leaf):
            if self.stop:
               result.append('\\%s' % self.stop)
            elif not leaf.dynamics:
               result.append('\\!')
      else:
         if self._isMyFirst(leaf, (Chord, Note)):
            result.append('\\%s' % self._shape)
            if self.start:
               result.append('\\%s' % self.start)
         if self._isMyLast(leaf, (Chord, Note)):
            if self.stop:
               result.append('\\%s' % self.stop)
            elif not leaf.dynamics:
               result.append('\\!')
      return result
   
   ## PRIVATE METHODS ##

   def _parse_descriptor(self, descriptor):
      '''Example descriptors:
         '<'
         'p <'
         'p < f'
      '''
      assert isinstance(descriptor, str)
      parts = descriptor.split( )
      num_parts = len(parts)
      start, shape, stop = None, None, None
      if parts[0] in ('<', '>'):
         assert 1 <= num_parts <= 2
         if num_parts == 1:
            shape = parts[0]
         else:
            shape = parts[0]
            stop = parts[1]
      else:
         assert 2 <= num_parts <= 3
         if num_parts == 2:
            start = parts[0]
            shape = parts[1]
         else:
            start = parts[0]
            shape = parts[1]
            stop = parts[2]
      assert shape in ('<', '>')
      return start, shape, stop

   ## PUBLIC ATTRIBUTES ##

   @apply
   def start( ):
      def fget(self):
         return self._start
      def fset(self, arg):
         self._start = arg
      return property(**locals( ))

   @apply
   def stop( ):
      def fget(self):
         return self._stop
      def fset(self, arg):
         self._stop = arg
      return property(**locals( ))

   @apply
   def trim( ):
      def fget(self):
         return self._trim
      def fset(self, arg):
         self._trim = arg
      return property(**locals( ))


#def Hairpin(music, descriptor, trim = False):
#   #start, shape, stop = _parse_descriptor(descriptor)
#   hp = _Hairpin( )
#   start, shape, stop = hp._parse_descriptor(descriptor)
#   if shape == '<':
#      from crescendo import Crescendo
#      result = Crescendo(music, start = start, stop = stop, trim = trim)
#   elif shape == '>':
#      from decrescendo import Decrescendo
#      result = Decrescendo(music, start = start, stop = stop, trim = trim)
#   return result
