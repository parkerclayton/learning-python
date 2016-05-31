import interrupts

cdef class Domain1D:
    def __cinit__(self, *args, **kwargs):
        self.domain = NULL

    # The signature of this function causes warnings for Sphinx documentation
    def __init__(self, _SolutionBase phase, *args, name=None, **kwargs):
        if self.domain is NULL:
            raise TypeError("Can't instantiate abstract class Domain1D.")

        if name is not None:
            self.name = name

        self.gas = phase
        self.have_user_tolerances = False

    property index:
        """
        Index of this domain in a stack. Returns -1 if this domain is not part
        of a stack.
        """
        def __get__(self):
            return self.domain.domainIndex()

    property n_components:
        """Number of solution components at each grid point."""
        def __get__(self):
            return self.domain.nComponents()

    property n_points:
        """Number of grid points belonging to this domain."""
        def __get__(self):
            return self.domain.nPoints()

    def component_name(self, int n):
        """Name of the nth component."""
        return pystr(self.domain.componentName(n))

    property component_names:
        """List of the names of all components of this domain."""
        def __get__(self):
            return [self.component_name(n) for n in range(self.n_components)]

    def component_index(self, str name):
        """Index of the component with name 'name'"""
        return self.domain.componentIndex(stringify(name))

    def set_bounds(self, *, default=None, Y=None, **kwargs):
        """
        Set the lower and upper bounds on the solution.

        The argument list should consist of keyword/value pairs, with
        component names as keywords and (lower_bound, upper_bound) tuples as
        the values.  The keyword *default* may be used to specify default
        bounds for all unspecified components. The keyword *Y* can be used to
        stand for all species mass fractions in flow domains.

        >>> d.set_bounds(default=(0, 1), Y=(-1.0e-5, 2.0))
        """
        if default is not None:
            for n in range(self.n_components):
                self.domain.setBounds(n, default[0], default[1])

        if Y is not None:
            k0 = self.component_index(self.gas.species_name(0))
            for n in range(k0, k0 + self.gas.n_species):
                self.domain.setBounds(n, Y[0], Y[1])

        for name,(lower,upper) in kwargs.items():
            self.domain.setBounds(self.component_index(name), lower, upper)

    def set_steady_tolerances(self, *, default=None, Y=None, abs=None, rel=None,
                              **kwargs):
        """
        Set the error tolerances for the steady-state problem.

        The argument list should consist of keyword/value pairs, with
        component names as keywords and (rtol, atol) tuples as the values.
        The keyword *default* may be used to specify default bounds for all
        unspecified components. The keyword *Y* can be used to stand for all
        species mass fractions in flow domains. Alternatively, the keywords
        *abs* and *rel* can be used to specify arrays for the absolute and
        relative tolerances for each solution component.
        """
        self.have_user_tolerances = True
        if default is not None:
            self.domain.setSteadyTolerances(default[0], default[1])

        if abs is not None and rel is not None:
            assert len(abs) == len(rel) == self.n_components
            for n,(r,a) in enumerate(zip(rel,abs)):
                self.domain.setSteadyTolerances(r,a,n)

        if Y is not None:
            k0 = self.component_index(self.gas.species_name(0))
            for n in range(k0, k0 + self.gas.n_species):
                self.domain.setSteadyTolerances(Y[0], Y[1], n)

        for name,(lower,upper) in kwargs.items():
            self.domain.setSteadyTolerances(lower, upper, self.component_index(name))

    def set_transient_tolerances(self, *, default=None, Y=None, abs=None,
                                 rel=None, **kwargs):
        """
        Set the error tolerances for the steady-state problem.

        The argument list should consist of keyword/value pairs, with
        component names as keywords and (rtol, atol) tuples as the values.
        The keyword *default* may be used to specify default bounds for all
        unspecified components. The keyword *Y* can be used to stand for all
        species mass fractions in flow domains. Alternatively, the keywords
        *abs* and *rel* can be used to specify arrays for the absolute and
        relative tolerances for each solution component.
        """
        self.have_user_tolerances = True
        if default is not None:
            self.domain.setTransientTolerances(default[0], default[1])

        if abs is not None and rel is not None:
            assert len(abs) == len(rel) == self.n_components
            for n,(r,a) in enumerate(zip(rel,abs)):
                self.domain.setTransientTolerances(r,a,n)

        if Y is not None:
            k0 = self.component_index(self.gas.species_name(0))
            for n in range(k0, k0 + self.gas.n_species):
                self.domain.setTransientTolerances(Y[0], Y[1], n)

        for name,(lower,upper) in kwargs.items():
            self.domain.setTransientTolerances(lower, upper, self.component_index(name))

    def bounds(self, component):
        """
        Return the (lower, upper) bounds for a solution component.

        >>> d.bounds('T')
        (200.0, 5000.0)
        """
        n = self.component_index(component)
        return self.domain.lowerBound(n), self.domain.upperBound(n)

    def tolerances(self, component):
        """
        Return the (relative, absolute) error tolerances for a solution
        component.

        >>> rtol, atol = d.tolerances('u')
        """
        k = self.component_index(component)
        return self.domain.rtol(k), self.domain.atol(k)

    def steady_reltol(self, component=None):
        """
        Return the relative error tolerance for the steady state problem for a
        specified solution component, or all components if none is specified.
        """
        if component is None:
            return np.array([self.domain.steady_rtol(n)
                             for n in range(self.n_components)])
        else:
            return self.domain.steady_rtol(self.component_index(component))

    def steady_abstol(self, component=None):
        """
        Return the absolute error tolerance for the steady state problem for a
        specified solution component, or all components if none is specified.
        """
        if component is None:
            return np.array([self.domain.steady_atol(n)
                             for n in range(self.n_components)])
        else:
            return self.domain.steady_atol(self.component_index(component))

    def transient_reltol(self, component=None):
        """
        Return the relative error tolerance for the transient problem for a
        specified solution component, or all components if none is specified.
        """
        if component is None:
            return np.array([self.domain.transient_rtol(n)
                             for n in range(self.n_components)])
        else:
            return self.domain.transient_rtol(self.component_index(component))

    def transient_abstol(self, component=None):
        """
        Return the absolute error tolerance for the transient problem for a
        specified solution component, or all components if none is specified.
        """
        if component is None:
            return np.array([self.domain.transient_atol(n)
                             for n in range(self.n_components)])
        else:
            return self.domain.transient_atol(self.component_index(component))

    property grid:
        """ The grid for this domain """
        def __get__(self):
            cdef np.ndarray[np.double_t, ndim=1] grid = np.empty(self.n_points)
            cdef int i
            for i in range(self.n_points):
                grid[i] = self.domain.grid(i)
            return grid

        def __set__(self, grid):
            cdef np.ndarray[np.double_t, ndim=1] data = \
                np.ascontiguousarray(grid, dtype=np.double)
            self.domain.setupGrid(len(data), &data[0])

    property name:
        """ The name / id of this domain """
        def __get__(self):
            return pystr(self.domain.id())
        def __set__(self, name):
            self.domain.setID(stringify(name))

    property description:
        """ A description of this domain """
        def __get__(self):
            return pystr(self.domain.desc())
        def __set__(self, desc):
            self.domain.setDesc(stringify(desc))

    def __reduce__(self):
        raise NotImplementedError('Domain1D object is not picklable')

    def __copy__(self):
        raise NotImplementedError('Domain1D object is not copyable')

