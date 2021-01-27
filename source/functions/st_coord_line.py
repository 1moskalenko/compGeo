import numpy as np
from zero_two_pi import zero_two_pi
from lower_hemisphere import lower_hemisphere

# Some constants
pi_4 = np.pi/4
sqrt_2 = np.sqrt(2)

## TODO: deprecated
def eq_angle_stereonet(trd, plg):
	trd, plg = lower_hemisphere(trd, plg)
	plg_2 = plg / 2

	# Equal angle stereonet, Eq. 3.6
	xp = np.tan(pi_4 - plg_2)*np.sin(trd)
	yp = np.tan(pi_4 - plg_2)*np.cos(trd)

	return xp, yp

def eq_angle_stereonet_transform(cn, ce, cd):
	return ce / (1 + cd), cn / (1 + cd)

def eq_area_stereonet(trd, plg):
	trd, plg = lower_hemisphere(trd, plg)
	plg_2 = plg / 2

	# Equal area stereonet, Eq. 3.7
	xp = sqrt_2*np.sin(pi_4 - plg_2)*np.sin(trd)
	yp = sqrt_2*np.sin(pi_4 - plg_2)*np.cos(trd)

	return xp, yp