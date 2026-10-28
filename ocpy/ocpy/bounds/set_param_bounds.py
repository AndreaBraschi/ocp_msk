import numpy as np
from typing import Dict, Union, List

def set_param_bounds(cfg) -> Dict[str, Dict[str, np.ndarray]]:
    # This function assign the user defined residual forces.


    bounds: Dict[str, Dict[str, np.ndarray]] = {}
    scaling = {}

    params = cfg["params"]
    keys = params.keys()

    for i, key in enumerate(list(keys)):
        items = params[key]

        param_lower: float = items['bounds'][0]
        param_upper: float = items['bounds'][1]
        param_size: int = items['size']

        param_range = param_upper - param_lower

        lower = param_lower * np.ones(param_size)
        upper =  param_upper * np.ones(param_size)

        scaling[key] = param_range

        bounds[key] = {
            "lower": lower / param_range,
            "upper": upper / param_range,
        }

    return bounds, scaling