cdef class Boundary1D(Domain1D):
    """
    Base class for boundary domains.

    :param phase:
        The (gas) phase corresponding to the adjacent flow domain
    """
    def __cinit__(self, *args, **kwargs):
        self.boundary = NULL

    # The signature of this function causes warnings for Sphinx documentation
    def __init__(self, *args, **kwargs):
        if self.boundary is NULL:
            raise TypeError("Can't instantiate abstract class Boundary1D.")
        self.domain = <CxxDomain1D*>(self.boundary)
        Domain1D.__init__(self, *args, **kwargs)

    property T:
        """ The temperature [K] at this boundary. """
        def __get__(self):
            return self.boundary.temperature()
        def __set__(self, T):
            self.boundary.setTemperature(T)

    property mdot:
        """ The mass flow rate per unit area [kg/m^2] """
        def __get__(self):
            return self.boundary.mdot()
        def __set__(self, mdot):
            self.boundary.setMdot(mdot)

    property X:
        """
        Species mole fractions at this boundary. May be set as either a string
        or as an array.
        """
        def __get__(self):
            self.gas.TPY = self.gas.T, self.gas.P, self.Y
            return self.gas.X

        def __set__(self, X):
            self.gas.TPX = None, None, X
            cdef np.ndarray[np.double_t, ndim=1] data = self.gas.X
            self.boundary.setMoleFractions(&data[0])

    property Y:
        """
        Species mass fractions at this boundary. May be set as either a string
        or as an array.
        """
        def __get__(self):
            cdef int nsp = self.boundary.nSpecies()
            cdef np.ndarray[np.double_t, ndim=1] Y = np.empty(nsp)
            cdef int k
            for k in range(nsp):
                Y[k] = self.boundary.massFraction(k)
            return Y

        def __set__(self, Y):
            self.gas.TPY = self.gas.T, self.gas.P, Y
            self.X = self.gas.X


