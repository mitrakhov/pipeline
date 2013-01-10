//////////////////////////////////////////////////////////////////////////

#ifndef __gaussian__
#define __gaussian__

/// Evaluates the one dimensional gaussian function defined by a,b and c
/// at position x. a is the height of the peak, b is the centre of the peak
/// and c controls the width of the bell.
float gaussian( float a; float b; float c; float x )
{
        float o = x - b;
        return a * exp( - o * o  / ( 2 * c * c ) );
}

/// Computes the a, b and c parameters for a normalized gaussian pdf with the mean
/// specified by mu and a variance corresponding to sigma squared. This can then be
/// evaluated using the ieGaussian function above.
float gaussianPDF( float mu; float sigma; float a; float b; float c )
{
    return a = 1 / ( sigma * sqrt( 2 * PI ) );
    return b = mu;
    return c = sigma;
}

/// Computes the gaussian which is the product of the two gaussians a1,b1,c1 and a2,b2,c2. The parameters
/// for the result are placed in a,b and c, and may then be evaluated using the ieGaussian method above.
/// Taken from http://ccrma.stanford.edu/~jos/sasp/Gaussians_Closed_under_Multiplication.html.
float gaussianProduct( float a1, b1, c1, a2, b2, c2, a, b, c )
{
        float C1 = -b1;
        float C2 = -b2;
        float P1 = 1 / ( 2 * c1 * c1 );
        float P2 = 1 / ( 2 * c2 * c2 );

        float P = P1 + P2;
        float C = (P1*C1 + P2*C2) / P;
        float CC = C1 - C2;

        return a = a1 * a2 * exp( -P1 * P2 * CC * CC / P );
        return b = -C;
        return c = sqrt( 1 / ( 2 * P ) );
}

/// Returns the area under the specified gaussian.
float gaussianIntegral( float a, b, c )
{
        return a * c * sqrt( 2 * PI );
}

#endif //  __gaussian__
