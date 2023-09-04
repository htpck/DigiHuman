
import numpy as np
import math

from .facedata import FaceBlendShape
from .blendshape_config import BlendShapeConfig

_blendshape_config = BlendShapeConfig()
    
def _remap(value, min, max) -> float:
    """
    np.clip(value, min, max) ->  clips the value to the range [min, max].
    For example,
    if value = 5, min = 3, and max = 7, then np.clip (value, min, max) = 5. But if value = 10, then np.clip (value, min, max) = 7.
    
    Remap a value from the range [min, max] to the range [0, 1].

    :param value: The value to remap.
    :param min: The minimum value in the range.
    :param max: The maximum value in the range.
    :return: The remapped value.
    
    for example: 
    _remap(0.5, 0, 1) = 0.5
    _remap(0.5, 0, 0.5) = 1
    _remap(0.5, 0.5, 1) = 0
    """

    return (np.clip(value, min, max) - min) / (max - min)

def _remap_blendshape(index: FaceBlendShape, value: float, config: BlendShapeConfig = None) -> float:
    '''Remap the value to the range of the blendshape'''
    global _blendshape_config
    if config is None:
        if _blendshape_config is None:
            _blendshape_config = config = BlendShapeConfig()
        else:
            config = _blendshape_config
    
    min, max =config.config.get(index)
    return _remap(value, min, max)

def dist(p, q) -> float:
    '''Euclidean distance between two points p and q'''
    return math.sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p, q)))

def dist2(p, q,o) -> float:
    return math.sqrt(sum((px - ox) ** 2.0 + (px - qx) ** 2.0 for px, qx,ox in zip(p, q,o)))
    
def map_value(value, in_min, in_max, out_min, out_max):
    # Calculate the ratio of the value to the input range
    value_ratio = (value - in_min) / (in_max - in_min)
    # Scale the ratio by the output range
    mapped_value = out_min + value_ratio * (out_max - out_min)
    # Return the mapped value
    return mapped_value


def _lerp(v0, v1, t):
    '''Linear interpolation between v0 and v1 by t'''
    '''t is between 0 and 1 fraction'''
    '''for example t = 0.5 returns the middle point between v0 and v1'''
    return (1 - t) * v0 + t * v1