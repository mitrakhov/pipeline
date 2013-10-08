def fit(val, oldmin, oldmax, newmin, newmax):
	return newmin + (val - oldmin) * (newmax - newmin)/(oldmax - oldmin)

def fit01(val, minval, maxval):
	return (val - minval)/(maxval - minval)
	
def fitfrom01(val, minval, maxval):
	return minval + val * (maxval - minval)
	
def mix(val0, val1, bias):
	return( 1.0 - bias) * val0 + bias*val1
	
def clamp(val, minval = 0.0, maxval = 1.0):
	if val > maxval:
		return maxval
	if val < minval:
		return minval