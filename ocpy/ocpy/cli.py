import argparse
from . import muscle_driven
from . import torque_driven

def main():
    parser = argparse.ArgumentParser(description=f'Tool to solve Optimal Control Problems for Musculoskeletal systems')
    parser.add_argument('--opt', help="muscle_driven or torque_driven")
    parser.add_argument('--model_path', help='Path to the .osim file')
    parser.add_argument('--ik_path', help='Path to the IK')
    parser.add_argument('--external_function', help='Path to the IK')
    parser.add_argument('--config', help='Path to the config file')
    parser.add_argument('--kinematic_coupling', help='Path to the kinematic coupling config file')
    parser.add_argument('--output_dir', help='Where to save the results')
    parser.add_argument('--muscle_info', help='Path to the results of the polynomial fit')
    parser.add_argument('--grf_file', required=False, help='Path to GRF (.mot) file (optional)')

    args = parser.parse_args()

    opt = args.opt

    if opt == "muscle_driven":
        muscle_driven.run(
            model_path=args.model_path,
            ik_path=args.ik_path,
            external_func_path=args.external_function,
            config_filepath=args.config,
            kinematic_coupling_path=args.kinematic_coupling,
            output_dir=args.output_dir,
            muscle_info_path=args.muscle_info,
            grf_path=args.grf_file

        )





if __name__ == '__main__':
    main()