cdef class Inlet1D(Boundary1D):
    """
    A one-dimensional inlet. Note that an inlet can only be a terminal
    domain - it must be either the leftmost or rightmost domain in a
    stack.
    """
    def __cinit__(self, *args, **kwargs):
        self.inlet = new CxxInlet1D()
        self.boundary = <CxxBdry1D*>(self.inlet)

    def __dealloc__(self):
        del self.inlet

    property spread_rate:
        """
        Get/set the tangential velocity gradient [1/s] at this boundary.
        """
        def __get__(self):
            return self.inlet.spreadRate()
        def __set__(self, s):
            self.inlet.setSpreadRate(s)


cdef class Outlet1D(Boundary1D):
    """
    A one-dimensional outlet. An outlet imposes a zero-gradient boundary
    condition on the flow.
    """
    def __cinit__(self, *args, **kwargs):
        self.outlet = new CxxOutlet1D()
        self.boundary = <CxxBdry1D*>(self.outlet)

    def __dealloc__(self):
        del self.outlet


cdef class OutletReservoir1D(Boundary1D):
    """
    A one-dimensional outlet into a reservoir.
    """
    def __cinit__(self, *args, **kwargs):
        self.outlet = new CxxOutletRes1D()
        self.boundary = <CxxBdry1D*>(self.outlet)

    def __dealloc__(self):
        del self.outlet


cdef class SymmetryPlane1D(Boundary1D):
    """A symmetry plane."""
    def __cinit__(self, *args, **kwargs):
        self.symm = new CxxSymm1D()
        self.boundary = <CxxBdry1D*>(self.symm)

    def __dealloc__(self):
        del self.symm


cdef class Surface1D(Boundary1D):
    """A solid surface."""
    def __cinit__(self, *args, **kwargs):
        self.surf = new CxxSurf1D()
        self.boundary = <CxxBdry1D*>(self.surf)

    def __dealloc__(self):
        del self.surf


cdef class ReactingSurface1D(Boundary1D):
    """A reacting solid surface."""
    def __cinit__(self, *args, **kwargs):
        self.surf = new CxxReactingSurf1D()
        self.boundary = <CxxBdry1D*>(self.surf)

    def __dealloc__(self):
        del self.surf

    def set_kinetics(self, Kinetics kin):
        """Set the kinetics manager (surface reaction mechanism object)."""
        if kin.kinetics.type() not in (kinetics_type_interface,
                                       kinetics_type_edge):
            raise TypeError('Kinetics object must be derived from '
                            'InterfaceKinetics.')
        self.surf.setKineticsMgr(<CxxInterfaceKinetics*>kin.kinetics)

    property coverage_enabled:
        """Controls whether or not to solve the surface coverage equations."""
        def __set__(self, value):
            self.surf.enableCoverageEquations(<cbool>value)


