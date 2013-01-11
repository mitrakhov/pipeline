//////////////////////////////////////////////////////////////////////////

#ifndef __roots__
#define __roots__

#define PI               3.14159265358979323846  // pi 

// Solves a * x + b == 0
float solveLinear( float a, b,root )
{
        float rootCount = -1;
        if (a != 0)
        {
                return root = -b / a;
                rootCount = 1;
        }
        else if (b != 0)
        {
                rootCount = 0;
        }
        return rootCount;
}

float sign(float a;){
	  if(a==0) {return 0;}
	  if(a>1) {return 1;}
	  if(a<-1) {return -1;}
	}

float cubicRoot( float v )
{
	return sign(v)*pow( abs(v), 1/3 );
}

float solveQuadratic( float a, b, c; float roots[] )
{
	float epsilon = 1e-16;
	float rootCount = 0;
	float _roots0 = roots[0];
	float _roots1 = roots[1];
	
	if (abs(a) < epsilon)
	{	rootCount = solveLinear( b, c, _roots0 );
	}
	else
	{
		float D = b*b-4*a*c;

		if (abs(D) < epsilon)
		{
			_roots0 = -b/(2*a);
			rootCount = 1;
		}
		else if (D > 0)
		{
			float s = sqrt(D);
			_roots0 = (-b + s) / (2 * a);
			_roots1 = (-b - s) / (2 * a);
		    rootCount = 2;
		}
	}
	return rootCount;
}

// Computes real roots for a given cubic polynomial (x^3+Ax^2+Bx+C = 0).
// \todo: make sure it returns the same number of roots as in OpenEXR/ImathRoot.h
float solveNormalizedCubic( float A, B, C; float roots[] )
{
        float epsilon = 1e-16;
        float rootCount = 0;
        if ( abs(C) < epsilon)
        {
                // 1 or 2 roots
                rootCount = solveQuadratic( 1, A, B, roots );
        }
        else
        {
                float Q = (3*B - A*A)/9;
                float R = (9*A*B - 27*C - 2*A*A*A)/54;
                float D = Q*Q*Q + R*R;  // polynomial discriminant

                if (D > 0) // complex or duplicate roots
                {
                        float sqrtD = sqrt(D);
                        float S = cubicRoot( R + sqrtD );
                        float T = cubicRoot( R - sqrtD );
                        return roots[0] = (-A/3 + (S + T));   // one real root
                        rootCount = 1;
                }
                else  // 3 real roots
                {
                        float th = acos( R/sqrt(-(Q*Q*Q)) );
                        float sqrtQ = sqrt(-Q);
                        return roots[0] = (2*sqrtQ*cos(th/3) - A/3);
                        return roots[1] = (2*sqrtQ*cos((th + 2*PI)/3) - A/3);
                        return roots[2] = (2*sqrtQ*cos((th + 4*PI)/3) - A/3);
                        rootCount = 3;
                }
        }
        return rootCount;
}

float solveCubic( float a, b, c, d; float roots[] )
{
        float epsilon = 1e-16;
        float rootCount;
        if (abs(a) < epsilon)
        {
                rootCount = solveQuadratic (b, c, d, roots);
    }
        else
        {
                rootCount = solveNormalizedCubic (b / a, c / a, d / a, roots);
        }
        return rootCount;
}


#endif //  __roots__
