/* File "spectrl2.c", defined below, runs NREL's simple spectral model. */
#include <math.h>
#include <string.h>
#include <stdio.h>

#include "solpos00.h"
#include "spectrl2_2.h"



/*============================================================================
*    S_spectral2     (NREL's simple spectral model)
*
*        Based on the SERI (now NREL) technical report SERI/TR-215-2436,
*        "Simple Solar Spectral Model for Direct and Diffuse Irradiance
*        on Horizontal and Tilted Planes at the Earth's Surface for 
*        Cloudless Atmospheres", by
*            R. Bird & C. Riordan
*
*        INPUTS:
*            alpha      DEFAULT 1.14, power on Angstrom turbidity
*            aspect     DEFAULT 180.0 (South; N=0, E=90, W=270),
*                            aspect (azimuth angle) of collector panel.
*            assym      DEFAULT 0.65, aerosol assymetry factor
*            day        Day of month (May 27 = 27, etc.) 
*            hour       Hour of day, 0 - 23
*            minute     Minute of hour, 0 - 59
*            month      Month number (Jan = 1, Feb = 2, etc.)
*            latitude   Latitude, degrees north (south negative)
*            longitude  Longitude, degrees east (west negative)
*            ozone      DEFAULT -1.0 will force an internal calculation;
*                            ozone amount (atmospheric cm)
*            press      Surface pressure, millibars
*            second     Second of minute, 0 - 59
*            spcrfl[6]  DEFAULT 0.2 (all), ground reflectivities
*            spcwvr[6]  DEFAULT { 0.3, 0.7, 0.8, 1.3, 2.5, 4.0 }
*                            wavelength regions (microns) for reflectivities
*            tau500     DEFAULT -1.0 (missing);
*                            aerosol optical depth at 0.5 microns, base e
*            tilt       DEFAULT 0.0, tilt angle of collector panel;
*                            if tilt < 0, sun-tracking is assumed. // MM 2012-01-20, change tilt < 0, same as solpos
*            timezone   Time zone, east (west negative)
*            temp       Ambient dry-bulb temperature, degrees C
*            units      Output units:
*                            1 = irradiance (W/sq m/micron) 
*                                  per wavelength (microns)
*                            2 = photon flux (10.0E+16 /sq cm/s/micron) 
*                                  per wavelength (microns)
*                            3 = photon flux density (10.0E+16 /sq cm/s/eV)
*                                  per energy (eV)
*            watvap     DEFAULT -1.0 (missing);
*                            precipitable water vapor (cm)
*            year       4-digit year
* 
*        OUTPUTS:    
*            specdif[122]    Diffuse spectrum on panel (see specdat->units)
*            specdir[122]    Direct normal spectrum (see specdat->units)
*            specetr[122]    Extraterrestrial spectrum (W/sq m/micron)
*            specglo[122]    Global spectrum on panel (see specdat->units)
*            specx[122]      X-coordinate (wavelength or energy; see specdat->units)
*
*    Usage:
*         In calling program, just after other 'includes', insert:
*
*              #include "spectrl2.h"
*
*         "solpos.c" must be linked as well as "spectrl2.c", and its inputs
*         must be satisfied as well (see its documentation).
*
*    Martin Rymes
*    National Renewable Energy Laboratory
*    21 April 1998
*----------------------------------------------------------------------------
* Modifications:
* -------------
*
*   18 March 2004: Variablesnow passed to functions through structure.
*
*       Steve Wilcox
*       Mary Anderberg
*       National Renewable Energy Laboratory
*----------------------------------------------------------------------------*/