cdef class _FlowBase(Domain1D):
    """ Base class for 1D flow domains """
    def __cinit__(self, *args, **kwargs):
        self.flow = NULL

    def __init__(self, *args, **kwargs):
        self.domain = <CxxDomain1D*>(self.flow)
        super().__init__(*args, **kwargs)
        if not self.gas.transport_model:
            self.gas.transport_model = 'Mix'
        self.flow.setKinetics(deref(self.gas.kinetics))
        self.flow.setTransport(deref(self.gas.transport))
        self.P = self.gas.P
        self.flow.solveEnergyEqn()

    property P:
        """ Pressure [Pa] """
        def __get__(self):
            return self.flow.pressure()
        def __set__(self, P):
            self.flow.setPressure(P)

    def set_transport(self, _SolutionBase phase):
        """
        Set the `Solution` object used for calculating transport properties.
        """
        self.gas = phase
        self.flow.setTransport(deref(self.gas.transport))

    property soret_enabled:
        """
        Determines whether or not to include diffusive mass fluxes due to the
        Soret effect. Enabling this option works only when using the
        multicomponent transport model.
        """
        def __get__(self):
            return self.flow.withSoret()
        def __set__(self, enable):
            self.flow.enableSoret(<cbool>enable)

    property energy_enabled:
        """ Determines whether or not to solve the energy equation."""
        def __get__(self):
            return self.flow.doEnergy(0)
        def __set__(self, enable):
            if enable:
                self.flow.solveEnergyEqn()
            else:
                self.flow.fixTemperature()

    def set_fixed_temp_profile(self, pos, T):
        """Set the fixed temperature profile. This profile is used
        whenever the energy equation is disabled.

        :param pos:
            arrray of relative positions from 0 to 1
        :param temp:
            array of temperature values

        >>> d.set_fixed_temp_profile(array([0.0, 0.5, 1.0]),
        ...                          array([500.0, 1500.0, 2000.0])
        """
        cdef vector[double] x, y
        for p in pos:
            x.push_back(p)
        for t in T:
            y.push_back(t)
        self.flow.setFixedTempProfile(x, y)

    def __dealloc__(self):
        del self.flow

    def set_boundary_emissivities(self, e_left, e_right):
        self.flow.setBoundaryEmissivities(e_left, e_right)

    property radiation_enabled:
        """ Determines whether or not to include radiative heat transfer """
        def __get__(self):
            return self.flow.radiationEnabled()
        def __set__(self, do_radiation):
            self.flow.enableRadiation(<cbool>do_radiation)


cdef CxxIdealGasPhase* getIdealGasPhase(ThermoPhase phase) except *:
    if phase.thermo.eosType() != thermo_type_ideal_gas:
        raise TypeError('ThermoPhase object is not an IdealGasPhase')
    return <CxxIdealGasPhase*>(phase.thermo)


cdef class FreeFlow(_FlowBase):
    def __cinit__(self, _SolutionBase thermo, *args, **kwargs):
        gas = getIdealGasPhase(thermo)
        self.flow = <CxxStFlow*>(new CxxFreeFlame(gas, thermo.n_species, 2))


cdef class AxisymmetricStagnationFlow(_FlowBase):
    """
    An axisymmetric flow domain.

    In an axisymmetric flow domain, the equations solved are the similarity
    equations for the flow in a finite-height gap of infinite radial extent.
    The solution variables are:

    *u*
        axial velocity
    *V*
        radial velocity divided by radius
    *T*
        temperature
    *lambda*
        (1/r)(dP/dr)
    *Y_k*
        species mass fractions

    It may be shown that if the boundary conditions on these variables are
    independent of radius, then a similarity solution to the exact governing
    equations exists in which these variables are all independent of radius.
    This solution holds only in in low-Mach-number limit, in which case
    (dP/dz) = 0, and lambda is a constant. (Lambda is treated as a spatially-
    varying solution variable for numerical reasons, but in the final solution
    it is always independent of z.) As implemented here, the governing
    equations assume an ideal gas mixture.  Arbitrary chemistry is allowed, as
    well as arbitrary variation of the transport properties.
    """
    def __cinit__(self, _SolutionBase thermo, *args, **kwargs):
        gas = getIdealGasPhase(thermo)
        self.flow = <CxxStFlow*>(new CxxAxiStagnFlow(gas, thermo.n_species, 2))


