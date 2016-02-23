// 2013 Sunpower Corp.
// Confidential & Proprietary
// Do Not Distribute

// include C Standard Library headers
#include <math.h>
#include <string.h>
#include <stdio.h>

// include solpos header
// contains documentation, function and structure prototypes, enumerations and
// other definitions and macros
#include "solpos00.h"

// define a macro for __declspec(dllexport) keyword instead of .def file
#ifdef WIN32
#define DllExport   __declspec( dllexport )
#else
#define DllExport
#endif

// solposAM
// Inputs:
//      location: (float*) [longitude, latitude, UTC-timezone]
//      datetime: (int*) [year, month, day, hour, minute, second]
//      weather: (float*) [ambient-pressure (mBar), ambient-temperature (C)]
// Outputs:
//      angles: (float*) [refracted-zenith, azimuth]
//      airmass: (float*) [airmass (atmos), pressure-adjusted-airmass (atmos)]
//      settings: (int*): [daynum, interval]
//      orientation: (float*) [tilt, aspect] (degrees)
//      shadowband: (float*): [width, radiation, sky]
DllExport long solposAM( float *location, int *datetime, float *weather,
    float *angles, float *airmass, int *settings, float *orientation,
    float *shadowband )
{
    
    /* variable declarations */
    struct posdata pd, *pdat; /* declare a posdata struct and a pointer for
                               * it (if desired, the structure could be
                               * allocated dynamically with malloc) */
    long retval;              /* to capture S_solpos return codes */
    
    /**************  Begin Program **************/
    
    pdat = &pd; /* point to the structure for convenience */
    
    /* Initialize structure to default values. (Optional only if ALL input
     * parameters are initialized in the calling code, which they are not
     * in this example.) */
    S_init(pdat);
    
    // output solar azimuth, refracted zenith and air mass
    // set month and day input instead of day-of-year number 
    pdat->function = ( (S_SOLAZM  | S_REFRAC | S_AMASS) & ~S_DOY );
    
    // location
    pdat->latitude  = location[0]; //   35.56836; // degrees
    pdat->longitude = location[1]; // -119.2022;  // degrees
    pdat->timezone  = location[2]; //   -8.0;     // UTC
    
    // weather
    pdat->press     = weather[0]; //1015.62055; // mbar
    pdat->temp      = weather[1]; //40.0; // deg C
    
    // set horizontal surface
    pdat->tilt      = 0;
    pdat->aspect    = 180;
    
    // date time
    // using ~S_DOY so it will calculate the day of year for me
    pdat->year      = datetime[0];
    pdat->month     = datetime[1];
    pdat->day       = datetime[2];
    pdat->hour      = datetime[3];
    pdat->minute    = datetime[4];
    pdat->second    = datetime[5];
    
    /* call the computational routine */
    retval = S_solpos(pdat);  /* S_solpos function call */
    
    // Errors are decoded by SOLPOS_Error
    // S_decode(retval, pdat);   /* ALWAYS look at the return code! */
    
    /* outputs */
    angles[0]  = pdat->zenref; // refracted zenith [degrees]
    angles[1]  = pdat->azim; // azimuth [degrees]

    airmass[0] = pdat->amass; // air mass [atmos]
    airmass[1] = pdat->ampress; // pressure adjusted air mass [atmos]
    
    settings[0] = pdat->daynum;
    settings[1] = pdat->interval;
    
    orientation[0] = pdat->tilt;
    orientation[1] = pdat->aspect;
    
    shadowband[0] = pdat->sbwid;
    shadowband[1] = pdat->sbrad;
    shadowband[2] = pdat->sbsky;

    return retval;

}
