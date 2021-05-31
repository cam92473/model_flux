
def get_corners(grav,temp,metal,interp):
    import math

    if grav%0.5 != 0 and grav != 5:
        grav_lo = math.floor(2*grav)/2
        grav_hi = math.ceil(2*grav)/2
    elif grav%0.5 == 0 and grav != 5:
        grav_lo = grav
        grav_hi = grav+0.5
    elif grav == 5:
        grav_lo = 4.5
        grav_hi = 5

    if metal < 0:
        if metal % 0.5 != 0:
            metal_lo = math.floor(2 * metal) / 2
            metal_hi = math.ceil(2 * metal) / 2
        elif metal % 0.5 == 0:
            metal_lo = metal
            metal_hi = metal + 0.5
    elif metal >= 0 and metal < 0.2:
        metal_lo = 0
        metal_hi = 0.2
    elif metal >= 0.2 and metal <= 0.5:
        metal_lo = 0.2
        metal_hi = 0.5

    if temp%250 != 0 and temp != 50000:
        temp_lo = math.floor(4 / 1000 * temp) / 4 * 1000
        temp_hi = math.ceil(4 / 1000 * temp) / 4 * 1000
    elif temp%250 == 0 and temp != 50000:
        temp_lo = temp
        temp_hi = temp+250
    elif temp == 50000:
        temp_lo = 47500
        temp_hi = 50000

    if interp == "            Linear          ":
        interp_par = "linear"
    elif interp == "Nearest neighbour":
        interp_par = "nearest"

    return grav_lo,grav_hi,temp_lo,temp_hi,metal_lo,metal_hi,interp_par

