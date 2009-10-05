from abjad import *


def test_lilytools_HeaderBlock_01( ):

   header_block = lilytools.HeaderBlock( )
   header_block.composer = Markup('Josquin')
   header_block.title = Markup('Missa sexti tonus')

   r'''
   \header {
           composer = \markup { Josquin }
           title = \markup { Missa sexti tonus }
   }
   '''

   assert header_block.format == '\\header {\n\tcomposer = \\markup { Josquin }\n\ttitle = \\markup { Missa sexti tonus }\n}'
