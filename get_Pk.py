from LIM_b7 import *
from LIM_b7.fiducial_pars import astrocosmo_dict


save_dir = './results/nu_mass/' 
save_fig_dir = './PLOTS/nu_mass/' 

def run_pk(get_matter_pk,
           get_line_pk,
           get_velocity_pk,
           get_velocity_lim_pk,
           get_electron_lim_pk,
           model_data,
           survey,
           redshift,
           save_flag,
           plot_flag,
           plot_cross_corr_flag):

    if save_flag:
        create_dir('./results')
        create_dir('./PLOTS')
        create_dir(save_dir)
        create_dir(save_fig_dir)

    if plot_flag or plot_cross_corr_flag:
        plt.figure(figsize=(10,5))

    data = lambda developer, z:{**astrocosmo_dict(developer,z), **model_data}

    detector_params = lambda z, s: obs_params_lowz(z, s) if z < 4 else obs_params_highz(z, s)

    fid_model = update_Pkline(\
                detector_params(redshift, survey),\
                data(model_data['developer'],redshift))[0]

    k_fid = fid_model.k	

    if get_matter_pk:

        pk_m = fid_model.Pm[0]

        if save_flag:
            np.savetxt(save_dir + 'matter_pk',(k_fid.value,pk_m.value),header='k [Mpc-1], Pk [Mpc3]')

        if plot_flag:

            plt.loglog(k_fid, pk_m,
                       label=r'$\rm Dark Matter$')

    if get_line_pk:

        pk_line_clust = fid_model.Pk_clust
        pk_line = fid_model.Pk
        pk_line_monopole = fid_model.Pk_0

        if save_flag:
            np.savetxt(save_dir + 'line_pk',np.array((k_fid,pk_line_monopole)),header='k [Mpc-1], Pk_line_monopole [Mpc3]')

        if plot_flag:

            plt.loglog(k_fid,       
                       pk_line_monopole,
                       label=r'$\rm Line\, monopole$')
                       
    if get_velocity_pk:
    
        pk_velocity = fid_model.Pvv
        
        if save_flag:
            np.savetxt(save_dir + 'velocity_pk',np.array((k_fid,pk_velocity)),header='k [Mpc-1], Pk_velocity [Mpc3]')

        if plot_flag:

            plt.loglog(k_fid,       
                       pk_velocity,
                       label=r'$\rm Velocity$')
    
    if plot_flag:

        plt.xlabel(r'$k\,[{\rm Mpc^{-1}}]$',fontsize=20)
        plt.ylabel(r'$P(k,z =%g)\,[{\rm Mpc^{3}}]$'%round(redshift,2),fontsize=20)
        plt.legend(loc=3,fontsize=20)

        #plt.ylim(1e-10,1e4) 
        plt.ylim(1e-10,1e12)


        plt.tight_layout()
        plt.savefig(save_dir+'pk.png')
        plt.show()
        
    
    ### Cross correlations power spectra part
    if get_line_pk:

        pk_line_clust = fid_model.Pk_clust
        pk_line = fid_model.Pk
        pk_line_monopole = fid_model.Pk_0

        #if save_flag:
        #    np.savetxt(save_dir + 'line_pk',np.array((k_fid,pk_line_monopole)),header='k [Mpc-1], Pk_line_monopole [Mpc3]')

        if plot_cross_corr_flag:

            plt.loglog(k_fid,       
                       pk_line_monopole,
                       label=r'$\rm Line\, monopole$')
                       
                       
    if get_velocity_lim_pk:
    
        pk_lim_velocity_monopole = fid_model.Pkv_0
        
        if save_flag:
            np.savetxt(save_dir + 'velocity_lim_pk',np.array((k_fid,pk_lim_velocity_monopole)),header='k [Mpc-1], Pk_line_velocity P_xv [Mpc3]')

        if plot_cross_corr_flag:

            plt.loglog(k_fid,       
                       pk_lim_velocity_monopole,
                       label=r'$\rm Line\-Velocity\, P_{Xv}$')
                       
        
    if get_electron_lim_pk:
    
        pk_lim_electron_monopole = fid_model.Pke_0
                
        if save_flag:
            np.savetxt(save_dir + 'electron_lim_pk',np.array((k_fid,pk_lim_electron_monopole)),header='k [Mpc-1], Pk_line_electron P_xe [Mpc3]')

        if plot_cross_corr_flag:

            plt.loglog(k_fid,       
                       pk_lim_electron_monopole,
                       label=r'$\rm Line\-Electron\, P_{Xe}$')
                       
                       
    
    if plot_cross_corr_flag:
        
        plt.xlabel(r'$k\,[{\rm Mpc^{-1}}]$',fontsize=20)
        plt.ylabel(r'$P(k,z =%g)\,[{\rm Mpc^{3}}]$'%round(redshift,2),fontsize=20)
        plt.legend(loc=3,fontsize=20)

        #plt.xlim(1e-4,1e-1) 
        plt.ylim(1e-10,1e12) 

        plt.tight_layout()
        plt.savefig(save_dir+'pk_cross_corr.png')
        plt.show()
        

    return
