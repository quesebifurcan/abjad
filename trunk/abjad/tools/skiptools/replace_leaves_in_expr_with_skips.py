from abjad.tools.skiptools.Skip import Skip
from abjad.tools.leaftools.iterate_leaves_forward_in_expr import iterate_leaves_forward_in_expr


def replace_leaves_in_expr_with_skips(expr):
   r'''.. versionadded:: 1.1.1

   Replace leaves with skips in `expr`::

      abjad> staff = Staff(Measure((2, 8), macros.scale(2)) * 2)
      abjad> skiptools.replace_leaves_in_expr_with_skips(staff[0])
      abjad> print staff.format
      \new Staff {
            \time 2/8
            s8
            s8
            \time 2/8
            c'8
            d'8
      }

   Return none.

   .. versionchanged:: 1.1.2
      renamed ``leaftools.replace_leaves_with_skips_in( )`` to
      ``skiptools.replace_leaves_in_expr_with_skips( )``.

   .. versionchanged:: 1.1.2
      renamed ``leaftools.replace_leaves_with_skips_in_expr( )`` to
      ``skiptools.replace_leaves_in_expr_with_skips( )``.

   .. versionchanged:: 1.1.2
      renamed ``leaftools.replace_leaves_in_expr_with_skips( )`` to
      ``skiptools.replace_leaves_in_expr_with_skips( )``.
   '''
   from abjad.tools import componenttools

   for leaf in iterate_leaves_forward_in_expr(expr):
      skip = Skip(leaf)
      componenttools.move_parentage_and_spanners_from_components_to_components([leaf], [skip])
