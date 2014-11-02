#include <stdio.h>
#include "aacgmlib_v2.h"

int main(void)
{
double lat,lon,hgt;
double mlat,mlon,r;
double mlt,mslong;
int geo;
int err;
int year, month, day, hour, minute, second;

/* compute AACGM lat/lon with no time specified */
lat = 45.5;
lon = -23.5;
hgt = 1135.;
geo = 0;
err = AACGM_v2_Convert(lat,lon,hgt, &mlat,&mlon, &r, geo);
if (err == 0) {
	printf("lat = %lf, lon = %lf, height = %lf\n", lat,lon,hgt);
	printf("mlat = %lf, mlon = %lf, r = %lf\n", mlat,mlon,r);
	printf("\n\n");
}

year   = 2014;
month  = 3;
day    = 22;
hour   = 3;
minute = 11;
second = 0;
printf("Setting time to : %04d%02d%02d %02d%02d:%02d\n",
					year, month, day, hour, minute, second);

/* set date and time */
AACGM_v2_SetDateTime(year, month, day, hour, minute, second);

/* compute AACGM lat/lon */
err = AACGM_v2_Convert(lat,lon,hgt, &mlat,&mlon, &r, geo);
err = AACGM_v2_ConvertMLT(mlon,hgt,&mlt,&mslong);

printf("lat = %lf, lon = %lf, height = %lf\n", lat,lon,hgt);
printf("mlat = %lf, mlon = %lf, r = %lf\n", mlat,mlon,r);
printf("mlt = %lf, mslong = %lf\n",mlt,mslong);
//printf("%lf %lf\n", fyear, fyear_old);
printf("\n\n");

/* pick a different year */
year   = 1997;
printf("Setting time to : %04d%02d%02d %02d%02d:%02d\n",
					year, month, day, hour, minute, second);
AACGM_v2_SetDateTime(year, month, day, hour, minute, second);

err = AACGM_v2_Convert(lat,lon,hgt, &mlat,&mlon, &r, geo);
err = AACGM_v2_ConvertMLT(mlon,hgt,&mlt,&mslong);

printf("lat = %lf, lon = %lf, height = %lf\n", lat,lon,hgt);
printf("mlat = %lf, mlon = %lf, r = %lf\n", mlat,mlon,r);
printf("mlt = %lf, mslong = %lf\n",mlt,mslong);
//printf("%lf %lf\n", fyear, fyear_old);
printf("\n\n");

/* pick a different lat/lon; should not need to do any interpolations */
lat = 65.5;
lon = 93.5;
err = AACGM_v2_Convert(lat,lon,hgt, &mlat,&mlon, &r, geo);
err = AACGM_v2_ConvertMLT(mlon,hgt,&mlt,&mslong);

printf("lat = %lf, lon = %lf, height = %lf\n", lat,lon,hgt);
printf("mlat = %lf, mlon = %lf, r = %lf\n", mlat,mlon,r);
printf("mlt = %lf, mslong = %lf\n",mlt,mslong);
//printf("%lf %lf\n", fyear, fyear_old);
printf("\n\n");

/* pick a different height; should only need to do height interpolation */
hgt = 0.;
err = AACGM_v2_Convert(lat,lon,hgt, &mlat,&mlon, &r, geo);
err = AACGM_v2_ConvertMLT(mlon,hgt,&mlt,&mslong);

printf("lat = %lf, lon = %lf, height = %lf\n", lat,lon,hgt);
printf("mlat = %lf, mlon = %lf, r = %lf\n", mlat,mlon,r);
printf("mlt = %lf, mslong = %lf\n",mlt,mslong);
printf("\n\n");

/* do another lat/lon; no interpolations */
lat = 75.5;
lon = 73.5;
err = AACGM_v2_Convert(lat,lon,hgt, &mlat,&mlon, &r, geo);
err = AACGM_v2_ConvertMLT(mlon,hgt,&mlt,&mslong);

printf("lat = %lf, lon = %lf, height = %lf\n", lat,lon,hgt);
printf("mlat = %lf, mlon = %lf, r = %lf\n", mlat,mlon,r);
printf("mlt = %lf, mslong = %lf\n",mlt,mslong);
printf("\n\n");

/* pick another year; should require loading new coeffs and both interps */
year   = 2004;
month  = 3;
day    = 22;
hour   = 3;
minute = 11;
second = 0;
printf("Setting time to : %04d%02d%02d %02d%02d:%02d\n",
					year, month, day, hour, minute, second);

AACGM_v2_SetDateTime(year, month, day, hour, minute, second);

err = AACGM_v2_Convert(lat,lon,hgt, &mlat,&mlon, &r, geo);
err = AACGM_v2_ConvertMLT(mlon,hgt,&mlt,&mslong);

printf("lat = %lf, lon = %lf, height = %lf\n", lat,lon,hgt);
printf("mlat = %lf, mlon = %lf, r = %lf\n", mlat,mlon,r);
printf("mlt = %lf, mslong = %lf\n",mlt,mslong);
printf("\n\n");
}
