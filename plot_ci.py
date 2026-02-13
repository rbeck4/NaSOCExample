#Pray, pray to St. Isidore; may he have mercy on your poor soul for trying to
#run something that I've written.
import matplotlib
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import scipy
import string
import sys
sys.path.append("/home/ryan/canalyzer")
#mac can eat an entire bag of ducks
sys.path.append("/Users/ryan/canalyzer")
from CANalyzer.ci_spectra import CI_spectra

font = { 
    'size' : '20', 
    'weight' : 'bold'
    }
matplotlib.rc('font', **font)
matplotlib.rcParams['axes.linewidth'] = 4.0
matplotlib.rcParams['hatch.linewidth'] = 2.0
matplotlib.rcParams['lines.linewidth'] = 2.0
har2ev = 27.2114

enMin = 1.990
enMax = 2.010
res = .00001
nPoints = int((enMax-enMin)/res)

plots = []
energy = []

fileList = [\
            "nonRel/03_NaCI.log", \
            "Scalar/03_NaCI.log", \
            "SOC/03_NaCI.log", \
           ]

fchkList = [\
            "nonRel/03_NaCI.fchk", \
            "Scalar/03_NaCI.fchk", \
            "SOC/03_NaCI.fchk", \
           ]

names    = [\
            "Non-Rel", \
            "SF-X2C", \
            "X2C", \
           ]

for i, fl in enumerate(fileList):
  print("WORKING, ", fl, " [", i+1, "/", len(fileList), "]")
  plots.append(CI_spectra(fl, fchkList[i], None))
  
for i in range(len(fileList)):
  plots[i].decompose_byorbital()
  energy.append((plots[i].energy[0,:])*har2ev)
  print("Plots: ", names[i], " max: ", max(energy[-1]))

for i in range(len(fileList)):
  space_names  = list(plots[0].spaces)
  for space in range(len(space_names)):
    os = plots[i].decomp_byorbital[0, :, space]
    totEn = energy[i]
    plots[i].make_spectrum(space_names[space], enMin, enMax, totEn, os, 0.001, npoints=nPoints)

space_names += ["Full Spectrum"]
fullEn = [[0] for x in range(len(fileList))]
fullOs = [[0] for x in range(len(fileList))]
for i in range(len(fileList)):
  fullOs[i] = plots[i].oscstr[0]
  fullEn[i] = energy[i]
  plots[i].make_spectrum("Full Spectrum", enMin, enMax, fullEn[i], fullOs[i], 0.001, npoints=nPoints)

#PLOTTING:
colors = list(['tab:blue','tab:red', 'tab:green'])
fig, ax = plt.subplots(1, sharex='col', figsize=[8,5], gridspec_kw={'hspace': 0},squeeze=False)

for e,p in enumerate(plots):
  ##Plot MO contributions to excitations:
  #for i, space in enumerate(space_names):
  #  y = p.spectra[space]
  #  x = np.linspace(enMin-5, enMax+5, len(y))
  #  if "Full" in space:
  #    ax[e,0].plot(x, y, label=str(space), color='k', linewidth=2)
  #  else:
  #    ax[e,0].plot(x, y, label=str(space), color=colors[i], linewidth=4)
  
  y = p.spectra["Full Spectrum"]
  x = np.linspace(enMin, enMax, len(y))
  ax[0,0].plot(x, y, label=names[e], color=colors[e], linewidth=4)
  
ax[0,0].set_yticks([])
ax[0,0].set_xlim([enMax,enMin])
ax[0,0].set_ylim([0.,None])
ax[0,0].axhline(y=0, xmin=enMin, xmax=enMax)
ax[0,0].legend(loc='upper left', handlelength=0.5, frameon=False, prop=dict(size=15))

plt.ylabel("Intensity (a.u.)", fontweight='bold')
plt.xlabel("Energy (eV)", fontweight='bold')
fig.tight_layout()
plt.savefig("Na.png")
  
