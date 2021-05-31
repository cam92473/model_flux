class ExtinctionFunctions():
    def __init__(self,c1,c2,c4,c5,x0,c3,gamma,O3,O2,O1,k_IR,R_V):

        self.c1 = c1
        self.c2 = c2
        self.c4 = c4
        self.c5 = c5
        self.x0 = x0
        self.c3 = c3
        self.gamma = gamma
        self.O3 = O3
        self.O2 = O2
        self.O1 = O1
        self.k_IR = k_IR
        self.R_V = R_V

    def func_D(self,x):
        return x**2/((x**2-self.x0**2)**2+x**2*self.gamma**2)

    def ir_model(self,x):
        return self.k_IR * x ** 1.84 - self.R_V

    def opt_model(self,x):
        import numpy as np
        from scipy.interpolate import CubicSpline
        xopt = np.array([1, 1.8083, 2.5, 3.0303, 3.7037])
        yopt = np.array([self.ir_model(1), self.O3, self.O2, self.O1, self.uv_lng_model(3.7037)])
        cs = CubicSpline(xopt, yopt, bc_type='natural')
        return cs(x)

    def uv_lng_model(self,x):
        return self.c1+self.c2*x+self.c3*self.func_D(x)

    def uv_srt_model(self,x):
        return self.c1+self.c2*x+self.c3*self.func_D(x)+self.c4*(x-self.c5)**2
