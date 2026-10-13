$trial_id = ""
$model_path = ""
$ik_path = ""
$dll_path = ""
$config_filepath = ""
$kinematic_coupling_path = ""
$output_dir = ""
$grf_path = ""
$muscle_info_path = ""


ocpy --opt "muscle_driven" `
--model_path $model_path `
--ik_path $ik_path `
--external_function $dll_path `
--config $config_filepath `
--kinematic_coupling $kinematic_coupling_path `
--output_dir $output_dir `
--muscle_info $muscle_info_path `
--grf_file $grf_path
