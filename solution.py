import datetime
import math
import numpy as np
from matplotlib.pyplot import *

def mjd_to_jd(mjd):
    """
    Convert Modified Julian Day to Julian Day.
        
    Parameters
    ----------
    mjd : float
        Modified Julian Day
        
    Returns
    -------
    jd : float
        Julian Day
    
        
    """
    return mjd + 2400000.5

def jd_to_date(jd):
    """
    Convert Julian Day to date.
    
    Algorithm from 'Practical Astronomy with your Calculator or Spreadsheet', 
        4th ed., Duffet-Smith and Zwart, 2011.
    
    Parameters
    ----------
    jd : float
        Julian Day
        
    Returns
    -------
    year : int
        Year as integer. Years preceding 1 A.D. should be 0 or negative.
        The year before 1 A.D. is 0, 10 B.C. is year -9.
        
    month : int
        Month as integer, Jan = 1, Feb. = 2, etc.
    
    day : float
        Day, may contain fractional part.
        
    Examples
    --------
    Convert Julian Day 2446113.75 to year, month, and day.
    
    >>> jd_to_date(2446113.75)
    (1985, 2, 17.25)
    
    """
    jd = jd + 0.5
    
    F, I = math.modf(jd)
    I = int(I)
    
    A = math.trunc((I - 1867216.25)/36524.25)
    
    if I > 2299160:
        B = I + 1 + A - math.trunc(A / 4.)
    else:
        B = I
        
    C = B + 1524
    
    D = math.trunc((C - 122.1) / 365.25)
    
    E = math.trunc(365.25 * D)
    
    G = math.trunc((C - E) / 30.6001)
    
    day = C - E + F - math.trunc(30.6001 * G)
    
    if G < 13.5:
        month = G - 1
    else:
        month = G - 13
        
    if month > 2.5:
        year = D - 4716
    else:
        year = D - 4715
        
    return year, month, day

google = np.loadtxt("data/google_data.txt", skiprows=1, delimiter='\t')
nytemp = np.loadtxt("data/ny_temps.txt", skiprows=1, delimiter='\t')
yahoo = np.loadtxt("data/yahoo_data.txt", skiprows=1, delimiter='\t')
yahoo_date = np.array([jd_to_date(d) for d in mjd_to_jd(yahoo[:,0])])
yahoo_datetime = np.array([datetime.datetime(*d.astype(int)) for d in yahoo_date])
google_date = np.array([jd_to_date(d) for d in mjd_to_jd(google[:,0])])
google_datetime = np.array([datetime.datetime(*d.astype(int)) for d in google_date])
temp_date = np.array([jd_to_date(d) for d in mjd_to_jd(nytemp[:,0])])
temp_datetime = np.array([datetime.datetime(*d.astype(int)) for d in temp_date])
# Plot
fig, ax = subplots()
ax.plot_date(yahoo_datetime, yahoo[:,1], 'b-', label="Yahoo")
ax.plot_date(google_datetime, google[:,1], 'g-', label="Google")
ax2 = ax.twinx()
ax2.plot_date(temp_datetime, nytemp[:,1], 'm--', label="NY Temperature")
ax2.set_ylim(-150, 100)
ax1 = ax
ax1.set_xlabel("Date")
ax1.set_ylabel(r'Value ($)')
ax1.set_ylim(-20, 770)
ax2.set_ylabel(r'Temperature $^\circ$F')
ax1.set_title('New York Temperature, Google, and Yahoo!', fontsize=22)
handles = []
labels = []
for a in (ax1, ax2):
    h, l = a.get_legend_handles_labels()
    for i in range(len(h)):
        handles.append(h[i])
        labels.append(l[i])
ax.legend(handles, labels, loc=6, frameon=False)
fig.autofmt_xdate()
fig.canvas.draw()
