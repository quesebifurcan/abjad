from abjad import *


### TEST COPY LEAVES ###

def test_copy_note_01( ):
   m = Note(0, (1, 8))
   n = m.copy( )
   assert id(m) != id(n)
   assert m._parent is None
   assert n._parent is None

def test_copy_rest_01( ):
   r = Rest((1, 8))
   s = r.copy( )
   assert id(r) != id(s)
   assert r._parent is None
   assert s._parent is None

def test_copy_skip_01( ):
   s = Skip((1, 8))
   t = s.copy( )
   assert id(s) != id(t)
   assert s._parent is None
   assert t._parent is None

def test_copy_chord_01( ):
   d = Chord([2, 3, 4], (1, 4))
   e = d.copy( )
   assert id(d) != id(e)
   assert d._parent is None
   assert e._parent is None

def test_tuplet_copy_note_01( ):
   t = FixedDurationTuplet((1, 4), Note(0, (1, 8)) * 3)
   m = t[1]
   n = m.copy( )
   assert id(m) != id(n)
   assert m._parent is t
   assert n._parent is None


### TEST COPY COMPLETE CONTAINER ###

def test_copy_complete_container_01( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   u = t.copy( )
   id(u) is not id(t)
   check(t)
   check(u)


### TEST COPY ONE CONTAINERIZED NOTE ###

def test_copy_one_containerized_note_01( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   u = tcopy(t[0 : 1])
   assert isinstance(u, Staff)
   assert len(u) == 1
   assert isinstance(u[0], Note)
   assert u[0].pitch == t[0].pitch
   assert id(u[0]) is not id(t[0])
   assert u[0]._parent == u

def test_copy_one_containerized_note_02( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   u = tcopy(t[1 : 2])
   assert isinstance(u, Staff)
   assert len(u) == 1
   assert isinstance(u[0], Note)
   assert u[0].pitch == t[1].pitch
   assert id(u[0]) is not id(t[1])
   assert u[0]._parent == u
   
def test_copy_one_containerized_note_03( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   u = tcopy(t[-1 :])
   assert isinstance(u, Staff)
   assert len(u) == 1
   assert isinstance(u[0], Note)
   assert u[0].pitch == t[-1].pitch
   assert id(u[0]) is not id(t[-1])
   assert u[0]._parent == u
   
def test_copy_one_containerized_note_04( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   u = tcopy(t[-2:-1])
   assert isinstance(u, Staff)
   assert len(u) == 1
   assert isinstance(u[0], Note)
   assert u[0].pitch == t[-2].pitch
   assert id(u[0]) is not id(t[-2])
   assert u[0]._parent == u


### TEST COPY ONE TUPLETIZED NOTE ###

def test_copy_one_tupletized_note_01( ):
   t = Staff(FixedDurationTuplet((2, 8), Note(0, (1, 8)) * 3) * 3)
   u = t.leaves[4].copy( )
   assert isinstance(u, Note)
   assert u.pitch == t.leaves[4].pitch
   assert u.duration == t.leaves[4].duration
   assert id(u) != id(t.leaves[4])
   assert u.duration.prolated != t.leaves[4].duration.prolated

def test_copy_one_tupletized_note_02( ):
   t = Staff(FixedDurationTuplet((2, 8), Note(0, (1, 8)) * 3) * 3)
   u = t.leaves[5].copy( )
   assert isinstance(u, Note)
   assert u.pitch == t.leaves[5].pitch
   assert u.duration == t.leaves[5].duration
   assert id(u) != id(t.leaves[5])
   assert u.duration.prolated != t.leaves[5].duration.prolated


### TEST COPY ADJACENT CONTAINERIZED NOTES ###

def test_copy_adjacent_containerized_notes_01( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   u = tcopy(t[0:3])
   assert isinstance(u, Staff)
   assert len(u) == 3
   for i, x in enumerate(u):
      assert x.pitch == t[i].pitch
      assert id(x) is not id(t[i])
   assert check(u, ret=True)

def test_copy_adjacent_containerized_notes_02( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   u = tcopy(t[1:7])
   assert isinstance(u, Staff)
   assert len(u) == 6
   for i, x in enumerate(u):
      j = i + 1
      assert x.pitch == t[j].pitch
      assert id(x) is not id(t[j])
   assert check(u, ret=True)

### COPY ADJACENT TUPLETIZED NOTES ###
### note - right now notes get 'ripped' out of tuplets
### and so lose parentage;
### the key assertion that shows this is 
### x.duratum != y.duratum;
### a different type of copy would preserve parentage
### and 'cut' out a (partial) tuplet to return;
### eg, cutting the first two notes of a triplet would
### return a broken tuplet equal to 2/12.
### TODO - that functionality does not yet exist
### but should implement somewhere;
### the question is what the appropriate interface should be;
### maybe copy(t, (0, 1), mode = 'preserve partial tuplets') or
### a different verb like excise(t, (0, 1)).

def test_copy_adjacent_tupletized_notes_01( ):
   t = Staff(FixedDurationTuplet((2, 8), Note(0, (1, 8)) * 3) * 3)
   u = tcopy(t[1][0:2])
   assert isinstance(u, FixedDurationTuplet)
   assert len(u) == 2
   for i, x in enumerate(u):
      j = i + 0
      assert x.pitch == t[1][j].pitch
      assert id(x) != id(t[1][j])
   assert check(u, ret=True)

def test_copy_adjacent_tupletized_notes_02( ):
   t = Staff(FixedDurationTuplet((2, 8), Note(0, (1, 8)) * 3) * 3)
   u = tcopy(t[1][1:3])
   assert isinstance(u, FixedDurationTuplet)
   assert len(u) == 2
   for i, x in enumerate(u):
      j = i + 1
      assert x.pitch == t[1][j].pitch
      assert id(x) != id(t[1][j])
   assert check(u, ret=True)

### TODO - implement some sort of 'crossing' copy.
### given t = Staff(FixedDurationTuplet((2, 8), Note(0, (1, 8)) * 3) * 3)
### there is currently no way to copy, eg, leaves 0 - 5
### because leaves 0 - 3 belong to tuplet 0 
### while leaves 4 - 5 belong to tuplet 1;
### in other words, leaves 0 - 5 'cross' tuplet boundaries.
### not sure what the right interface here would be;
### it isn't possible to say t.leaves(0, 5) because t.leaves
### is merely a (built-in) list.
### this may motivate a (non-object oriented) copy( ) function;
### then copy(t, (0, 5), indices = 'leaves') might make sense;
### or leafCopy(t, (0, 5)), or something similar.


### TEST COPY ONE CONTAINERIZED TUPLET ###
   
def test_copy_one_containerized_tuplet_01( ):
   t = Staff(FixedDurationTuplet((2, 8), Note(0, (1, 8)) * 3) * 3)
   u = tcopy(t[0:1])
   assert isinstance(u, Staff)
   assert len(u) == 1
   assert isinstance(u[0], FixedDurationTuplet)
   assert u[0].duration == t[0].duration
   assert id(u[0]) is not id(t[0])
   assert u[0]._parent == u
   
def test_copy_one_containerized_tuplet_02( ):
   t = Staff(FixedDurationTuplet((2, 8), Note(0, (1, 8)) * 3) * 3)
   u = tcopy(t[1:2])
   assert isinstance(u, Staff)
   assert len(u) == 1
   assert isinstance(u[0], FixedDurationTuplet)
   assert u[0].duration == t[1].duration
   assert id(u[0]) is not id(t[1])
   assert u[0]._parent == u
   
def test_copy_one_containerized_tuplet_03( ):
   t = Staff(FixedDurationTuplet((2, 8), Note(0, (1, 8)) * 3) * 3)
   u = tcopy(t[-1:])
   assert isinstance(u, Staff)
   assert len(u) == 1
   assert isinstance(u[0], FixedDurationTuplet)
   assert u[0].duration == t[-1].duration
   assert id(u[0]) is not id(t[-1])
   assert u[0]._parent == u

def test_copy_one_containerized_tuplet_04( ):
   t = Staff(FixedDurationTuplet((2, 8), Note(0, (1, 8)) * 3) * 3)
   u = tcopy(t[-2:-1])
   assert isinstance(u, Staff)
   assert len(u) == 1
   assert isinstance(u[0], FixedDurationTuplet)
   assert u[0].duration == t[-2].duration
   assert id(u[0]) is not id(t[-2])
   assert u[0]._parent == u
