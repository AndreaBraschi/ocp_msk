$trial_id = "P05R0002"
$model_path = "C:\Users\ab3758\Documents\PhD\msk\P5\scaled_model_rot.osim"
$ik_path = "C:\Users\ab3758\Documents\PhD\msk\P5\ik\${trial_id}\${trial_id}_ik.mot"
$dll_path = "C:\Users\ab3758\Documents\projects\ocp_msk\dlls\P05\build\RelWithDebInfo\P05.dll"
$config_filepath = "C:\Users\ab3758\Documents\projects\ocp_msk\configs\tackling\config_rot.json"
$kinematic_coupling_path = "C:\Users\ab3758\Documents\projects\ocp_msk\configs\tackling\kinematic_coupling_config.json"
$output_dir = "C:\Users\ab3758\Documents\PhD\msk\P5\opt\py"
$grf_path = "C:\Users\ab3758\Documents\PhD\msk\P5\grf\${trial_id}.mot"
$muscle_info_path = "C:\Users\ab3758\Documents\projects\ocp_msk\assets\muscle_poly_info.pkl"


ocpy --opt "muscle_driven" `
--model_path $model_path `
--ik_path $ik_path `
--external_function $dll_path `
--config $config_filepath `
--kinematic_coupling $kinematic_coupling_path `
--output_dir $output_dir `
--muscle_info $muscle_info_path `
--grf_file $grf_path
