class FileDigger():
    def __init__(self,grav,temp,metal,grav_lo,grav_hi,temp_lo,temp_hi,metal_lo,metal_hi,interp_par):
        self.grav = grav
        self.temp = temp
        self.metal = metal
        self.interp_par = interp_par
        self.grav_lo = grav_lo
        self.grav_hi = grav_hi
        self.temp_lo = temp_lo
        self.temp_hi = temp_hi
        self.metal_lo = metal_lo
        self.metal_hi = metal_hi

        self.spec_ml_tl_gl,self.g_mltlgl,self.t_mltlgl = self.search_for_corner(self.metal_lo,self.temp_lo,self.grav_lo, "corner mltlgl","down","down")
        self.spec_ml_tl_gh,self.g_mltlgh,self.t_mltlgh = self.search_for_corner(self.metal_lo,self.temp_lo,self.grav_hi, "corner mltlgh","down","up")
        self.spec_ml_th_gl,self.g_mlthgl,self.t_mlthgl = self.search_for_corner(self.metal_lo,self.temp_hi,self.grav_lo, "corner mlthgl","up","down")
        self.spec_ml_th_gh,self.g_mlthgh,self.t_mlthgh = self.search_for_corner(self.metal_lo,self.temp_hi,self.grav_hi, "corner mlthgh","up","up")
        self.spec_mh_tl_gl,self.g_mhtlgl,self.t_mhtlgl = self.search_for_corner(self.metal_hi,self.temp_lo,self.grav_lo, "corner mhtlgl","down","down")
        self.spec_mh_tl_gh,self.g_mhtlgh,self.t_mhtlgh = self.search_for_corner(self.metal_hi,self.temp_lo,self.grav_hi, "corner mhtlgh","down","up")
        self.spec_mh_th_gl,self.g_mhthgl,self.t_mhthgl = self.search_for_corner(self.metal_hi,self.temp_hi,self.grav_lo, "corner mhthgl","up","down")
        self.spec_mh_th_gh,self.g_mhthgh,self.t_mhthgh = self.search_for_corner(self.metal_hi,self.temp_hi,self.grav_hi, "corner mhthgh","up","up")


    def search_for_corner(self,metal_in,temp_in,grav_in,indicator,swim_dir_t,swim_dir_g):
        from astropy.io import fits
        from calculations.strfunc import grav_out_str,temp_out_str,metal_out_str
        #print("searching {}, swimming {} in temp and {} in grav".format(indicator,swim_dir_t,swim_dir_g))

        temp_swimming = True
        grav_swimming = True
        i = 0
        j = 0

        while temp_swimming is True:

            if temp_swimming is True and swim_dir_t == "up":
                try:
                    with fits.open("fits_library/ck{}/ck{}_{}.fits".format(metal_out_str(metal_in), metal_out_str(metal_in),temp_out_str(temp_in+i))) as hdul:
                        #print("Found temp after swimming up {} miles in temp".format(i/250))
                        temp_out = temp_in+i
                        temp_swimming = False
                        while grav_swimming is True:
                            if grav_swimming is True and swim_dir_g == "up":
                                try:
                                    spectrum = hdul[1].data["{}".format(grav_out_str(grav_in+j))]
                                    #print("Found grav after swimming {} miles in grav".format(j/0.5))
                                    grav_out = grav_in+j
                                    grav_swimming = False
                                except:
                                    pass
                            if grav_swimming is True and swim_dir_g == "down":
                                try:
                                    spectrum = hdul[1].data["{}".format(grav_out_str(grav_in-j))]
                                    #print("Found grav after swimming {} miles in grav".format(j/0.5))
                                    grav_out = grav_in-j
                                    grav_swimming = False
                                except:
                                    pass
                            j+=0.5
                except:
                    pass

            if temp_swimming is True and swim_dir_t == "down":
                try:
                    with fits.open("fits_library/ck{}/ck{}_{}.fits".format(metal_out_str(metal_in), metal_out_str(metal_in),temp_out_str(temp_in-i))) as hdul:
                        #print("Found temp after swimming down {} miles in temp".format(i/250))
                        temp_out = temp_in-i
                        temp_swimming = False
                        while grav_swimming is True:
                            if grav_swimming is True and swim_dir_g == "up":
                                try:
                                    spectrum = hdul[1].data["{}".format(grav_out_str(grav_in+j))]
                                    #print("Found grav after swimming {} miles in grav".format(j/0.5))
                                    grav_out = grav_in+j
                                    grav_swimming = False
                                except:
                                    pass
                            if grav_swimming is True and swim_dir_g == "down":
                                try:
                                    spectrum = hdul[1].data["{}".format(grav_out_str(grav_in-j))]
                                    #print("Found grav after swimming {} miles in grav".format(j/0.5))
                                    grav_out = grav_in-j
                                    grav_swimming = False
                                except:
                                    pass
                            j+=0.5
                except:
                    pass

            i += 250

        return spectrum,grav_out,temp_out


    def get_new_gtcorners(self):

        if self.g_mltlgl == self.g_mlthgl == self.g_mhtlgl == self.g_mhthgl and self.g_mltlgh == self.g_mlthgh == self.g_mhtlgh == self.g_mhthgh:
            self.grav_lo_N = self.g_mltlgl
            self.grav_hi_N = self.g_mltlgh
        else:
            print("inconsistent grav bounds")
            quit()

        if self.t_mltlgl == self.t_mltlgh == self.t_mhtlgl == self.t_mhtlgh and self.t_mlthgl == self.t_mlthgh == self.t_mhthgl == self.t_mhthgh:
            self.temp_lo_N = self.t_mltlgl
            self.temp_hi_N = self.t_mlthgl
        else:
            print("inconsistent temp bounds")
            quit()

    def build_swim_dict(self):
        self.swim_dict = {"{},{},{}".format(self.grav_lo,self.temp_lo,self.metal_lo):"{},{},{}".format(self.grav_lo_N,self.temp_lo_N,self.metal_lo),
                    "{},{},{}".format(self.grav_hi,self.temp_lo,self.metal_lo):"{},{},{}".format(self.grav_hi_N,self.temp_lo_N,self.metal_lo),
                    "{},{},{}".format(self.grav_lo,self.temp_hi,self.metal_lo):"{},{},{}".format(self.grav_lo_N,self.temp_hi_N,self.metal_lo),
                    "{},{},{}".format(self.grav_hi,self.temp_hi,self.metal_lo):"{},{},{}".format(self.grav_hi_N,self.temp_hi_N,self.metal_lo),
                    "{},{},{}".format(self.grav_lo,self.temp_lo,self.metal_hi):"{},{},{}".format(self.grav_lo_N,self.temp_lo_N,self.metal_hi),
                    "{},{},{}".format(self.grav_hi,self.temp_lo,self.metal_hi):"{},{},{}".format(self.grav_hi_N,self.temp_lo_N,self.metal_hi),
                    "{},{},{}".format(self.grav_lo,self.temp_hi,self.metal_hi):"{},{},{}".format(self.grav_lo_N,self.temp_hi_N,self.metal_hi),
                    "{},{},{}".format(self.grav_hi,self.temp_hi,self.metal_hi):"{},{},{}".format(self.grav_hi_N,self.temp_hi_N,self.metal_hi)}