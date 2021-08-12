from .errors import VMRError
from .strip import VMElement, bool_prop, str_prop, float_prop, LevelType
from . import kinds

class InputStrip(VMElement):
  """ Base class for input strips. """
  @classmethod
  def make(cls, is_physical, remote, index, **kwargs):
    """
    Factory function for input strips.

    Returns a physical/virtual strip for the remote's kind.
    """
    PhysStrip, VirtStrip = _strip_pairs[remote.kind.id]
    IS_cls = PhysStrip if is_physical else VirtStrip
    return IS_cls(remote, index, **kwargs)

  @property
  def identifier(self):
    return f'Strip[{self.index}]'
    
  @property
  def channel_level_type(self):
    # Hardcoded for testing - needs to know what number strip it is, calculate the offset based on channel counts
    # This is A2
    return LevelType.POST_FADER
    

  solo = bool_prop('Solo')
  mute = bool_prop('Mute')
  
  gain = float_prop('Gain', range=(-60,12))
  comp = float_prop('Comp', range=(0,10))
  gate = float_prop('Gate', range=(0,10))
  gate = float_prop('Gate', range=(0,10))

  label = str_prop('Label')
  device = str_prop('device.name')
  sr = str_prop('device.sr')
  
  
class PhysicalInputStrip(InputStrip):
  mono = bool_prop('Mono')
  channel_count = 2
  _channel_offset = 0

class VirtualInputStrip(InputStrip):
  mono = bool_prop('MC')
  _channel_offset = 10
  channel_count = 8
  @property
  def channel_level_start(self):
    return self._channel_offset+((self.index-5)*self.channel_count)


def _make_strip_mixin(kind):
  """ Creates a mixin with the kind's strip layout set as class variables. """
  num_A, num_B = kind.layout
  return type(f'StripMixin{kind.name}', (), {
    **{f'A{i}': bool_prop(f'A{i}') for i in range(1, num_A+1)},
    **{f'B{i}': bool_prop(f'B{i}') for i in range(1, num_B+1)}
  })

_strip_mixins = {kind.id: _make_strip_mixin(kind) for kind in kinds.all}

def _make_strip_pair(kind):
  """ Creates a PhysicalInputStrip and a VirtualInputStrip of a kind. """
  StripMixin = _strip_mixins[kind.id]
  PhysStrip = type(f'PhysicalInputStrip{kind.name}', (PhysicalInputStrip, StripMixin), {})
  VirtStrip = type(f'VirtualInputStrip{kind.name}', (VirtualInputStrip, StripMixin), {})
  return (PhysStrip, VirtStrip)

_strip_pairs = {kind.id: _make_strip_pair(kind) for kind in kinds.all}
