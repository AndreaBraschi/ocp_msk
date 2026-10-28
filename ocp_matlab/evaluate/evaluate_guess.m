function [GRFs_num, pelvis_res_num, eq_constr_num, mt_ft_num, mt_dm_num] =  evaluate_guess(opti, ...
    GRF_eval_all, pelvis_res_eval_all, mt_ft_all, mt_dm_all)

    GRFs_num = opti.debug.value(GRF_eval_all, opti.initial);
    pelvis_res_num = opti.debug.value(pelvis_res_eval_all, opti.initial);
    eq_constr_num = opti.debug.value(eq_constr_all, opti.initial);
    mt_ft_num = opti.debug.value(mt_ft_all, opti.initial);
    mt_dm_num = opti.debug.value(mt_dm_all, opti.initial);


end