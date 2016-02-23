// 2013 Sunpower Corp.
// Confidential & Proprietary
// Do Not Distribute

// include C Standard Library headers
#include <math.h>
#include <string.h>
#include <stdio.h>

// include spectrl2 header
// contains documentation, function and structure prototypes, enumerations and
// other definitions and macros
#include "spectrl2_2.h"

// define a macro for __declspec(dllexport) keyword instead of .def file
#ifdef WIN32
#define DllExport   __declspec( dllexport )
#define DllImport   __declspec( dllimport )
#else
#define DllExport
#define DllImport
#endif

// import solposAM
DllImport long solposAM( float *location, int *datetime, float *weather,
    float *angles, float *airmass, int *settings, float *orientation,
    float *shadowband );

// spectrl2
// Inputs:
//      units: (int) output units: 1, 2 or 3
//      location: (float*) [longitude, latitude, UTC-timezone]
//      datetime: (int*) [year, month, day, hour, minute, second]
//      weather: (float*) [ambient-pressure (mBar), ambient-temperature (C)]
//      orientation: (float*) [tilt, aspect] (degrees)
//      atmosphericConditions: (float*) [alpha, assym, ozone, tau500, watvap]
//      albedo: (float**) [wavelength * 6], [reflectance * 6]  (optional)
// Outputs:
//      specdif: (float*) diffuse spectrum on panel
//      specdir: (float*) direct normal spectrum on panel
//      specetr: (float*) extraterrestrial spectrum
//      specglo: (float*) global spectrum on panel
//      specx: (float*) wavelength
//      angles: (float*) [refracted-zenith, azimuth]
//      airmass: (float*) [airmass (atmos), pressure-adjusted-airmass (atmos)]
//      settings: (int*): [daynum, interval]
//      shadowband: (float*): [width, radiation, sky]
DllExport long spectrl2( int units, float *location, int *datetime,
    float *weather, float *orientation, float *atmosphericConditions,
    float *albedo, float *specdif, float *specdir, float *specetr,
    float *specglo, float *specx, float *angles, float *airmass, int *settings, 
    float *shadowband )
{

    /* variable declarations */
    struct specdattype spdat, *specdat;  /* spectral2 data structure */
    static int   i;                      /* Loop counter */
    long retval;              /* to capture S_spectral2 return codes */

    /**************  Begin Program **************/

    /* point to the specral2 structure */
    specdat = &spdat;

    /* Initialize the data structure -- you can omit if ALL structure vaiables 
     * are assigned elswhere. Defaults in initialization can be overridden by 
     * reassigning below. */

    S_spec_init (specdat);

    /* I use Atlanta, GA for this example */

    specdat->latitude  = location[0]; //  33.65; // degrees
    specdat->longitude = location[1]; // -84.43; // degrees
    specdat->timezone  = location[2]; //  -5.0; // UTC

    /* Note that latitude and longitude are in DECIMAL DEGREES, not Deg/Min/Sec
     * Eastern time zone, even though longitude would suggest Central.
     * We use what they use. DO NOT ADJUST FOR DAYLIGHT SAVINGS TIME. */

    /* The date is 22-July-2003 */

    specdat->year      = datetime[0]; // 1999;
    specdat->month     = datetime[1]; //    7;
    specdat->day       = datetime[2]; //   22;

    /* The time of day (STANDARD time) is 9:45:37 */

    specdat->hour      = datetime[3]; // 9;
    specdat->minute    = datetime[4]; // 45;
    specdat->second    = datetime[5]; // 37;

    /* Let's assume that the temperature is 27 degrees C and that
     * the pressure is 1006 millibars.  The temperature is used for the
     * atmospheric refraction correction, and the pressure is used for the
     * refraction correction and the pressure-corrected airmass. */

    specdat->press     = weather[0]; // 1006.0; // mB
    specdat->temp      = weather[1]; //   27.0; // deg C

    /* We will use the first set of units (energy vs wavelength) */

    specdat->units     = units; // 1;

    /* Tau at 500 nm will be assumed to be 0.2, and we will assume 1.36 cm of
     * atmospheric water vapor in a vertical column. */

    specdat->alpha     = atmosphericConditions[0]; // 1.14;
    if (atmosphericConditions[1] != -1) {
        specdat->assym     = atmosphericConditions[1]; // 0.65;
    }
    specdat->ozone     = atmosphericConditions[2];
    specdat->tau500    = atmosphericConditions[3]; // 0.2;
    specdat->watvap    = atmosphericConditions[4]; // 1.36;

    if ((int)albedo[0] != -1) {
        specdat->spcwvr[0]  = albedo[0]; // 0.3;
        specdat->spcwvr[1]  = albedo[1]; // 0.7;
        specdat->spcwvr[2]  = albedo[2]; // 0.8;
        specdat->spcwvr[3]  = albedo[3]; // 1.3;
        specdat->spcwvr[4]  = albedo[4]; // 2.5;
        specdat->spcwvr[5]  = albedo[5]; // 4.0;
        specdat->spcrfl[0]  = albedo[6]; // 0.2;
        specdat->spcrfl[1]  = albedo[7]; // 0.2;
        specdat->spcrfl[2]  = albedo[8]; // 0.2;
        specdat->spcrfl[3]  = albedo[9]; // 0.2;
        specdat->spcrfl[4]  = albedo[10]; // 0.2;
        specdat->spcrfl[5]  = albedo[11]; // 0.2;
    }

    /* Finally, we will assume that you have a flat surface facing southeast,
       tilted at latitude. */

    specdat->tilt      = orientation[0]; // specdat->latitude;  /* Tilted at latitude */
    specdat->aspect    = orientation[1]; // 135.0;       /* 135 deg. = SE */

    /* call the computational routine */
    retval = S_spectral2 ( specdat );

    // fill in values for angles, airmass, settings and shadowband
    solposAM( location, datetime, weather, angles, airmass, settings,
        orientation, shadowband );

    /* output of MEX function */
    for ( i = 0; i < 122; ++i ) {
        specdif[i]     = specdat->specdif[i];
        specdir[i]     = specdat->specdir[i];
        specetr[i]     = specdat->specetr[i];
        specglo[i]     = specdat->specglo[i];
        specx[i]       = specdat->specx[i];
    }

    return retval;

}
