from calculations.search import FileDigger

class Interpolator(FileDigger):
    def __init__(self,grav,temp,metal,grav_lo,grav_hi,temp_lo,temp_hi,metal_lo,metal_hi,interp_par):
        super(Interpolator,self).__init__(grav,temp,metal,grav_lo,grav_hi,temp_lo,temp_hi,metal_lo,metal_hi,interp_par)
        self.get_new_gtcorners()

    def interpolate(self):
        import xarray as xr
        import numpy as np
        import scipy

        spectra_array = np.array([self.spec_ml_tl_gl,self.spec_ml_tl_gh,self.spec_ml_th_gl,self.spec_ml_th_gh,self.spec_mh_tl_gl,self.spec_mh_tl_gh,self.spec_mh_th_gl,self.spec_mh_th_gh])
        wc = spectra_array.T
        self.final_wave_list=[]

        for i in range(wc.shape[0]):
            cubedata = np.array([[[wc[i][0],wc[i][1]],[wc[i][2],wc[i][3]]],[[wc[i][4],wc[i][5]],[wc[i][6],wc[i][7]]]])
            da = xr.DataArray(cubedata,[("abundance_ratio", [self.metal_lo,self.metal_hi]),("temperature", [self.temp_lo_N,self.temp_hi_N]),
                                        ("log_of_surface_gravity", [self.grav_lo_N,self.grav_hi_N])])

            interpolated = da.interp(abundance_ratio = self.metal, temperature = self.temp, log_of_surface_gravity = self.grav, method = self.interp_par)
            self.final_wave_list.append(float(interpolated.data))
