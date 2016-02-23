/*============================================================================
*
*    NAME:  spectest.c
*
*    PURPOSE:  Exercises NREL's Simple Spectral model, 'spectrl2_2.c'.
*
*        Based on the SERI (now NREL) technical report SERI/TR-215-2436,
*        "Simple Solar Spectral Model for Direct and Diffuse Irradiance
*        on Horizontal and Tilted Planes at the Earth's Surface for 
*        Cloudless Atmospheres", by
*            R. Bird & C. Riordan
*
*    'spectrl2_2.c' contains:
*
*        int S_spectral (void)
*
*        INPUTS:
*            alpha      DEFAULT 1.14, power on Angstrom turbidity
*            aspect     DEFAULT 180.0 (South; N=0, E=90, W=270),
*                            aspect (azimuth angle) of collector panel.
*            assym      DEFAULT 0.65, aerosol assymetry factor
*			 day		Day of month (May 27 = 27, etc.) 
*			 hour		Hour of day, 0 - 23
*			 minute		Minute of hour, 0 - 59
*			 month		Month number (Jan = 1, Feb = 2, etc.)
*            latitude	Latitude, degrees north (south negative)
*            longitude	Longitude, degrees east (west negative)
*            ozone      DEFAULT -1.0 will force an internal calculation;
*                            ozone amount (atmospheric cm)
*            press		Surface pressure, millibars
*			 second		Second of minute, 0 - 59
*            spcrfl[6]  DEFAULT 0.2 (all), ground reflectivities
*            spcwvr[6]  DEFAULT { 0.3, 0.7, 0.8, 1.3, 2.5, 4.0 }
*                            wavelength regions (microns) for reflectivities
*            tau500     DEFAULT -1.0 (missing);
*                            aerosol optical depth at 0.5 microns, base e
*            tilt       DEFAULT 0.0, tilt angle of collector panel;
*                            if tilt > 180.0, sun-tracking is assumed.
*            timezone	Time zone, east (west negative)
*            temp		Ambient dry-bulb temperature, degrees C
*            units      Output units:
*                            1 = irradiance (W/sq m/micron) 
*                                  per wavelength (microns)
*                            2 = photon flux (10.0E+16 /sq cm/s/micron) 
*                                  per wavelength (microns)
*                            3 = photon flux density (10.0E+16 /sq cm/s/eV)
*                                  per energy (eV)
*            watvap     DEFAULT -1.0 (missing);
*                            precipitable water vapor (cm)
* 			 year		4-digit year
* 
*            specdif[122]    Diffuse spectrum on panel (see units)
*            specdir[122]    Direct normal spectrum (see units)
*            specetr[122]    Extraterrestrial spectrum (W/sq m/micron)
*            specglo[122]    Global spectrum on panel (see units)
*            specx[122]      X-coordinate (wavelength or energy; see units)
*
*    Usage:
*         In calling program, just after other 'includes', insert:
*
*              #include "spectrl2.h"
*
*         "solpos.c" must be linked as well as "spectrl2_2.c", and its inputs
*         must be satisfied as well (see its documentation).
*
*
*    Martin Rymes
*    National Renewable Energy Laboratory
*    25 March 1998
*----------------------------------------------------------------------------
*
* Modifications:
* -------------
*
*	18 March 2004: Variables now passed to functions through structure.
*
*		Steve Wilcox
*		Mary Anderberg
*		National Renewable Energy Laboratory
*
*----------------------------------------------------------------------------*/
#include <math.h>
#include <string.h>
#include <stdio.h>

#include "spectrl2_2.h"   /* <-- include for spectrl2.  */


