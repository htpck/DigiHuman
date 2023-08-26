
import numpy as np
import math

from regex import B
from .facedata import FaceBlendShape
from .blendshape_config import BlendShapeConfig

_blendshape_config = BlendShapeConfig()
    
def _remap(value, min, max) -> float:
    return (np.clip(value, min, max) - min) / (max - min)

def _remap_blendshape(index: FaceBlendShape, value: float, config: BlendShapeConfig = None) -> float:
    global _blendshape_config
    if config is None:
        if _blendshape_config is None:
            _blendshape_config = config = BlendShapeConfig()
        else:
            config = _blendshape_config
    
    min, max =config.config.get(index)
    return _remap(value, min, max)

def dist(p, q) -> float:
    return math.sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p, q)))

def dist2(p, q,o) -> float:
    return math.sqrt(sum((px - ox) ** 2.0 + (px - qx) ** 2.0 for px, qx,ox in zip(p, q,o)))
    
def map_value(self,value, in_min, in_max, out_min, out_max):
    # Calculate the ratio of the value to the input range
    value_ratio = (value - in_min) / (in_max - in_min)
    # Scale the ratio by the output range
    mapped_value = out_min + value_ratio * (out_max - out_min)
    # Return the mapped value
    return mapped_value