cdef class Sim1D:
    """
    Class Sim1D is a container for one-dimensional domains. It also holds the
    multi-domain solution vector, and controls the process of finding the
    solution.

    Domains are ordered left-to-right, with domain number 0 at the left.
    """
    def __cinit__(self, *args, **kwargs):
        self.sim = NULL

    # The signature of this function causes warnings for Sphinx documentation
    def __init__(self, domains, *args, **kwargs):
        cdef vector[CxxDomain1D*] D
        cdef Domain1D d
        for d in domains:
            D.push_back(d.domain)

        self.sim = new CxxSim1D(D)
        self.domains = tuple(domains)
        self.set_interrupt(interrupts.no_op)
        self._initialized = False
        self._initial_guess_args = ()
        self._initial_guess_kwargs = {}

    def set_interrupt(self, f):
        """
        Set an interrupt function to be called each time that OneDim::eval is
        called. The signature of *f* is `float f(float)`. The default
        interrupt function is used to trap KeyboardInterrupt exceptions so
        that `ctrl-c` can be used to break out of the C++ solver loop.
        """
        if not isinstance(f, Func1):
            f = Func1(f)
        self.interrupt = f
        self.sim.setInterrupt(self.interrupt.func)

    def domain_index(self, dom):
        """
        Get the index of a domain, specified either by name or as a Domain1D
        object.
        """
        if isinstance(dom, Domain1D):
            idom = self.domains.index(dom)
        elif isinstance(dom, int):
            idom = dom
        else:
            idom = None
            for i,d in enumerate(self.domains):
                if d.name == dom:
                    idom = i
                    dom = d
            if idom is None:
                raise KeyError('Domain named "{0}" not found.'.format(dom))

        assert 0 <= idom < len(self.domains)
        return idom

    def _get_indices(self, dom, comp):
        idom = self.domain_index(dom)
        dom = self.domains[idom]
        if isinstance(comp, (str, unicode, bytes)):
            kcomp = dom.component_index(comp)
        else:
            kcomp = comp

        assert 0 <= kcomp < dom.n_components

        return idom, kcomp

    def value(self, domain, component, point):
        """
        Solution value at one point

        :param domain:
            Domain1D object, name, or index
        :param component:
            component name or index
        :param point:
            grid point number within *domain* starting with 0 on the left

        >>> t = s.value('flow', 'T', 6)
        """
        dom, comp = self._get_indices(domain, component)
        return self.sim.value(dom, comp, point)

    def set_value(self, domain, component, point, value):
        """
        Set the value of one component in one domain at one point to 'value'.

        :param domain:
            Domain1D object, name, or index
        :param component:
            component name or index
        :param point:
            grid point number within *domain* starting with 0 on the left
        :param value:
            numerical value

        >>> s.set(d, 3, 5, 6.7)
        >>> s.set(1, 0, 5, 6.7)
        >>> s.set('flow', 'T', 5, 500)
        """
        dom, comp = self._get_indices(domain, component)
        self.sim.setValue(dom, comp, point, value)

    def work_value(self, domain, component, point):
        """
        Internal work array value at one point. After calling eval, this array
        contains the values of the residual function.

        :param domain:
            Domain1D object, name, or index
        :param component:
            component name or index
        :param point:
            grid point number in the domain, starting with zero at the left

        >>> t = s.value(flow, 'T', 6)
        """
        dom, comp = self._get_indices(domain, component)
        return self.sim.workValue(dom, comp, point)

    def profile(self, domain, component):
        """
        Spatial profile of one component in one domain.

        :param domain:
            Domain1D object, name, or index
        :param component:
            component name or index

        >>> T = s.profile(flow, 'T')
        """
        idom, kcomp = self._get_indices(domain, component)
        dom = self.domains[idom]
        cdef int j
        cdef np.ndarray[np.double_t, ndim=1] data = np.empty(dom.n_points)
        for j in range(dom.n_points):
            data[j] = self.sim.value(idom, kcomp, j)
        return data

    def set_profile(self, domain, component, positions, values):
        """
        Set an initial estimate for a profile of one component in one domain.

        :param domain:
            Domain1D object, name, or index
        :param component:
            component name or index
        :param positions:
            sequence of relative positions, from 0 on the left to 1 on the right
        :param values:
            sequence of values at the relative positions specified in *positions*

        >>> s.set_profile(d, 'T', [0.0, 0.2, 1.0], [400.0, 800.0, 1500.0])
        """
        dom, comp = self._get_indices(domain, component)

        cdef vector[double] pos_vec, val_vec
        for p in positions:
            pos_vec.push_back(p)
        for v in values:
            val_vec.push_back(v)

        self.sim.setProfile(dom, comp, pos_vec, val_vec)

    def set_flat_profile(self, domain, component, value):
        """Set a flat profile for one component in one domain.

        :param domain:
            Domain1D object, name, or index
        :param component:
            component name or index
        :param v:
            value

        >>> s.set_flat_profile(d, 'u', -3.0)
        """
        dom, comp = self._get_indices(domain, component)
        self.sim.setFlatProfile(dom, comp, value)

    def show_solution(self):
        """ print the current solution. """
        if not self._initialized:
            self.set_initial_guess()
        self.sim.showSolution()

    def set_time_step(self, stepsize, n_steps):
        """Set the sequence of time steps to try when Newton fails.

        :param stepsize:
            initial time step size [s]
        :param n_steps:
            sequence of integer step numbers

        >>> s.set_time_step(1.0e-5, [1, 2, 5, 10])
        """
        cdef vector[int] data
        for n in n_steps:
            data.push_back(n)
        self.sim.setTimeStep(stepsize, data.size(), &data[0])

    property max_time_step_count:
        """
        Get/Set the maximum number of time steps allowed before reaching the
        steady-state solution
        """
        def __get__(self):
            return self.sim.maxTimeStepCount()
        def __set__(self, nmax):
            self.sim.setMaxTimeStepCount(nmax)

    def set_initial_guess(self, *args, **kwargs):
        """
        Set the initial guess for the solution. Derived classes extend this
        function to set approximations for the temperature and composition
        profiles.
        """
        self._initial_guess_args = args
        self._initial_guess_kwargs = kwargs
        self._get_initial_solution()
        self._initialized = True

    def _get_initial_solution(self):
        """
        Load the initial solution from each domain into the global solution
        vector.
        """
        self.sim.resize()
        self.sim.getInitialSoln()

    def extinct(self):
        """
        Method overloaded for some flame types to indicate if the flame has been
        extinguished. Base class method always returns 'False'
        """
        return False

    def solve(self, loglevel=1, refine_grid=True, auto=False):
        """
        Solve the problem.

        :param loglevel:
            integer flag controlling the amount of diagnostic output. Zero
            suppresses all output, and 5 produces very verbose output.
        :param refine_grid:
            if True, enable grid refinement.
        :param auto: if True, sequentially execute the different solution stages
            and attempt to automatically recover from errors. Attempts to first
            solve on the initial grid with energy enabled. If that does not
            succeed, a fixed-temperature solution will be tried followed by
            enabling the energy equation, and then with grid refinement enabled.
            If non-default tolerances have been specified or multicomponent
            transport is enabled, an additional solution using these options
            will be calculated.
        """

        if not auto:
            if not self._initialized:
                self.set_initial_guess()
            self.sim.solve(loglevel, <cbool>refine_grid)
            return

        have_user_tolerances = any(dom.have_user_tolerances for dom in self.domains)
        if have_user_tolerances:
            # Save the user-specified tolerances
            atol_ss_final = [dom.steady_abstol() for dom in self.domains]
            rtol_ss_final = [dom.steady_reltol() for dom in self.domains]
            atol_ts_final = [dom.transient_abstol() for dom in self.domains]
            rtol_ts_final = [dom.transient_reltol() for dom in self.domains]

        for dom in self.domains:
            dom.set_steady_tolerances(default=(1e-4, 1e-9))
            dom.set_transient_tolerances(default=(1e-4, 1e-11))

        # Do initial solution steps without multicomponent transport
        solve_multi = self.gas.transport_model == 'Multi'
        if solve_multi:
            self.gas.transport_model = 'Mix'
            for dom in self.domains:
                if isinstance(dom, _FlowBase):
                    dom.set_transport(self.gas)

        def log(msg, *args):
            if loglevel:
                print('\n{:*^78s}'.format(' ' + msg.format(*args) + ' '))

        flow_domains = [D for D in self.domains if isinstance(D, _FlowBase)]
        zmin = [D.grid[0] for D in flow_domains]
        zmax = [D.grid[-1] for D in flow_domains]
        nPoints = [len(flow_domains[0].grid), 12, 24, 48]

        for N in nPoints:
            for i,D in enumerate(flow_domains):
                if N != len(D.grid):
                    D.grid = np.linspace(zmin[i], zmax[i], N)

            self.set_initial_guess(*self._initial_guess_args,
                                   **self._initial_guess_kwargs)

            try:
                # Try solving with energy enabled, which usually works
                log('Solving on {} point grid with energy equation enabled', N)
                self.energy_enabled = True
                self.sim.solve(loglevel, <cbool>False)
                solved = True
            except Exception:
                solved = False

            if not solved:
                # If initial solve using energy equation fails, fall back on the
                # traditional fixed temperature solve followed by solving the energy
                # equation
                log('Initial solve failed; Retrying with energy equation disabled')
                try:
                    self.energy_enabled = False
                    self.sim.solve(loglevel, <cbool>False)
                    log('Solving on {} point grid with energy equation re-enabled', N)
                    self.energy_enabled = True
                    self.sim.solve(loglevel, <cbool>False)
                    solved = True
                except Exception:
                    pass

            if solved and not self.extinct():
                # Found a non-extinct solution on the fixed grid
                log('Solving with grid refinement enabled')
                try:
                    self.sim.solve(loglevel, <cbool>True)
                    solved = True
                except Exception:
                    solved = False

                if solved and not self.extinct():
                    # Found a non-extinct solution on the refined grid
                    break

            if self.extinct():
                log('Flame is extinct on {} point grid', N)

        if not solved:
            raise Exception('Could not find a solution for the 1D problem')

        if solve_multi:
            log('Solving with multicomponent transport')
            self.gas.transport_model = 'Multi'
            for dom in self.domains:
                if isinstance(dom, _FlowBase):
                    dom.set_transport(self.gas)

        if have_user_tolerances:
            log('Solving with user-specifed tolerances')
            for i in range(len(self.domains)):
                self.domains[i].set_steady_tolerances(abs=atol_ss_final[i],
                                                      rel=rtol_ss_final[i])
                self.domains[i].set_transient_tolerances(abs=atol_ts_final[i],
                                                         rel=rtol_ts_final[i])

        # Final call with expensive options enabled
        if have_user_tolerances or solve_multi:
            self.sim.solve(loglevel, <cbool>True)


    def refine(self, loglevel=1):
        """
        Refine the grid, adding points where solution is not adequately
        resolved.
        """
        self.sim.refine(loglevel)

    def set_refine_criteria(self, domain, ratio=10.0, slope=0.8, curve=0.8,
                          prune=0.05):
        """
        Set the criteria used to refine one domain.

        :param domain:
            domain object, index, or name
        :param ratio:
            additional points will be added if the ratio of the spacing on
            either side of a grid point exceeds this value
        :param slope:
            maximum difference in value between two adjacent points, scaled by
            the maximum difference in the profile (0.0 < slope < 1.0). Adds
            points in regions of high slope.
        :param curve:
            maximum difference in slope between two adjacent intervals, scaled
            by the maximum difference in the profile (0.0 < curve < 1.0). Adds
            points in regions of high curvature.
        :param prune:
            if the slope or curve criteria are satisfied to the level of
            'prune', the grid point is assumed not to be needed and is removed.
            Set prune significantly smaller than 'slope' and 'curve'. Set to
            zero to disable pruning the grid.

        >>> s.set_refine_criteria(d, ratio=5.0, slope=0.2, curve=0.3, prune=0.03)
        """
        idom = self.domain_index(domain)
        self.sim.setRefineCriteria(idom, ratio, slope, curve, prune)

    def set_grid_min(self, dz, domain=None):
        """
        Set the minimum grid spacing on *domain*. If *domain* is None, then
        set the grid spacing for all domains.
        """
        if domain is None:
            idom = -1
        else:
            idom = self.domain_index(domain)
        self.sim.setGridMin(idom, dz)

    def set_max_jac_age(self, ss_age, ts_age):
        """
        Set the maximum number of times the Jacobian will be used before it
        must be re-evaluated.

        :param ss_age:
            age criterion during steady-state mode
        :param ts_age:
            age criterion during time-stepping mode
        """
        self.sim.setJacAge(ss_age, ts_age)

    def set_time_step_factor(self, tfactor):
        """
        Set the factor by which the time step will be increased after a
        successful step, or decreased after an unsuccessful one.
        """
        self.sim.setTimeStepFactor(tfactor)

    def set_min_time_step(self, tsmin):
        """ Set the minimum time step. """
        self.sim.setMinTimeStep(tsmin)

    def set_max_time_step(self, tsmax):
        """ Set the maximum time step. """
        self.sim.setMaxTimeStep(tsmax)

    def set_fixed_temperature(self, T):
        """
        Set the temperature used to fix the spatial location of a freely
        propagating flame.
        """
        self.sim.setFixedTemperature(T)

    def save(self, filename='soln.xml', name='solution', description='none',
             loglevel=1):
        """
        Save the solution in XML format.

        :param filename:
            solution file
        :param name:
            solution name within the file
        :param description:
            custom description text

        >>> s.save(filename='save.xml', name='energy_off',
        ...        description='solution with energy eqn. disabled')

        """
        self.sim.save(stringify(filename), stringify(name),
                      stringify(description), loglevel)

    def restore(self, filename='soln.xml', name='solution', loglevel=2):
        """Set the solution vector to a previously-saved solution.

        :param filename:
            solution file
        :param name:
            solution name within the file
        :param loglevel:
            Amount of logging information to display while restoring,
            from 0 (disabled) to 2 (most verbose).

        >>> s.restore(filename='save.xml', name='energy_off')
        """
        self.sim.restore(stringify(filename), stringify(name), loglevel)
        self._initialized = True

    def restore_time_stepping_solution(self):
        """
        Set the current solution vector to the last successful time-stepping
        solution. This can be used to examine the solver progress after a failed
        integration.
        """
        self.sim.restoreTimeSteppingSolution()

    def restore_steady_solution(self):
        """
        Set the current solution vector to the last successful steady-state
        solution. This can be used to examine the solver progress after a
        failure during grid refinement.
        """
        self.sim.restoreSteadySolution()

    def show_stats(self, print_time=True):
        """
        Show the statistics for the last solution.

        If invoked with no arguments or with a non-zero argument, the timing
        statistics will be printed. Otherwise, the timing will not be printed.
        """
        self.sim.writeStats(print_time)

    def clear_stats(self):
        """
        Clear solver statistics.
        """
        self.sim.clearStats()

    property grid_size_stats:
        """Return total grid size in each call to solve()"""
        def __get__(self):
            return self.sim.gridSizeStats()

    property jacobian_time_stats:
        """Return CPU time spent evaluating Jacobians in each call to solve()"""
        def __get__(self):
            return self.sim.jacobianTimeStats()

    property jacobian_count_stats:
        """Return number of Jacobian evaluations made in each call to solve()"""
        def __get__(self):
            return self.sim.jacobianCountStats()

    property eval_time_stats:
        """
        Return CPU time spent on non-Jacobian function evaluations in each call
        to solve()
        """
        def __get__(self):
            return self.sim.evalTimeStats()

    property eval_count_stats:
        """
        Return number of non-Jacobian function evaluations made in each call to
        solve()
        """
        def __get__(self):
            return self.sim.evalCountStats()

    property time_step_stats:
        """Return number of time steps taken in each call to solve()"""
        def __get__(self):
            return self.sim.timeStepStats()

    def __dealloc__(self):
        del self.sim