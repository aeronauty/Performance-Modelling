#!/usr/bin/env python3# -*- coding: utf-8 -*-"""Created on Weds 3rd June 2020This module enables the blade form curves from Liner and Evans (1951) to beimported and interpolated for arbitrary values of x from 0.2 to 1, forpropellers I, II, and IIINote that only propeller I has any sweepA single dictionary is returned that has the required parameters@author: harrysmith"""import csvimport matplotlib.pyplot as plt import numpy as npfrom scipy.interpolate import splrep, splevplotting = Truesmoothing = False from scipy.interpolate import interp1d# >>># >>> x = np.linspace(0, 10, num=11, endpoint=True)# >>> y = np.cos(-x**2/9.0)# >>> f = interp1d(x, y)# >>> f2 = interp1d(x, y, kind='cubic')LinerFigure = 'BladeFormCurves.csv'# Load in the .csv filedatafile = open(LinerFigure, 'r')datareader = csv.reader(datafile)# Make a large figure if plotting:    plt.figure(figsize=(16,16))# Run through the CSV file line by linecolours = ['b', 'g', 'r', 'c', 'm', 'k', 'y', 'b', 'g']i = 0r = 0nrows = len(list(datareader))# Re-open and remake the datareader object as, apparently, getting the length means you cannot iterate through itdatafile = open(LinerFigure, 'r')datareader = csv.reader(datafile)# Make an empty dictionary to store interpolants inf = {}# What do we need to scale each y axis byscalings = {'t_c': 0.04*24, 'beta' : 4*24, 'cld' : 0.04*24, 'c' : 0.01*24 }for row in datareader:       r = r + 1    if (len(row) == 2) and (r < nrows):     # Then this line has entries - otherwise it is blank        if row[0] == 'x':     # This must be a header line if the first entry is 'x'            xdata = []             # In which case the lists for alpha and CL are reset/initilised as empty lists            ydata = []            dataname  = row[1]        else:            xdata = xdata + [row[0]] # This point is only reached if we have initilised the alpha/CL lists, and then the entries are appended to them            ydata = ydata + [row[1]]    else:               # Turn the list of strings into floats and then into np arrays        xdata = np.array([float(i) for i in xdata])        ydata = np.array([float(i) for i in ydata])                if smoothing:            bspl = splrep(xdata, ydata,s=2)            bspl_y = splev(xdata, bspl)            # Plot them        if plotting:            plt.plot(xdata, ydata, 'x', color=colours[i])            if smoothing:                plt.plot(xdata, bspl_y, 'o', color=colours[i])        i = i + 1                # Make an interpolant - store this in the dictionary with the 'key' being the name of the data taken out        f[dataname] = interp1d(xdata, ydata, kind='linear', fill_value="extrapolate")                # Make a vector of x and y values        xvector = np.linspace(.2, 1, 100)        yvector = f[dataname](xvector)        # Plot the interpolated values        if plotting:            plt.plot(xvector, yvector, '-', color=colours[i])    # plt.show()# plt.axis([0, 1, 0, 1])# All propellers have D = 10ft at the design conditionD = 10*.3048def FormCurves(propnum=2, x = np.linspace(.2, 1, 10)):    prop = {}    if propnum == 1:        prop['c'] = f['c1_3'](x)*D*scalings['c']        prop['Cld'] = f['cld1_2'](x)*scalings['cld']        prop['beta'] = f['beta'](x)*scalings['beta']        prop['t_c'] = f['t_c'](x)*scalings['t_c']    elif propnum == 2:        prop['c'] = f['c2'](x)*D*scalings['c']            prop['Cld'] = f['cld1_2'](x)*scalings['cld']        prop['beta'] = f['beta'](x)*scalings['beta']        prop['t_c'] = f['t_c'](x)*scalings['t_c']    elif propnum == 3:        prop['c'] = f['c1_3'](x)*D*scalings['c']        prop['Cld'] = f['cld3'](x)*scalings['cld']        prop['beta'] = f['beta'](x)*scalings['beta']        prop['t_c'] = f['t_c'](x)*scalings['t_c']    else:        print("Invalid propeller number entered")        return prop