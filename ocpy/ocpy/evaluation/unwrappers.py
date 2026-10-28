import json
import pickle
import numpy as np

def unwrap_muscle_solution(solution_path: str, config_filepath: str, output_dict_path: str):
    # ---------- read config file ----------- #
    with open(config_filepath) as f:
        cfg = json.load(f)

    N = cfg["collocation"]["number_of_segments"]
    d = cfg["collocation"]["num_points"]
    col_points = N * d
    mesh_end_points = N + 1

    # ---------- read output config file ----------- #
    with open(output_dict_path) as f:
        cfg_out = json.load(f)

    num_q_ind = cfg_out["num_q_ind"]
    num_actuators = cfg_out["num_actuators"]
    num_muscles = cfg_out["num_muscles"]

    # ---------- read solution file ----------- #
    with open(solution_path, 'rb') as f:
        solution = pickle.load(f)

    w_opt = solution['w_opt']

    dims_x = num_q_ind * 2
    X_col = np.zeros((dims_x, col_points))
    u = 0
    for n in range(col_points):
        X_col[:, n] = w_opt[u:u + dims_x]
        u += dims_x


    # mesh end points
    X = np.zeros((dims_x, mesh_end_points))
    for n in range(mesh_end_points):
        X[:, n] = w_opt[u:u + dims_x]
        u += dims_x

    # Muscle activation
    # 1) collocation points
    a_m_col = np.zeros((num_muscles, N * d))
    for n in range(col_points):
        a_m_col[:, n] = w_opt[u:u + num_muscles]
        u += num_muscles

    # 2) mesh end-points
    a_m = np.zeros((num_muscles, mesh_end_points))
    for n in range(mesh_end_points):
        a_m[:, n] = w_opt[u:u + num_muscles]
        u += num_muscles

    # MTU Force
    # 1) collocation points
    fT_col = np.zeros((num_muscles, N * d))
    for n in range(col_points):
        fT_col[:, n] = w_opt[u:u + num_muscles]
        u += num_muscles

    # 2) mesh end-points
    fT = np.zeros((num_muscles, mesh_end_points))
    for n in range(mesh_end_points):
        fT[:, n] = w_opt[u:u + num_muscles]
        u += num_muscles

    # Torque actuators
    # 1) collocation points
    a_a_col = np.zeros((num_actuators, N * d))
    for n in range(col_points):
        a_a_col[:, n] = w_opt[u:u + num_actuators]
        u += num_actuators

    # 2) mesh end-points
    a_a = np.zeros((num_actuators, mesh_end_points))
    for n in range(mesh_end_points):
        a_a[:, n] = w_opt[u:u + num_actuators]
        u += num_actuators


    # -------------------- Controls ------------------------- #
    e_a = np.zeros((num_actuators, mesh_end_points))
    for n in range(mesh_end_points):
        e_a[:, n] = w_opt[u:u + num_actuators]
        u += num_actuators


    A_col = np.zeros((num_q_ind, N * d))
    for n in range(col_points):
        A_col[:, n] = w_opt[u:u + num_q_ind]
        u += num_q_ind


    return X_col, A_col