int main ( )
{
	struct specdattype spdat, *specdat;  /* spectral2 data structure */
	
	/* point to the specral2 structure */
	specdat = &spdat;
	
	/* Initialize the data structure -- you can omit if ALL structure vaiables 
	   		are assigned elswhere. Defaults in initialization can be overridden by 
	   		reassigning below. */
	   
	S_spec_init (specdat);
    
    /* I use Atlanta, GA for this example */
    
    specdat->longitude = -84.43;  /* Note that latitude and longitude are  */
    specdat->latitude  =  33.65;  /*   in DECIMAL DEGREES, not Deg/Min/Sec */
    specdat->timezone  =  -5.0;   /* Eastern time zone, even though longitude would
                                		suggest Central.  We use what they use.
                                		DO NOT ADJUST FOR DAYLIGHT SAVINGS TIME. */

    /* The date is 22-July-2003 */
    
	specdat->year      = 1999;
    specdat->month     =    7;
    specdat->day       =   22;

    /* The time of day (STANDARD time) is 9:45:37 */

    specdat->hour      = 9;
    specdat->minute    = 45;
    specdat->second    = 37;

    /* Let's assume that the temperature is 27 degrees C and that
       the pressure is 1006 millibars.  The temperature is used for the
       atmospheric refraction correction, and the pressure is used for the
       refraction correction and the pressure-corrected airmass. */

    specdat->temp      =   27.0;
    specdat->press     = 1006.0;

    /* We will use the first set of units (energy vs wavelength) */
    
    specdat->units     = 1;
    
    /* Tau at 500 nm will be assumed to be 0.2, and we will assume 1.36 cm of
       atmospheric water vapor in a vertical column. */
       
    specdat->tau500    = 0.2;
    specdat->watvap    = 1.36;

    /* Finally, we will assume that you have a flat surface facing southeast,
       tilted at latitude. */

    specdat->tilt      = specdat->latitude;  /* Tilted at latitude */
    specdat->aspect	   = 135.0;       /* 135 deg. = SE */

    printf ( "\n" );
    printf ( "***** TEST S_spectral2: *****\n" );
    printf ( "\n" );
    
	S_spectral2 ( specdat );

    printf ( "Every tenth wavelength will be printed.\n" );
    printf ("\n" );
    printf ( "Note that your final decimal place values may vary\n" );
    printf ( "based on your computer's floating-point storage and your\n" );
    printf ( "compiler's mathematical algorithms.  If you agree with\n" );
    printf ( "NREL's values for at least 5 decimal places, assume it works.\n" );
    printf ("\n" );
    printf ( "micron  (NREL) ETRglo (NREL) global (NREL) direct (NREL) diffuse (NREL)\n" );
    printf ( "%6.3f  0.300 %6.1f  518.7 %6.1f    2.7 %6.1f    0.9 %6.1f    1.8\n",
        specdat->specx[  0], specdat->specetr[  0], specdat->specglo[  0], specdat->specdir[  0], specdat->specdif[  0] );
    printf ( "%6.3f  0.350 %6.1f  944.3 %6.1f  483.9 %6.1f  271.0 %6.1f  236.6\n",
        specdat->specx[ 10], specdat->specetr[ 10], specdat->specglo[ 10], specdat->specdir[ 10], specdat->specdif[ 10] );
    printf ( "%6.3f  0.450 %6.1f 1940.8 %6.1f 1446.4 %6.1f 1066.0 %6.1f  473.6\n",
        specdat->specx[ 20], specdat->specetr[ 20], specdat->specglo[ 20], specdat->specdir[ 20], specdat->specdif[ 20] );
    printf ( "%6.3f  0.550 %6.1f 1831.4 %6.1f 1457.9 %6.1f 1220.4 %6.1f  344.1\n",
        specdat->specx[ 30], specdat->specetr[ 30], specdat->specglo[ 30], specdat->specdir[ 30], specdat->specdif[ 30] );
    printf ( "%6.3f  0.724 %6.1f 1329.0 %6.1f  998.5 %6.1f  923.4 %6.1f  155.9\n",
        specdat->specx[ 40], specdat->specetr[ 40], specdat->specglo[ 40], specdat->specdir[ 40], specdat->specdif[ 40] );
    printf ( "%6.3f  0.831 %6.1f 1004.8 %6.1f  839.4 %6.1f  797.3 %6.1f  111.8\n",
        specdat->specx[ 50], specdat->specetr[ 50], specdat->specglo[ 50], specdat->specdir[ 50], specdat->specdif[ 50] );
    printf ( "%6.3f  0.965 %6.1f  743.7 %6.1f  550.7 %6.1f  538.3 %6.1f   59.6\n",
        specdat->specx[ 60], specdat->specetr[ 60], specdat->specglo[ 60], specdat->specdir[ 60], specdat->specdif[ 60] );
    printf ( "%6.3f  1.170 %6.1f  516.3 %6.1f  375.9 %6.1f  376.7 %6.1f   32.1\n",
        specdat->specx[ 70], specdat->specetr[ 70], specdat->specglo[ 70], specdat->specdir[ 70], specdat->specdif[ 70] );
    printf ( "%6.3f  1.477 %6.1f  297.5 %6.1f  101.6 %6.1f  104.8 %6.1f    6.0\n",
        specdat->specx[ 80], specdat->specetr[ 80], specdat->specglo[ 80], specdat->specdir[ 80], specdat->specdif[ 80] );
    printf ( "%6.3f  1.678 %6.1f  213.4 %6.1f  191.2 %6.1f  197.1 %6.1f   11.4\n",
        specdat->specx[ 90], specdat->specetr[ 90], specdat->specglo[ 90], specdat->specdir[ 90], specdat->specdif[ 90] );
    printf ( "%6.3f  2.100 %6.1f   89.4 %6.1f   74.8 %6.1f   78.2 %6.1f    3.5\n",
        specdat->specx[100], specdat->specetr[100], specdat->specglo[100], specdat->specdir[100], specdat->specdif[100] );
    printf ( "%6.3f  2.900 %6.1f   27.2 %6.1f    1.1 %6.1f    1.2 %6.1f    0.0\n",
        specdat->specx[110], specdat->specetr[110], specdat->specglo[110], specdat->specdir[110], specdat->specdif[110] );
    printf ( "%6.3f  3.900 %6.1f    9.2 %6.1f    7.4 %6.1f    7.9 %6.1f    0.2\n",
        specdat->specx[120], specdat->specetr[120], specdat->specglo[120], specdat->specdir[120], specdat->specdif[120] );

	return ( 0 );
}
