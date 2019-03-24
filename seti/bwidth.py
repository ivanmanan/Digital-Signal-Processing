#!/usr/bin/env python
""" Find the full-width half maximum bandwidth of signals a user-defined number of standard deviations of the noise above the noise. Returns a string of bandwidths of the signals (Hz) from the signal 
occurring at the lowest frequency to the signal occurring at the highest frequency.

This module performs the calculation as follows::

- Calculate the median noise (baseline).
- Find threshold power that a signal must rise above to qualify as a signal. This threshold is a user defined number of standard deviations of the noise above the median
noise.
- Find the signals in the specified frequency window, defined by whether they rise above the threshold, and then find their maximum powers and at which frequencies these maxima occur.
- Find the frequencies for each signal at which the power spectrum is at half the maximum power of
each signal.
- Measure the difference in frequency between the half-power frequency coordinates.
- Return the bandwidth of each signal.

Examples
--------

    (to be added)

Authors
-------
|    UCLA SETI Group Spring 2017
|    Ruth Pike
|    Thomas Ayalde (tayalde268@gmail.com)
|    Paul Pinchuk (ppinchuk@physics.ucla.edu)


Jean-Luc Margot UCLA SETI Group.
University of California, Los Angeles.
Copyright 2018. All rights reserved.
"""
import os
import sys
if os.environ['SETIBASE'] not in sys.path:
    sys.path.append(os.environ['SETIBASE'])  # This is only needed if module not on python path

import numpy as np
import math
from setiS18 import CandidateSignal
import setiS18.figures.tfdiagram as tf
import setiS18.signal_characterization.idsignal as idsignal

def bwidth(id_, mult=10, window=300, show=True):
    """ Calculate and print bandwidth of signal using the defined multiplier threshold.

    Parameters
    ----------
    id_ : int
        ID of signal that appears in name of subarray file.
    mult : float
        Multiplier that signifies how many times above std to threshold signal for bandwidth calculation
        window : float, optional
        Size of half-window (in Hz) to look around the signal. If you specify a window value that is too
        small to contain the signal completely, it will automatically be adjusted so that the entire
        signal can fit within the data matrix. Units: Hz
    show: bool
        Whether to print the results of the bandwidths

    Notes
    -----

    

    """
    
    intersections = [] #will contain indexes for the signal maxima in the power spectrum
    max_indices = [] #will contain intersection points of power spectrum of signal with threshold at half the maximum power
    bandwidths = [] #will contain bandwidths of each signal
    
    signal = CandidateSignal(id_,window) #Initiate CandidateSignal object
    pow_spec = signal.pow_vs_freq() # FFT power spectrum
   
    resolution = signal.fres # MHz; amount of frequency between each signal sample
    
    baseline = np.median(pow_spec) #median power of signal in the specified window
    sd = 1 # standard deviation of the noise
 
    # Generate threshold value for identifying signal
    threshold = baseline + mult*sd 
    
    #Find maximum power and corresponding frequency coordinate for each signal
    #  in the power spectrum
    
    signal_maxima = idsignal.idsignal(id_,mult=mult,window=window)
    
    #Find the indexes for the signal maxima in the power spectrum
    
    for i in np.arange(0,len(signal_maxima[:,1])):
        index = abs(signal.frqs-signal_maxima[:,1][i]).argmin()
        max_indices = max_indices + [index]
    
    if show:
        # Plot threshold on spectrogram (i.e. power spectrum diagram)
        tf.pow_intersect(id_, threshold)
    
    #Find intersection points of power spectrum of signal with threshold at half the
    # maximum power

    for i in np.arange(0,len(signal_maxima[:,0])): 
        individual_intersect = tf.intersection_points(id_, signal_maxima[:,0][i]/2)
        intersections = intersections + [individual_intersect]
    
    if show:
        print("Signal bandwidths given from lowest frequency to highest frequency. \n Note that each"\
          +"bandwidth as a potential uncertainty of +/- " +str(signal.fres*2) + ".")

    for i in np.arange(0,len(signal_maxima[:,0])): 
        
        if show:
            print("\nSignal #"+str(i+1))
        
        #If no intersections found, return that there is no bandwidth
        if not intersections[i].size:
            print("No bandwidth found.")
        
        #If there are intersections with the threshold found, then find the bandwidths
        else:
            max_pow_index = int(max_indices[i])
            freqs = tf.SignalPlot(signal,window).frqs
            
            #Find the intersection points closest to the maximum of each signal
            freq_min = intersections[i][0][intersections[i][0] > freqs[max_pow_index]].min()
            freq_max = intersections[i][0][intersections[i][0] < freqs[max_pow_index]].max()
            
            #print("Frequency max:", freq_max)
            #print("Frequency min:", freq_min)
                
            if freq_min == 0 or freq_max == 0:
                bandwidths = bandwidths + [0]
                if show:
                    print("Signal out of range")
            else:
                # Take difference between frequency coordinates of intersection points to give bandwidth
                bandwidth = math.fabs(freq_max - freq_min)
                bandwidths = bandwidths + [bandwidth]
                if show:
                    print("Bandwidth (FWHM):", bandwidth, "Hz")
                    
    return bandwidths

if __name__ == "__main__":

    from numpydoc.docscrape import NumpyDocString
    import argparse as ap
    import warnings

    # ignore warnings from NumpyDocString about extra sections like "Author"
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        doc = NumpyDocString(__doc__)

    parser = ap.ArgumentParser(formatter_class=ap.RawDescriptionHelpFormatter, description="\n".join(doc["Examples"]))
    parser.add_argument('id', help="fftbsub file id")
    parser.add_argument('mult', type=int, help="number of multiples of std")
    try:
        args = vars(parser.parse_args())
        bwidth(args['id'], args['mult'])
    except IOError:
        print("Subarray does not exist!")
        
       
