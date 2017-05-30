# Created by Alexandros Kazantzidis
# Date 25/05/17 (The basic statistical filtering was implemented in 26/05/17)

from math import *
from decimal import *
import numpy as np
import pandas as pd
pd.set_option('display.max_rows', 500)
np.set_printoptions(precision=16)




def atan3(a,b):
		
	# four quadrant inverse tangent

	# input

	#  a = sine of angle
	#  b = cosine of angle

	# output

	#  y = angle (radians 0 =< c <= 2 * pi)

	epsilon = 0.0000000001

	pidiv2 = 0.5 * pi

	if (abs(a) < epsilon):
		y = (1 - np.sign(b)) * pidiv2
		return y
	else:
		c = (2 - np.sign(a)) * pidiv2


	if (abs(b) < epsilon):
		y = c
		
	else:
		y = c + np.sign(a) * np.sign(b) * (abs(atan(a / b)) - pidiv2)
		
	return y

def state_kep(r,v):
	
	
	# convert eci state vector to six classical orbital
	# elements via equinoctial elements

	# input

	#  mu = central body gravitational constant (km**3/sec**2)
	#  r  = eci position vector (kilometers)
	#  v  = eci velocity vector (kilometers/second)

	# output

	#  oev(1) = semimajor axis (kilometers)
	#  oev(2) = orbital eccentricity (non-dimensional)
	#           (0 <= eccentricity < 1)
	#  oev(3) = orbital inclination (radians)
	#           (0 <= inclination <= pi)
	#  oev(4) = argument of perigee (radians)
	#           (0 <= argument of perigee <= 2 pi)
	#  oev(5) = right ascension of ascending node (radians)
	#           (0 <= raan <= 2 pi)
	#  oev(6) = true anomaly (radians)
	#           (0 <= true anomaly <= 2 pi)
	
	mu = 398600.4405

	pi2 = 2.0 * pi
	
# position and velocity magnitude

	rmag = np.linalg.norm(r)

	vmag = np.linalg.norm(v)

# position unit vector

	rhat = r[:] / rmag

# angular momentum vectors
	
	hv = np.cross(r, v)

	hhat = hv / np.linalg.norm(hv)

# eccentricity vector

	vtmp = v[:] / mu

	ecc = np.cross(vtmp, hv)

	ecc = ecc - rhat

# semimajor axis

	sma = 1.0 / (2.0 / rmag - vmag * vmag / mu)

	p = hhat[0] / (1.0 + hhat[2])

	q = -hhat[1] / (1.0 + hhat[2])

	const1 = 1.0 / (1.0 + p * p + q * q)
	
	fhat=np.array([1.0,2.0,3])
	fhat[0] = const1 * (1.0 - p * p + q * q)
	fhat[1] = const1 * 2.0 * p * q
	fhat[2] = -const1 * 2.0 * p
	
	
	
	
	ghat=np.array([1.0,2.0,3.0])
	ghat[0]=(const1 * 2.0 * p * q)
	ghat[1] = const1 * (1.0 + p * p - q * q)
	ghat[2] = const1 * 2.0 * q
	
	h = np.dot(ecc, ghat)
	
	xk = np.dot(ecc, fhat)

	x1 = np.dot(r, fhat)

	y1 = np.dot(r, ghat)

# orbital eccentricity
	
	eccm = sqrt((h * h + xk * xk))
	
# orbital inclination

	inc = 2.0 * atan(sqrt(p * p + q * q))

# true longitude

	xlambdat = atan3(y1, x1)

# check for equatorial orbit

	if (inc > 0.00000001):
		raan = atan3(p, q)
	else:
		raan = 0.0


# check for circular orbit

	if (eccm > 0.00000001):
		first=atan3(h,xk)-raan
		second=pi2
		firstint=int(first)
		secondint=int(second)
		argper = first - (secondint*(firstint/secondint))
		
	else:
		argper = 0.0


# true anomaly
	
	first = xlambdat - raan - argper
	second = pi2
	firstint=int(first)
	secondint=int(second)
	tanom = first - (secondint*(firstint/secondint))
	inc = degrees(inc)
	

# load orbital element vector
	oev = np.zeros((6,1))
	oev[0,0] = sma
	oev[1,0] = eccm
	oev[2,0] = inc
	oev[3,0] = argper
	oev[4,0] = raan
	oev[5,0] = tanom
	return oev
	

r = np.array([ 5.0756899358316559e+03,-4.5590381308371752e+03,  1.9322228177731663e+03])
v = np. array([ 1.3360847905126974e+00, -1.5698574946888049e+00, -7.2117328822023676e+00])

kep=state_kep(r,v)
print(kep)