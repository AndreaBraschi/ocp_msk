import json
from pathlib import Path

import numpy as np

# local imports
from ..kinematic_coupling.linear import linear
from ..kinematic_coupling.cubic  import cubic


def apply_constraints(
    x,                          # ca.MX, interleaved [q; q_dot] of independent coords
    acc,                        # ca.MX, accelerations of independent coords
    q_all_list: list[str],      # names of ALL coordinates (independent + dependent)
    independent_indices,        # integer array / list of independent coord indices (0-based)
    path_to_config: str | Path,
):

    path_to_config = Path(path_to_config)
    with open(path_to_config) as fh:
        config = json.load(fh)

    # Extract q and q_dot from the interleaved independent state
    q     = x[0::2]    # every even entry
    q_dot = x[1::2]    # every odd entry

    num_q_all = len(q_all_list)

    # Allocate full vectors
    q_all     = np.zeros((num_q_all, ))
    q_dot_all = np.zeros((num_q_all, ))
    acc_all   = np.zeros((num_q_all, ))

    # Fill independent coordinates first
    ind = list(independent_indices)
    q_all[ind] = q
    q_dot_all[ind] = q_dot
    acc_all[ind] = acc

    # Apply constraints for each coupling
    for constraint_name, cfg in config.items():
        dep_name  = cfg["dependent_coordinate"]
        ind_name  = cfg["independent_coordinate"]
        coupling  = cfg["coupling"]
        coeffs    = cfg["coefficients"]

        dep_idx = q_all_list.index(dep_name)
        ind_idx = q_all_list.index(ind_name)

        pos = q_all[ind_idx]
        vel = q_dot_all[ind_idx]
        acc_in = acc_all[ind_idx]

        if coupling == "linear":
            a, b = coeffs[0], coeffs[1]
            val = linear(pos, vel, acc_in, a, b)

        elif coupling == "cubic":
            a, b, c, d = coeffs[0], coeffs[1], coeffs[2], coeffs[3]
            val = cubic(pos, vel, acc_in, a, b, c, d)

        else:
            raise ValueError(f"Unknown coupling type: '{coupling}'")

        q_all[dep_idx]     = val["pos"]
        q_dot_all[dep_idx] = val["vel"]
        acc_all[dep_idx]   = val["acc"]

    x_all = np.column_stack((np.ravel(q_all), np.ravel(q_dot_all))).ravel()  # shape (2*num_q_all,)

    return x_all, acc_all