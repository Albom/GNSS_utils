
import math

class ELLIPSE:
	A = 6378137.0
	B = 6356752.3141403561
	E2 = 0.00669438002290069

def xyz(lat, long, height):
	lat *= math.pi/180.0
	long *= math.pi/180.0
	n = ELLIPSE.A / math.sqrt(1 - ELLIPSE.E2*math.sin(lat)**2)
	x = (n + height) * math.cos(lat) * math.cos(long)
	y = (n + height) * math.cos(lat) * math.sin(long)
	z = ((1 - ELLIPSE.E2)*n + height ) * math.sin(lat)
	return {'x':x, 'y':y, 'z':z}

def geo(x, y, z):
	eps = 1e-4
	if (math.fabs(x)<eps) & (math.fabs(y)<eps):
		lat = math.copysign(math.pi/2, z)
		long = 0
		height = math.fabs(z)-ELLIPSE.B
	else:
		p = math.hypot(x, y)
		long = 2*math.atan2(y, x+p)
		lat = math.atan(z/(p*(1-ELLIPSE.E2)))
		height = 0
		while True:
			prev = height
			n = ELLIPSE.A / math.sqrt(1 - ELLIPSE.E2*math.sin(lat)**2)
			height = p/math.cos(lat) - n
			lat = math.atan(z/(p*(1-ELLIPSE.E2*n/(n-height))))
			if math.fabs(height-prev)<eps:
				break

		return {'lat':lat/math.pi*180, 'long':long/math.pi*180, 'height':height}
