/*============================================================================
*
*    NAME:  spectrl2.h
*
*    Contains:
*        int S_spectral2 ()
*
*        INPUTS:
*            alpha      DEFAULT 1.14, power on Angstrom turbidity
*            aspect     DEFAULT 180.0 (South; N=0, E=90, W=270),
*                            aspect (azimuth angle) of collector panel.
*            assym      DEFAULT 0.65, aerosol assymetry factor
*            ozone      DEFAULT -1.0 will force an internal calculation;
*                            ozone amount (atmospheric cm)
*            spcrfl[6]  DEFAULT 0.2 (all), ground reflectivities
*            spcwvr[6]  DEFAULT { 0.3, 0.7, 0.8, 1.3, 2.5, 4.0 }
*                            wavelength regions (microns) for reflectivities
*            tau500     DEFAULT -1.0 (missing);
*                            aerosol optical depth at 0.5 microns, base e
*            tilt       DEFAULT 0.0, tilt angle of collector panel;
*                            if tilt > 180.0, sun-tracking is assumed.
*            units      Output units:
*                            1 = irradiance (W/sq m/micron) 
*                                  per wavelength (microns)
*                            2 = photon flux (10.0E+16 /sq cm/s/micron) 
*                                  per wavelength (microns)
*                            3 = photon flux density (10.0E+16 /sq cm/s/eV)
*                                  per energy (eV)
*            watvap     DEFAULT -1.0 (missing);
*                            precipitable water vapor (cm)
*   
*        OUTPUTS:    
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
*         "solpos.c" must be linked as well as "spectrl2.c", and its inputs
*         must be satisfied as well (see its documentation).
*
*    Martin Rymes
*    National Renewable Energy Laboratory
*    21 April 1998
*----------------------------------------------------------------------------
*
* Modifications:
* -------------
*
*	17 March 2004: Variables put into structure.
*
*		Steve Wilcox
*		Mary Anderberg
*		National Renewable Energy Laboratory
*
*----------------------------------------------------------------------------*/

struct specdattype
{
	/***** ALPHABETICAL LIST OF COMMON VARIABLES *****/
	                              /* Each comment begins with a 1-column letter code:
	                                 I:  INPUT variable
	                                 O:  OUTPUT variable
	/***** INTEGERS *****/

	int   units;         /* I:  Output units:
	                                       1 = irradiance (W/sq m/micron) 
	                                             per wavelength (microns)
	                                       2 = photon flux (10.0E+16 /sq cm/s/micron) 
	                                             per wavelength (microns)
	                                       3 = photon flux density (10.0E+16 /sq cm/s/eV)
	                                             per energy (eV)   */
	int   year;			/* I:  4-digit year */
	int   month;		/* I:  Month number (Jan = 1, Feb = 2, etc.) */
	int   day;			/* I:  Day of month (May 27 = 27, etc.) */
	int   hour;			/* I:  Hour of day, 0 - 23 */
	int   minute;		/* I:  Minute of hour, 0 - 59 */
	int	  second;		/* I:  Second of minute, 0 - 59 */

	/***** FLOATS *****/

	float alpha;         /* I:  Power on Angstrom turbidity,
	                                DEFAULT 1.14 */
	float aspect;   	 /* I:  Azimuth of panel surface (direction it
                                    faces) N=0, E=90, S=180, W=270 */
	float assym;         /* I:  Aerosol assymetry factor,
	                                DEFAULT 0.65 (rural assumed) */
	float latitude;		 /* I:  Latitude, degrees north (south negative) */
	float longitude;	 /* I:  Longitude, degrees east (west negative) */
	float ozone;         /* I:  Atmospheric ozone (cm); 
	                                -1.0 = let S_spectral2 calculate it */
	float press;     	 /* I:  Surface pressure, millibars */
	float specdif[122];  /* O:  Diffuse spectrum */
	float specdir[122];  /* O:  Direct spectrum */
	float specetr[122];  /* O:  Extraterrestrial spectrum */
	float specglo[122];  /* O:  Global spectrum */
	float spcrfl[6];     /* I:  Ground reflectivities,
	                                DEFAULT 0.2 (all) */
	float spcwvr[6];     /* I:  Reflectivity wavelengths,
	                                DEFAULT { 0.3, 0.7, 0.8, 1.3, 2.5, 4.0 ) */
	float specx[122];    /* O:  X-value (wavelength or frequency) of spectrum */
	float tau500;        /* I:  Aerosol optical depth at 0.5 microns, base e */
	float tilt;			 /* I:  Degrees tilt from horizontal of panel */
	float timezone;	     /* I:  Time zone, east (west negative). */
	float temp; 		 /* I:  Ambient dry-bulb temperature, degrees C */
	float watvap;        /* I:  Precipitable water vapor (cm) */
};

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
*        OUTPUTS:    
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
*         "solpos.c" must be linked as well as "spectrl2.c", and its inputs
*         must be satisfied as well (see its documentation).
*
*    Martin Rymes
*    National Renewable Energy Laboratory
*    21 April 1998
*----------------------------------------------------------------------------*/
extern int S_spectral2 (struct specdattype *specdat);
void S_spec_init(struct specdattype *specdat);