int S_spectral2 (struct specdattype *specdat)
{
    /* This array contains the extraterrestrial spectrum and atmospheric 
       absorption coefficients at 122 wavelengths.  The first array range is
       defined as follows:
         0 = wavelength (microns)
         1 = extraterrestrial spectrum (W/sq m/micron)
         2 = water vapor absorption coefficient
         3 = ozone absorption coefficient
         4 = uniformly mixed gas "absorption coefficient"   */
    static float A[5][122] = { { 0.3, 0.305, 0.31, 0.315, 0.32, 0.325, 0.33, 0.335, 0.34,
      0.345, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47,
      0.48, 0.49, 0.5, 0.51, 0.52, 0.53, 0.54, 0.55, 0.57, 0.593, 0.61, 0.63, 0.656, 
      0.6676, 0.69, 0.71, 0.718, 0.7244, 0.74, 0.7525, 0.7575, 0.7625, 0.7675, 0.78, 0.8,
      0.816, 0.8237, 0.8315, 0.84, 0.86, 0.88, 0.905, 0.915, 0.925, 0.93, 0.937, 0.948,
      0.965, 0.98, 0.9935, 1.04, 1.07, 1.1, 1.12, 1.13, 1.145, 1.161, 1.17, 1.2, 1.24, 
      1.27, 1.29, 1.32, 1.35, 1.395, 1.4425, 1.4625, 1.477, 1.497, 1.52, 1.539, 1.558,
      1.578, 1.592, 1.61, 1.63, 1.646, 1.678, 1.74, 1.8, 1.86, 1.92, 1.96, 1.985, 2.005,
      2.035, 2.065, 2.1, 2.148, 2.198, 2.27, 2.36, 2.45, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 
      3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4.0 },
        { 535.9, 558.3, 622.0, 692.7, 715.1, 832.9, 961.9, 931.9, 900.6, 911.3, 975.5,
      975.9, 1119.9, 1103.8, 1033.8, 1479.1, 1701.3, 1740.4, 1587.2, 1837.0, 2005.0,
      2043.0, 1987.0, 2027.0, 1896.0, 1909.0, 1927.0, 1831.0, 1891.0, 1898.0, 1892.0,
      1840.0, 1768.0, 1728.0, 1658.0, 1524.0, 1531.0, 1420.0, 1399.0, 1374.0, 1373.0,
      1298.0, 1269.0, 1245.0, 1223.0, 1205.0, 1183.0, 1148.0, 1091.0, 1062.0, 1038.0,
      1022.0, 998.7, 947.2, 893.2, 868.2, 829.7, 830.3, 814.0, 786.9, 768.3, 767.0, 757.6,
      688.1, 640.7, 606.2, 585.9, 570.2, 564.1, 544.2, 533.4, 501.6, 477.5, 442.7, 440.0,
      416.8, 391.4, 358.9, 327.5, 317.5, 307.3, 300.4, 292.8, 275.5, 272.1, 259.3, 246.9,
      244.0, 243.5, 234.8, 220.5, 190.8, 171.1, 144.5, 135.7, 123.0, 123.8, 113.0, 108.5,
      97.5, 92.4, 82.4, 74.6, 68.3, 63.8, 49.5, 48.5, 38.6, 36.6, 32.0, 28.1, 24.8, 22.1,
      19.6, 17.5, 15.7, 14.1, 12.7, 11.5, 10.4, 9.5, 8.6 },
        { 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
      0.075, 0.0, 0.0, 0.0, 0.0, 0.016, 0.0125, 1.8, 2.5, 0.061, 0.0008, 0.0001, 0.00001,
      0.00001, 0.0006, 0.036, 1.6, 2.5, 0.5, 0.155, 0.00001, 0.0026, 7.0, 5.0, 5.0, 27.0,
      55.0, 45.0, 4.0, 1.48, 0.1, 0.00001, 0.001, 3.2, 115.0, 70.0, 75.0, 10.0, 5.0, 2.0,
      0.002, 0.002, 0.1, 4.0, 200.0, 1000.0, 185.0, 80.0, 80.0, 12.0, 0.16, 0.002, 0.0005,
      0.0001, 0.00001, 0.0001, 0.001, 0.01, 0.036, 1.1, 130.0, 1000.0, 500.0, 100.0, 4.0,
      2.9, 1.0, 0.4, 0.22, 0.25, 0.33, 0.5, 4.0, 80.0, 310.0, 15000.0, 22000.0, 8000.0,
      650.0, 240.0, 230.0, 100.0, 120.0, 19.5, 3.6, 3.1, 2.5, 1.4, 0.17, 0.0045 },
        { 10.0, 4.8, 2.7, 1.35, 0.8, 0.38, 0.16, 0.075, 0.04, 0.019, 0.007, 0.0, 0.0, 0.0,
      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.003, 0.006, 0.009, 0.01400, 0.021, 0.03, 0.04,
      0.048, 0.063, 0.075, 0.085, 0.12, 0.119, 0.12, 0.09, 0.065, 0.051, 0.028, 0.018,
      0.015, 0.012, 0.01, 0.008, 0.007, 0.006, 0.005, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
      0.0 },
        { 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
      0.0, 0.0, 0.0, 0.0, 0.15, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 4.0, 0.35, 0.0, 0.0, 0.0,
      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.05, 0.3, 0.02, 0.0002, 0.00011, 0.00001, 0.05,
      0.011, 0.005, 0.0006, 0.0, 0.005, 0.13, 0.04, 0.06, 0.13, 0.001, 0.0014, 0.0001,
      0.00001, 0.00001, 0.0001, 0.001, 4.3, 0.2, 21.0, 0.13, 1.0, 0.08, 0.001, 0.00038,
      0.001, 0.0005, 0.00015, 0.00014, 0.00066, 100.0, 150.0, 0.13, 0.0095, 0.001, 0.8,
      1.9, 1.3, 0.075, 0.01, 0.00195, 0.004, 0.29, 0.025 } };
    static float wv[6];    /* Temporary wavelength array */
    static float rf[6];    /* Temporary reflectivity array */

    static float afs;      /* Equation 3-12 */
    static float alg;      /* Equation 3-14 */
    static float Am;       /* Abbrev. for soldat->amass */
    static float Amo;      /* Abbrev. for ozone amount */
    static float Amp;      /* Abbrev. for soldat->ampress */
    static float Ao;       /* Abbrev. for ozone adjustment */
    static float Au;       /* Abbrev. for uniformly mixed gases */
    static float Aw;       /* Abbrev. for water vapor adjustment */
    static float bfs;      /* Equation 3-13 */
    static float c      =  2.9979244e14;  /* Used to calculate photon flux */ 
    static float c1, c2, c3, c4, c5, c6;  /* general coefficients */
    static float ci;       /* cosine of incidence angle */
    static float cons   =  5.0340365e14;  /* Used to calculate photon flux */ 
    static float ct;       /* cosine of specdat->tilt */
    static float cz;       /* cosine of the zenith angle */
    static float daer;     /* Equation 3-6, aerosol acattering component */
    static float dir;      /* temporary direct normal energy value */
    static float dif;      /* temporary diffuse energy value */
    static float dray;     /* Equation 3-5, Rayleigh scattering component */
    static float drgd;     /* Equation 3-7, multiple reflection, ground & air */
    static float dtot;     /* temporary total energy value */
    static float e;        /* energy in electron volts */
    static float evolt  =  1.6021891e-19; /* Joules per electron-volt */
    static float fs;       /* Equation 3-11 */
    static float fsp;      /* Fs[prime], Equation 3-15 */
    static float h      =  6.6261762e-34; /* Used to calculate photon flux */ 
    static float H0;       /* Abbrev. for horizontal extraterrestrial spectrum */
    static float omeg   =  0.945;         /* Single scattering albedo, 0.4 microns */
    static float omegl;    /* Equation 3-16; omega-lamda; single-scattering albedo */
    static float omegp  =  0.095;         /* Wavelength variation factor */
    static float O3;       /* Abbrev. for ozone */
    static float ozone;    /* ozone amount */
    static float raddeg;   /* radians-to-degrees conversion */
    static float rho;      /* interpolated specdat->spcrfl for specific wavelength */
    static float rhoa;     /* Equation 3-8; sky reflectivity */
    static float s1, s2, s3;    /* sine coefficients */
    static float Ta, Taa, Taap, Tas, Tasp, To, Tr, Trp, Tu, Tup, Tw, Twp;  
                           /* Transmissivities */
    static float W;        /* Abbrev. for soldat->S_watvap */
    static float wvl;      /* Abbrev. for wavelength number */
                    
    static int  track;    /* tracking/fixed tilt switch */
    static int   nr;       /* indicates the wavelength range */
    static int   i;              /* Loop counter */
    static int   false  = 0;     /* 0 is false */
    static int   true   = 1;     /* non-0 is true */
    static int   retval;    /* solpos return code */
    
    /* set up the solpos structure */
    struct posdata sdat, *soldat;
    
    /* point to the posdata structure and initialize it */
    soldat = &sdat;
    S_init(soldat);
    
    /* set solpos for month, day, year (turns off day of year convention) */
    soldat->function &= ~S_DOY;

    soldat->year        = specdat->year;
    soldat->month       = specdat->month;
    soldat->day         = specdat->day;
    soldat->hour        = specdat->hour;
    soldat->minute      = specdat->minute;
    soldat->second      = specdat->second;
    soldat->latitude    = specdat->latitude;
    soldat->longitude   = specdat->longitude;
    soldat->timezone    = specdat->timezone;
    soldat->tilt        = specdat->tilt;
    soldat->aspect      = specdat->aspect;
        
    /* Check for silly inputs */
    // don't print to stdout, raise SPECTRL2_Error
    // change return values to -1, -2, -3 and -4
    if ( specdat->units > 3 || specdat->units < 1 ) {
        //printf ( "*** S_spectral2 -> units should be 1 to 3, not %d\n", specdat->units );
        return ( -1 );
    }
    if ( specdat->tau500 > 10.0 || specdat->tau500 < 0.0 ) {
        //printf ( "*** S_spectral2 -> tau500 should not be %f\n", specdat->tau500 );
        return ( -2 );
    }
    if ( specdat->watvap > 100.0 || specdat->watvap < 0.0 ) {
        //printf ( "*** S_spectral2 -> watvap should not be %f\n", specdat->watvap );
        return ( -3 );
    }
    if ( specdat->assym >= 1.0 || specdat->assym <= 0.0 ) {
        //printf ( "*** S_spectral2 -> assym should not be %f\n", specdat->assym );
        return ( -4 );
    }
    
    /* Define constants. */
    e        = h * c / evolt;
    raddeg   = 180.0 / acos ( -1.0 );
        
    /* Angles of incidence and tilt angles must be preset */
    track  = false;
    if ( soldat->tilt < 0 ) // MM 2012-01-20, change tilt < 0, same as solpos
        track    = true;
    
    /* Find the sun */
    if ((retval = S_solpos (soldat )) != 0)
        // raises SOLPOS_Error
        //S_decode(retval, soldat);
        return retval;

    ci       = soldat->cosinc;
    if ( track ) {
        specdat->tilt  = soldat->zenref;
        ci      = 1.0;
    }
        
    ct       = cos ( soldat->tilt / raddeg );
    cz       = cos ( soldat->zenref / raddeg );
    
    /* Initialize defaults */
    if ( specdat->alpha < 0 ) 
        specdat->alpha = 1.14;
    
    if ( specdat->spcrfl[0] < 0.0 )  {
        specdat->spcwvr[0]  = 0.3;
        specdat->spcwvr[1]  = 0.7;
        specdat->spcwvr[2]  = 0.8;
        specdat->spcwvr[3]  = 1.3;
        specdat->spcwvr[4]  = 2.5;
        specdat->spcwvr[5]  = 4.0;
        specdat->spcrfl[0]  = 0.2;
        specdat->spcrfl[1]  = 0.2;
        specdat->spcrfl[2]  = 0.2;
        specdat->spcrfl[3]  = 0.2;
        specdat->spcrfl[4]  = 0.2;
        specdat->spcrfl[5]  = 0.2;
    }
    
    for ( i = 0; i < 6; ++i ) {
        wv[i]  = specdat->spcwvr[i];
        rf[i]  = specdat->spcrfl[i];
    }

    /* I cannot find the reference for this calculation of atmospheric ozone.
       If this makes you nervous, please enter your own soldat->ozone value. */
    if ( specdat->ozone < 0 ) {
        if ( soldat->latitude >= 0 ) {
            c1  =  150.0;
            c2  =    1.28;
            c3  =   40.0;
            c4  =  -30.0;
            c5  =    3.0;
            c6  =    0.0;

            if ( soldat->longitude > 0. )
                c6  =   20.0;
        }
        else {
            c1  =  100.0;
            c2  =    1.5;
            c3  =   30.0;
            c4  =  152.625;
            c5  =    2.0;
            c6  =  -75.0;
        }
  
        s1      = sin ( 0.9865 * ( soldat->daynum + c4 ) / raddeg );
        s2      = sin ( c5 * ( soldat->longitude + c6 ) / raddeg );
        s3      = sin ( c2 * soldat->latitude / raddeg );

        O3     = 0.235 + ( c1 + c3 * s1 + 20.0 * s2 ) * pow (s3,2) / 1000.0;
    }
    else 
        O3     = specdat->ozone;
        
    /* Equation 3-14 */
    alg   = log ( 1.0 - specdat->assym );

    /* Equation 3-12 */
    afs   = alg * ( 1.459 + alg * ( 0.1595 + alg * 0.4129 ) ); 

    /* Equation 3-13 */
    bfs   = alg * ( 0.0783 + alg * ( -0.3824 - alg * 0.5874 ) );

    /* Equation 3-15 */
    fsp   = 1.0 - 0.5 * exp ( ( afs + bfs / 1.8 ) / 1.8 );

    /* Equation 3-11 */
    fs       = 1.0 - 0.5 * exp ( ( afs + bfs * cz ) * cz ); 
        
    /* Ozone mass */
    Amo   = 1.003454 / sqrt ( pow(cz,2) + 0.006908 );

    /* Abbreviations of common variables */
    Am  = soldat->amass;
    Amp = soldat->ampress;
    W   = specdat->watvap;
    
    /* Current wavelength range */
    nr  = 1;
    
    /* MAIN LOOP:  step through the wavelengths */
    for ( i = 0; i < 122; ++i ) {
        /* Input variables */
        wvl = A[0][i];
        H0  = A[1][i];
        Aw  = A[2][i];
        Ao  = A[3][i];
        Au  = A[4][i];

        /* ETR spectrum */
        H0          *= soldat->erv;
        specdat->specetr[i] = H0;

        /* Equation 3-16 */
        omegl = omeg * exp ( -omegp * pow ( log (wvl/0.4), 2 ) );

        /* Equation 2-7 */
        c1    = specdat->tau500 * pow ( wvl*2.0, -specdat->alpha );

        /* Advance to the next wavelength range? */
        if ( wvl > wv[nr] )
            ++nr;

        /* Equation 2-4 */
        Tr    = exp ( -Amp / ( pow (wvl,4) * ( 115.6406 - 1.3366 / pow (wvl,2) ) ) );

        /* Equation 2-9 */
        To    = exp ( -Ao * O3 * Amo );

        /* Equation 2-8 */
        Tw    = exp ( -0.2385*Aw*W*Am / pow ( (1.0 + 20.07*Aw*W*Am), 0.45 ) );

        /* Equation 2-11 */
        Tu    = exp ( -1.41*Au*Amp / pow ( (1.0 + 118.3*Au*Amp), 0.45 ) );

        /* Equation 3-9 */
        Tas   = exp ( -omegl * c1 * Am );

        /* Equation 3-10 */
        Taa   = exp ( ( omegl - 1.0 ) * c1 * Am );

        /* Equation 2-6, sort of */
        Ta    = exp ( -c1 * Am );

        /* Equation 2-4; primed airmass M = 1.8 (Section 3.1) */
        Trp   = exp ( -1.8 / ( pow (wvl,4) * ( 115.6406 - 1.3366 / pow (wvl,2 ) ) ) );

        /* Equation 2-8; primed airmass M = 1.8 (Section 3.1) affects coefficients */
        Twp   = exp ( -0.4293*Aw*W / pow ( (1.0 + 36.126*Aw*W), 0.45 ) );

        /* Equation 2-11; primed airmass M = 1.8 (Section 3.1) affects coefficients */ 
        Tup   = exp ( -2.538*Au / pow ( (1.0 + 212.94*Au), 0.45 ) );

        /* Equation 3-9; primed airmass M = 1.8 (Section 3.1) */
        Tasp  = exp ( -omegl * c1 * 1.8 );

        /* Equation 3-10; primed airmass M = 1.8 (Section 3.1) */
        Taap  = exp ( ( omegl - 1.0 ) * c1 * 1.8 );

        /*........... Direct energy .............*/
        /* Temporary variable */
        c2    = H0 * To * Tw * Tu;

        /* Equation 2-1 */
        dir   = c2 * Tr * Ta;

        /*........... Diffuse energy .............*/
        /* Temporary variables */
        c2   *= cz * Taa;
        c3    = ( rf[nr] - rf[nr-1] ) / ( wv[nr] - wv[nr-1] );

        /* Equation 3-17; c4 = Cs */
        c4    = 1.0;
        if ( wvl <= 0.45 ) 
            c4   = pow ( (wvl + 0.55),1.8 );

        /* Equation 3-8 */
        rhoa  = Tup*Twp*Taap*( 0.5*(1.0-Trp) + (1.0-fsp)*Trp*(1.0-Tasp) );

        /* Interpolated ground reflectivity */
        rho   = c3 * ( wvl - wv[nr-1] ) + rf[nr-1];

        /* Equation 3-5 */
        dray  = c2 * ( 1.0 - pow ( Tr, 0.95 ) ) / 2.0;

        /* Equation 3-6 */
        daer  = c2 * pow (Tr,1.5) * ( 1.0 - Tas ) * fs;

        /* Equation 3-7 */
        drgd  = (dir*cz + dray + daer)*rho*rhoa/(1.0 - rho*rhoa);
    
        /* Equation 3-1 */
        dif   = ( dray + daer + drgd ) * c4;

        /*........... Global (total) energy .............*/
        dtot  = dir * cz + dif;

        /*........... Tilt energy, if applicable */
        if ( specdat->tilt > 1.0e-4 ) {
            /* Equation 3-18 without the first (direct-beam) term */
            c1      = dtot * rho * ( 1.0 - ct ) / 2.0;
            c2      = dir / H0;
            c3      = dif * c2 * ci / cz;
            c4      = dif * ( 1.0 - c2 ) * ( 1.0 + ct ) / 2.0;
            dif     = c1 + c3 + c4;

            /* Equation 3-18, including first term */
            dtot    = dir * ci + dif;
        }

        /* Adjust the output according to the units requested */
        if ( specdat->units == 1 ) {
            specdat->specx[i]      = wvl;
            specdat->specglo[i]    = dtot;
            specdat->specdir[i]    = dir;
            specdat->specdif[i]    = dif;
        }       
        else {
            c1  = wvl * cons;
            if ( specdat->units == 3 ) {
                specdat->specx[i]  = e / wvl;
                c1         *= wvl / specdat->specx[i];
            }
            else
                specdat->specx[i]  = wvl;

            specdat->specglo[i]    = dtot * c1;
            specdat->specdir[i]    = dir * c1;
            specdat->specdif[i]    = dif * c1;
        }
    }    
    return ( 0 );
}

/*============================================================================
*    S_spec_init     (initializes the data structure to conventional values)
*
*----------------------------------------------------------------------------*/

void S_spec_init(struct specdattype *specdat)
{
    float ini_spcrfl[6] = { 0.2, 0.2, 0.2, 0.2, 0.2, 0.2 };  /* Input reflectivities */
    float ini_spcwvr[6] = { 0.3, 0.7, 0.8, 1.3, 2.5, 4.0 };  /* Input reflectivity wavelengths */
    
    int i;

    specdat->alpha  = 1.14; /* Power on Angstrom turbidity */             
    specdat->assym  = 0.65; /* Aerosol assymetry factor (rural assumed) */
    specdat->ozone  = -1.0; /* Atmospheric ozone (cm);                    
                                   -1.0 = let S_spectral2 calculate it */ 
    specdat->tau500 = -1.0; /* Aerosol optical depth at 0.5 microns, base e */
    specdat->watvap = -1.0; /* Precipitable water vapor (cm) */               
    
    for (i = 0; i < 6; i++)
    {
        specdat->spcrfl[i]  = ini_spcrfl[i]; /* Input reflectivities */          
        specdat->spcwvr[i]  = ini_spcwvr[i]; /* Input reflectivity wavelengths */
    }
    
}
