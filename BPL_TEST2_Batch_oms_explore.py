# Setup application functions BPL_TEST2_Batch, dependent on previous import of functions from fmu_explore 
# Author: Jan Peter Axelsson
#------------------------------------------------------------------------------------------------------------------
# 2026-02-24 - Created
# 2026-09-29 - Import for oms related handling
# 2026-10-07 - Diagrams modified for DyMat
# 2026-10-07 - Rudimentary function descxribe()
#------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------
#  Framework
#------------------------------------------------------------------------------------------------------------------

import numpy as np
import scipy.io
import matplotlib.pyplot as plt 

#------------------------------------------------------------------------------------------------------------------
#  Specific application constructs:  newplot(), describe()
#------------------------------------------------------------------------------------------------------------------

# Define standard diagrams
def newplot(title='Batch cultivation', plotType='TimeSeries'):
    """ Standard plot window
        title = ''
       two possible diagrams
        diagram = 'TimeSeries' default
        diagram = 'PhasePlane' """
    
    resetPen()
    
    # Plot diagram 
    if plotType == 'TimeSeries':

        ax1 = plt.subplot(2,1,1)
        ax2 = plt.subplot(2,1,2)

        ax.clear()
        ax.append(ax1)
        ax.append(ax2)

        ax[0].set_title(title)
        ax[0].grid()
        ax[0].set_ylabel('X and S [g/L]')

        ax[1].grid()
        ax[1].set_ylabel('mu [1/h]')
        ax[1].set_xlabel('Time [h]') 
      
        # List of commands to be executed by simu() after a simulation  
        diagrams.clear()
        diagrams.append("ax[0].plot(t, sim_res['Batch.bioreactor.c[1]'], color='r',linestyle=linetype)")
        diagrams.append("ax[0].plot(t, sim_res['Batch.bioreactor.c[2]'], color='b',linestyle=linetype)")   
        diagrams.append("ax[0].legend(['X','S'])")   
        diagrams.append("ax[1].plot(t, sim_res['Batch.bioreactor.culture.q[1]'], color='r',linestyle=linetype)")   

    elif plotType == 'PhasePlane':
       
        plt.figure()
        ax[0] = plt.subplot(1,1,1)

        ax[0].set_title(title)
        ax[0].grid()
        ax[0].set_ylabel('S [g/L]')
        ax[0].set_xlabel('X [g/L]')

        # List of commands to be executed by simu() after a simulation         
        diagrams.clear()
        diagrams.append("ax[0].plot(sim_res['Batch.bioreactor.c[1]'], sim_res['Batch.bioreactor.c[2]'], \
                         color='b', linestyle=linetype)")

    else:
        print("Plot window type not correct")


def describe(name, decimals=3):
    """Look up description of culture, media, as well as parameters and variables in the model code"""

    if name == 'culture':
        print('Simplified text book model - only substrate S and cell concentration X')
    elif name in ['MSL']:
        describe_MSL()
    else:
        dummy = decimals
        #describe_general(name, decimals)

#------------------------------------------------------------------------------------------------------------------
#  Startup
#------------------------------------------------------------------------------------------------------------------

FMU_explore_info()