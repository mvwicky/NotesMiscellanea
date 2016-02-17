def calc_rho(h, T=None):
	p_o = 101325 # Pa
	L = 0.0065 # K/m
	T_o = 288.15 # K
	R = 8.31447 # J/mol*K
	M = 0.0289644 # kg/mol
	g = 9.80665 # m/s^2
	if (T == None):
		T = T_o - L*h # temp at altitude h
	p = p_o * (1 - (L * h) / T_o)**((g*M)/(R*L)) # absolute pressure at altitude h
	rho = (p * M) / (R * T)
	return rho

def rho(h, T=None):
	if (T == None):
		T = 288.15 - 0.0065 * h 
	p = 101325 * (1 - (0.0065 * h) / 288.15)**((9.80665 * 0.0289644)/(8.31447 * 0.0065))
	return (p * 0.0289644) / (8.31447 * T)