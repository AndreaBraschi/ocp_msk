import json
import pickle
import numpy as np
import casadi as ca
from typing import List

# local imports
from ..numerical_functions.apply_constraints import apply_constraints

def evaluate(X_col, A_col, config_filepath: str, x_scaling_path: str, output_dict_path: str, external_func_path: str,
             external_func_indices: List[int], kinematic_coupling_path: str):

    # ---------- read config file ----------- #
    with open(config_filepath) as f:
        cfg = json.load(f)

    N = cfg["collocation"]["number_of_segments"]
    d = cfg["collocation"]["num_points"]
    col_points = N * d


    # ---------- read solution file ----------- #
    with open(x_scaling_path, 'rb') as f:
        x_scaling = pickle.load(f)

    q_scaling = x_scaling['q_scaling']
    qdot_scaling = x_scaling['qdot_scaling']
    acc_scaling = x_scaling['acc_scaling']

    # ---------- read output config file ----------- #
    with open(output_dict_path) as f:
        cfg_out = json.load(f)

    q_names = cfg_out["q_names"]
    q_ind_indices = cfg_out["q_ind_indices"]
    num_q_all = len(q_names)


    #------------ load external function (rigid body dynamics) ----------- #
    F = ca.external('F', external_func_path)

    # ----------- unscale design variables that serve as input to the external function ---------- #
    X_nsc = np.zeros_like(X_col)
    X_nsc[::2] = X_col[::2] * q_scaling[q_ind_indices, None]
    X_nsc[1::2] = X_col[1::2] * qdot_scaling[q_ind_indices, None]

    A_nsc = A_col * acc_scaling[q_ind_indices, None]


    # pre-allocate space in memory for accumulation during loop over collocation points
    q_unscaled = np.zeros((col_points, num_q_all))
    qdot_unscaled = np.zeros((col_points, num_q_all))
    acc_unscaled = np.zeros((col_points, num_q_all))

    output = np.zeros((col_points, len(external_func_indices)))

    for i in range(col_points):
        # current independent q and q_dot
        x_i = X_nsc[:, i]

        # current independent accelerations
        acc_i = A_nsc[:, i]

        # apply kinematic couplings --> get full x and acc (independent and dependent)
        x_all_i, acc_all_i = apply_constraints(x_i, acc_i, q_names, q_ind_indices,
                                               path_to_config=kinematic_coupling_path)

        q_unscaled[i, :] = x_all_i[::2]
        qdot_unscaled[i, :] = x_all_i[1::2]
        acc_unscaled[i, :] = acc_all_i

        # evaluate external function: rigid body dynamics
        Ti = F(ca.vertcat(x_all_i, acc_all_i))
        output[i, :] = Ti[external_func_indices, 0].full().ravel()


    return q_unscaled, qdot_unscaled, acc_unscaled, output

