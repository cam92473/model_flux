
def grav_out_str(grav_in):
    return "g" + str(grav_in).replace(".", "")

def metal_out_str(metal_in):
    if metal_in == 0:
        return "p00"
    elif str(metal_in).find("-") != -1:
        return str(metal_in).replace(".", "").replace("-", "m")
    else:
        return "p"+str(metal_in).replace(".", "")

def temp_out_str(temp_in):
    return str(int(temp_in))