"""
*******************************
MODULE: models.tsyganenko.trace
*******************************

This module contains the following functions:

  trace

This module contains the following classes:

  tsygTrace

*******************************
"""

class tsygTrace(object):
    def __init__(self, lat, lon, rho, coords='geo', datetime=None,
        vswgse=[-400.,0.,0.], pdyn=2., dst=-5., byimf=0., bzimf=-5.,
        lmax=5000, rmax=60., rmin=1., dsmax=0.01, err=0.000001):
        """
|   **PACKAGE**: models.tsyganenko.trace
|   **FUNCTION**: trace(lat, lon, rho, coords='geo', datetime=None,
|        vswgse=[-400.,0.,0.], Pdyn=2., Dst=-5., ByIMF=0., BzIMF=-5.
|        lmax=5000, rmax=60., rmin=1., dsmax=0.01, err=0.000001)
|   **PURPOSE**: trace magnetic field line(s) from point(s)
|
|   **INPUTS**:
|       **lat**: latitude [degrees]
|       **lon**: longitude [degrees]
|       **rho**: distance from center of the Earth [km]
|       **[coords]**: coordinates used for start point ['geo']
|       **[datetime]**: a python datetime object
|       **[vswgse]**: solar wind velocity in GSE coordinates [m/s, m/s, m/s]
|       **[pdyn]**: solar wind dynamic pressure [nPa]
|       **[dst]**: Dst index [nT]
|       **[byimf]**: IMF By [nT]
|       **[bzimf]**: IMF Bz [nT]
|       **[lmax]**: maximum number of points to trace
|       **[rmax]**: upper trace boundary in Re
|       **[rmin]**: lower trace boundary in Re
|       **[dsmax]**: maximum tracing step size
|       **[err]**: tracing step tolerance
|
|   **OUTPUTS**:
|       Elements of this object:
|       **.lat[N/S]H**: latitude of the trace footpoint in Northern/Southern hemispher
|       **.lon[N/S]H**: longitude of the trace footpoint in Northern/Southern hemispher
|       **.rho[N/S]H**: distance of the trace footpoint in Northern/Southern hemispher
|
|   **EXAMPLES**:
|       # trace a series of points
|       lats = range(10, 90, 10)
|       lons = zeros(len(lats))
|       rhos = 6372.*ones(len(lats))
|       trace = tsyganenko.tsygTrace(lats, lons, rhos)
|       # Print the results nicely
|       print trace
|       # Plot the traced field lines
|       ax = trace.plot()
|       # Or generate a 3d view of the traced field lines
|       ax = trace.plot3d()
|
|   Written by Sebastien 2012-10
        """
        self.lat = lat
        self.lon = lon
        self.rho = rho
        self.coords = coords
        self.datetime = datetime
        self.vswgse = vswgse
        self.pdyn = pdyn
        self.dst = dst
        self.byimf = byimf
        self.bzimf = bzimf
        iTest = self.__test_valid__()
        if not iTest: self.__del__()
        self.trace()


    def __test_valid__(self):
        """
|   Test the validity of input arguments to the tsygTrace class and trace method
|
|   Written by Sebastien 2012-10
        """
        assert (len(self.vswgse) == 3), 'vswgse must have 3 elements'
        assert (self.coords.lower() == 'geo'), '{}: this coordinae system is not supported'.format(self.coords.lower())
        # A provision for those who want to batch trace
        try:
            [l for l in self.lat]
        except:
            self.lat = [self.lat]
        try:
            [l for l in self.lon]
        except:
            self.lon = [self.lon]
        try:
            [r for r in self.rho]
        except:
            self.rho = [self.rho]
        # Make sure they're all the sam elength
        assert (len(self.lat) == len(self.lon) == len(self.rho)), 'lat, lon and rho must me the same length'
        
        return True


    def trace(self, lat=None, lon=None, rho=None, coords=None, datetime=None,
        vswgse=None, pdyn=None, dst=None, byimf=None, bzimf=None,
        lmax=5000, rmax=60., rmin=1., dsmax=0.01, err=0.000001):
        """
|   See tsygTrace for a description of each parameter
|   Any unspecified parameter default to the one stored in the object
|   Unspecified lmax, rmax, rmin, dsmax, err has a set default value
|
|   Written by Sebastien 2012-10
        """
        from models.tsyganenko import tsygFort
        from numpy import radians, degrees, zeros
        from datetime import datetime as pydt

        # Store existing values of class attributes in case something is wrong
        # and we need to revert back to them
        if lat: _lat = self.lat
        if lon: _lon = self.lon
        if rho: _rho = self.rho
        if coords: _coords = self.coords
        if vswgse: _vswgse = self.vswgse

        # Pass position if new
        if lat: self.lat = lat
        lat = self.lat
        if lon: self.lon = lon
        lon = self.lon
        if rho: self.rho = rho
        rho = self.rho

        # Set necessary parameters if new
        if coords: self.coords = coords
        coords = self.coords
        if datetime: self.datetime = datetime
        datetime = self.datetime
        if vswgse: self.vswgse = vswgse
        vswgse = self.vswgse
        if pdyn: self.pdyn = pdyn
        pdyn = self.pdyn
        if dst: self.dst = dst
        dst = self.dst
        if byimf: self.byimf = byimf
        byimf = self.byimf
        if bzimf: self.bzimf = bzimf
        bzimf = self.bzimf

        # Test that everything is in order, if not revert to existing values
        iTest = self.__test_valid__()
        if not iTest: 
            if lat: self.lat = _lat
            if lon: _self.lon = lon
            if rho: self.rho = _rho
            if coords: self.coords = _coords 
            if vswgse: self.vswgse = _vswgse

        # Declare the same Re as used in Tsyganenko models [km]
        Re = 6371.2
        
        # Initialize trace array
        self.l = zeros(len(lat))
        self.xTrace = zeros((len(lat),2*lmax))
        self.yTrace = self.xTrace.copy()
        self.zTrace = self.xTrace.copy()
        self.xGsw = []
        self.yGsw = []
        self.zGsw = []
        self.latNH = []
        self.lonNH = []
        self.rhoNH = []
        self.latSH = []
        self.lonSH = []
        self.rhoSH = []

        # If no datetime is provided, defaults to today
        if not datetime: datetime = pydt.utcnow()

        # This has to be called first
        tsygFort.recalc_08(datetime.year,datetime.timetuple().tm_yday,
                                datetime.hour,datetime.minute,datetime.second,
                                vswgse[0],vswgse[1],vswgse[2])

        # And now iterate through the desired points
        for ip in xrange(len(lat)):
            # Convert lat,lon to geographic cartesian and then gsw
            r, theta, phi, xgeo, ygeo, zgeo = tsygFort.sphcar_08(
                                                    rho[ip]/Re, radians(90.-lat[ip]), radians(lon[ip]),
                                                    0., 0., 0.,
                                                    1)
            if coords.lower() == 'geo':
                xgeo, ygeo, zgeo, xgsw, ygsw, zgsw = tsygFort.geogsw_08(
                                                            xgeo, ygeo, zgeo,
                                                            0. ,0. ,0. ,
                                                            1)
            self.xGsw.append(xgsw)
            self.yGsw.append(ygsw)
            self.zGsw.append(zgsw)

            # Trace field line
            inmod = 'IGRF_GSW_08'
            exmod = 'T96_01'
            parmod = [pdyn, dst, byimf, bzimf, 0, 0, 0, 0, 0, 0]
            # First towards southern hemisphere
            maptoL = [-1, 1]
            for mapto in maptoL:
                xfgsw, yfgsw, zfgsw, xarr, yarr, zarr, l = tsygFort.trace_08( xgsw, ygsw, zgsw,
                                                                mapto, dsmax, err, rmax, rmin, 0,
                                                                parmod, exmod, inmod,
                                                                lmax )

                # Convert back to spherical geographic coords
                xfgeo, yfgeo, zfgeo, xfgsw, yfgsw, zfgsw  = tsygFort.geogsw_08(
                                                                    0. ,0. ,0. ,
                                                                    xfgsw, yfgsw, zfgsw,
                                                                    -1)
                geoR, geoColat, geoLon, xgeo, ygeo, zgeo = tsygFort.sphcar_08(
                                                                    0., 0., 0.,
                                                                    xfgeo, yfgeo, zfgeo,
                                                                    -1)

                # Get coordinates of traced point
                if mapto == 1:
                    self.latSH.append( 90. - degrees(geoColat) )
                    self.lonSH.append( degrees(geoLon) )
                    self.rhoSH.append( geoR*Re )
                elif mapto == -1:
                    self.latNH.append( 90. - degrees(geoColat) )
                    self.lonNH.append( degrees(geoLon) )
                    self.rhoNH.append( geoR*Re )
                    
                # Store trace
                if mapto == -1:
                    self.xTrace[ip,0:l] = xarr[l-1::-1]
                    self.yTrace[ip,0:l] = yarr[l-1::-1]
                    self.zTrace[ip,0:l] = zarr[l-1::-1]
                elif mapto == 1:
                    self.xTrace[ip,self.l[ip]:self.l[ip]+l] = xarr[0:l]
                    self.yTrace[ip,self.l[ip]:self.l[ip]+l] = yarr[0:l]
                    self.zTrace[ip,self.l[ip]:self.l[ip]+l] = zarr[0:l]
                self.l[ip] += l

        # Resize trace output to more minimum possible length
        self.xTrace = self.xTrace[:,0:self.l.max()]
        self.yTrace = self.yTrace[:,0:self.l.max()]
        self.zTrace = self.zTrace[:,0:self.l.max()]


    def __str__(self):
        """
|   Print object information in a nice way
|
|   Written by Sebastien 2012-10
        """
        # Declare print format
        outstr =    '''
vswgse=[{:6.0f},{:6.0f},{:6.0f}]    [m/s]
pdyn={:3.0f}                        [nPa]
dst={:3.0f}                         [nT]
byimf={:3.0f}                       [nT]
bzimf={:3.0f}                       [nT]
                    '''.format(self.vswgse[0],
                               self.vswgse[1],
                               self.vswgse[2],
                               self.pdyn,
                               self.dst,
                               self.byimf,
                               self.bzimf)
        outstr += '\n(latitude [degrees], longitude [degrees], distance from center of the Earth [km])'

        # Print stuff
        for ip in xrange(len(self.lat)):
            outstr +=   '''
({:6.3f}, {:6.3f}, {:6.3f}) 
    --> NH({:6.3f}, {:6.3f}, {:6.3f})
    --> SH({:6.3f}, {:6.3f}, {:6.3f}) 
                        '''.format(self.lat[ip], self.lon[ip], self.rho[ip], 
                                   self.latNH[ip], self.lonNH[ip], self.rhoNH[ip], 
                                   self.latSH[ip], self.lonSH[ip], self.rhoSH[ip])

        return outstr


    def plot(self, proj='xz', color='b', showPts=False, 
        subplot=111, showEarth=True, disp=True, **kwargs):
        """
|   Generate a 2D plot of the trace projected onto a given plane
|   Graphic keywords apply to the plot method for the field lines
|   
|   **INPUTS**:
|       **plane**: the projection plane in GSW coordinates
|       **subplot**: subplot position
|       **showEarth**: Toggle Earth disk visibility on/off
|       **showPts**: Toggle start points visibility on/off
|       **disp**: invoke pylab.show()
|       **color**: field line color
|       **kwargs**: see matplotlib.axes.Axes.plot
|   
|   **OUTPUTS**:
|       **ax**: matplotlib axes object
|
|   Written by Sebastien 2012-10
        """
        from pylab import gcf, show
        from matplotlib.patches import Circle
        from numpy import pi, linspace, outer, ones, size, cos, sin, radians

        assert (len(proj) == 2) or \
            (proj[0] in ['x','y','z'] and proj[1] in ['x','y','z']) or \
            (proj[0] != proj[1]), 'Invalid projection plane'

        fig = gcf()
        ax = fig.add_subplot(subplot)
        ax.set_aspect('equal')

        # First plot a nice disk for the Earth
        if showEarth:
            circ = Circle(xy=(0,0), radius=1, facecolor='0.8', edgecolor='k', alpha=.5, zorder=-1)
            ax.add_patch(circ)

        # Then plot the traced field line
        for ip in xrange(len(self.lat)):
            # Select projection plane
            if proj[0] == 'x':
                xx = self.xTrace[ip,0:self.l[ip]]
                xpt = self.xGsw[ip]
                ax.set_xlabel(r'$X_{GSW}$')
            elif proj[0] == 'y':
                xx = self.yTrace[ip,0:self.l[ip]]
                xpt = self.yGsw[ip]
                ax.set_xlabel(r'$Y_{GSW}$')
            elif proj[0] == 'z':
                xx = self.zTrace[ip,0:self.l[ip]]
                xpt = self.zGsw[ip]
                ax.set_xlabel(r'$Z_{GSW}$')
            if proj[1] == 'x':
                yy = self.xTrace[ip,0:self.l[ip]]
                ypt = self.xGsw[ip]
                ax.set_ylabel(r'$X_{GSW}$')
            elif proj[1] == 'y':
                yy = self.yTrace[ip,0:self.l[ip]]
                ypt = self.yGsw[ip]
                ax.set_ylabel(r'$Y_{GSW}$')
            elif proj[1] == 'z':
                yy = self.zTrace[ip,0:self.l[ip]]
                ypt = self.zGsw[ip]
                ax.set_ylabel(r'$Z_{GSW}$')
            # Plot
            ax.plot(xx, yy, c=color, **kwargs)
            if showPts:
                ax.scatter(xpt, ypt, c='k')

        if disp: show()

        return ax


    def plot3d(self, subplot=111, showEarth=True, showPts=False, disp=True, 
        xyzlim=None, zorder=1, linewidth=2, color='b', **kwargs):
        """
|   Generate a 3D plot of the trace
|   Graphic keywords apply to the plot3d method for the field lines
|   
|   **INPUTS**:
|       **subplot**: subplot position
|       **showEarth**: Toggle Earth sphere visibility on/off
|       **showPts**: Toggle start points visibility on/off
|       **disp**: invoke pylab.show()
|       **xyzlim**: 3D axis limits
|       **zorder**: 3D layers ordering
|       **linewidth**: field line width
|       **color**: field line color
|       **kwargs**: see mpl_toolkits.mplot3d.axes3d.Axes3D.plot3D
|   
|   **OUTPUTS**:
|       **ax**: matplotlib axes object
|
|   Written by Sebastien 2012-10
        """
        from mpl_toolkits.mplot3d import proj3d
        from numpy import pi, linspace, outer, ones, size, cos, sin, radians
        from pylab import gcf, show

        fig = gcf()
        ax = fig.add_subplot(subplot, projection='3d')

        # First plot a nice sphere for the Earth
        if showEarth:
            u = linspace(0, 2 * pi, 179)
            v = linspace(0, pi, 179)
            tx = outer(cos(u), sin(v))
            ty = outer(sin(u), sin(v))
            tz = outer(ones(size(u)), cos(v))
            ax.plot_surface(tx,ty,tz,rstride=10, cstride=10, color='grey', alpha=.5, zorder=0, linewidth=0.5)

        # Then plot the traced field line
        for ip in xrange(len(self.lat)):
            ax.plot3D(  self.xTrace[ip,0:self.l[ip]],
                        self.yTrace[ip,0:self.l[ip]],
                        self.zTrace[ip,0:self.l[ip]], 
                        zorder=zorder, linewidth=linewidth, color=color, **kwargs)
            if showPts:
                ax.scatter3D(self.xGsw[ip], self.yGsw[ip], self.zGsw[ip], c='k')

        # Set plot limits
        if not xyzlim:
            xyzlim = max( [ ax.get_xlim3d().max(),
                         ax.get_ylim3d().max(),
                         ax.get_zlim3d().max(), ] )
        ax.set_xlim3d([-xyzlim,xyzlim])
        ax.set_ylim3d([-xyzlim,xyzlim])
        ax.set_zlim3d([-xyzlim,xyzlim])

        if disp: show()

        return ax