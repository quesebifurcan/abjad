from abjad.receipt.parentage import ParentageReceipt
from abjad.receipt.spanners import SpannersReceipt


class Receipt(object):
   '''Well structured references attaching to some Abjad component.'''

   def __init__(self, component):
      self._component = component
      self._parent_receipt = _ParentReceipt(component)
      self._spanners_receipt = _SpannersReceipt(component)

   ## PRIVATE METHODS ##

   ## TODO: Reimplement dynamically
   def _clear_all_references(self):
      self.__init__(self)
