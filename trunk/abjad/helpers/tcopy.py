from abjad.helpers.contiguity import _are_contiguous_music_elements


### TODO: make tcopy( ) automatically SHINK or TRIM

def tcopy(ll):
   '''
   Clone list ll of contiguous music from some container.
   
   Usage:

     tcopy(t[37 : 39 + 1])

   Return copied music in container of type T,
   where T is the type of the parent of the first element in ll.
   '''

   # assert contiguous elements in ll
   if not _are_contiguous_music_elements(ll):
     raise ValueError('Input must be contiguous music elements.')

   # remember parent
   parent = ll[0]._parent

   # remember parent's music
   parents_music = ll[0]._parent._music

   # strip parent of music temporarily
   parent._music = [ ]

   # copy parent without music
   result = parent.copy( )

   # give music back to parent
   parent._music = parents_music

   # populate result with references to input list
   #result.extend(ll)
   result._music.extend(ll)

   # populate result with deepcopy of input list and fracture spanners
   result = result.copy( )

   # point elements in result to result as new parent
   for element in result:
      element._parent = result

   # point elements in input list back to old parent
   for element in ll:
      element._parent = parent

   # return copy
   return result
