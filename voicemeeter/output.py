# param_name => is_numeric
from .errors import VMRError
from .strip import VMElement, bool_prop, str_prop, float_prop, LevelType


class OutputBus(VMElement):
  busmodes = {
    'normal' : 'Normal',
    'Amix'   : 'Mix down A',
    'Bmix'   : 'Mix down B',
    'Repeat' : 'stereo Repeat',
    'Composite' : 'Composite',
    'TVMix' : 'Up Mix TV',
    'UpMix21' : 'Up Mix 2.1',
    'UpMix41': 'Up Mix 4.1',
    'UpMix61': 'Up Mix 6.1',
    'CenterOnly' : 'Center Only',
    'LFEOnly' : 'LFE Only',
    'Rear Only': 'LFE Only',
  }
  """ Base class for output busses. """
  @classmethod
  def make(cls, is_physical, *args, **kwargs):
    """
    Factory function for output busses.

    Returns a physical/virtual strip for the remote's kind
    """
    OB_cls = PhysicalOutputBus if is_physical else VirtualOutputBus
    return OB_cls(*args, **kwargs)

  @property
  def identifier(self):
    return f'Bus[{self.index}]'
  
  @property
  def channel_level_type(self):
    return LevelType.OUTPUT

  mute = bool_prop('Mute')
  gain = float_prop('Gain', range=(-60,12))
  channel_count = 8

  @property
  def mode(self):
    for busmode in list(busmodes):
      if self.get('mode.' + busmode ):
        return busmodes[busmode]

  def set_modes(self,modes):
    self.modes = modes

  
  
class PhysicalOutputBus(OutputBus):
  _channel_offset = 0
  
class VirtualOutputBus(OutputBus):
  _channel_offset = channel_count * 8*5