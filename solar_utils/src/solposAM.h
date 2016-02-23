// solposAM function definition
//
// 2013 Sunpower Corp.
// Confidential & Proprietary
// Do Not Distribute

// define a macro for __declspec(dllexport) keyword instead of .def file
#ifdef WIN32
#define DllExport   __declspec( dllexport )
#else
#define DllExport
#endif

DllExport long solposAM( float *location, int *datetime, float *weather,
    float *angles, float *airmass, int *settings, float *orientation,
    float *shadowband );