import numpy as np
from sph_to_cart import sph_to_cart
from cart_to_sph import cart_to_sph
from rotation import rotation_matrix
from pole_utils import pole_from_plane

def great_circle(strike, dip):
	'''
	GreatCircle computes the great circle path of a plane in NED coordinate system

	pole_trd, pole_plg - pole of the plane

	Python function translated from the Matlab function
	GreatCircle in Allmendinger et al. (2012)
	'''
	pole_trd, pole_plg = pole_from_plane(strike, dip)
	pole_n, pole_e, pole_d = sph_to_cart(pole_trd, pole_plg)

	# This vector will trace great circle from South to North pole
	v = np.array(sph_to_cart(strike, 0.0))

	n = 181 # number of angles from 0 to 180
	NED = np.zeros((3, n))

	# To make the great circle, rotate the North vector 180 degrees
	# in increments of 1 degree
	for i in range(0, n):
		rad = np.radians(i)
		R = rotation_matrix(pole_n, pole_e, pole_d, rad)
		NED[:, i] = np.dot(R, v) # write result to ith column of the NED matrix

	# there could be vectors with negative plunge due to impresice calcualtions
	# have a look at an example https://github.com/rzaitov/compGeo/blob/master/source/notebooks/Unstable_Rotate.ipynb
	mask = NED[2,:] < 0
	NED[2, mask] = 0

	return cart_to_sph(NED[0, :], NED[1, :], NED[2, :])