/* function prototypes */

/* private functions */
int AACGM_v2_Rylm(double colat, double lon, int order, double *ylmval);
void AACGM_v2_Alt2CGM(double r_height_in, double r_lat_alt, double *r_lat_adj);
int AACGM_v2_CGM2Alt(double r_height_in, double r_lat_in, double *r_lat_adj);
double AACGM_v2_Sgn(double a, double b);
int convert_geo_coord(double lat_in, double lon_in, double height_in,
                      double *lat_out, double *lon_out, int flag, int order);
int dayno(int year, int month, int day, int *diy);
int AACGM_v2_LoadCoefFP(FILE *fp, int code);
int AACGM_v2_LoadCoef(char *fname, int code);
int AACGM_v2_LoadCoefs(int year);
double astmlt1(int t0,double solar_dec,double mlon,double height,double *mslon);
void msg_notime(void);

/* public functions */
int AACGM_v2_Convert(double in_lat, double in_lon, double height,
                  double *out_lat, double *out_lon, double *r, int flag);
int AACGM_v2_SetDateTime(int year, int month, int day,
                      int hour, int minute, int second);
int AACGM_v2_GetDateTime(int *year, int *month, int *day,
                      int *hour, int *minute, int *second, int *dayno);
int AACGM_v2_SetNow(void);
int AACGM_v2_ConvertMLT(double mlon, double height, double *mlt, double *mslong);
