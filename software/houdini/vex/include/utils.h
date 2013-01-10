//////////////////////////////////////////////////////////////////////////

#ifndef __utils__
#define __utils__

#include "voplib.h"


vector linear( vector input ){
    return pow(input, 1/0.45);
}

/*
float mod(float aa; float bb){
    float rem = aa % bb;
    if (rem < 0) rem += bb;
    return rem;
}
*/

vector hsvshift( vector input; float hueShift, satShift, valueShift){
	    
    if(abs(hueShift) + abs(satShift) + abs(valueShift) > 0 ){
	vector inputHSV = rgbtohsv(input);
	return hsvtorgb(inputHSV.x + hueShift, inputHSV.y + satShift, inputHSV.z + valueShift);
    }
    else return input;
    
}


vector smoothnoise(vector pos; float freq, cutoff, rolloff){
    vector smoothedNoise;
    setcomp(smoothedNoise, smooth( getcomp(noise(pos * freq), 0), cutoff, rolloff), 0);
    setcomp(smoothedNoise, smooth( getcomp(noise(pos * freq), 1), cutoff, rolloff), 1);
    setcomp(smoothedNoise, smooth( getcomp(noise(pos * freq), 2), cutoff, rolloff), 2);
    
    return fit(smoothedNoise, {0, 0, 0}, {1, 1, 1}, {-1, -1, -1}, {1, 1, 1} );
}

vector fitvector(vector input; float oldMin, oldMax, newMin, newMax;){
    return fit(input, set(oldMin, oldMin, oldMin), set(oldMax, oldMax, oldMax), set(newMin, newMin, newMin), set(newMax, newMax, newMax));
}
#endif //  __utils__
