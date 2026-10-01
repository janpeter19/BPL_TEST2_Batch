# Setup application functions BPL_TEST2_Batch, dependent on previous import of functions from fmu_explore 
# Author: Jan Peter Axelsson
#------------------------------------------------------------------------------------------------------------------
# 2026-02-24 - Created
# 2026-09-29 - Import for oms relatted handling
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
        diagrams.append("ax[0].plot(t, sim_res['data_2'][2], color='r',linestyle=linetype)")
        diagrams.append("ax[0].plot(t, sim_res['data_2'][3], color='b',linestyle=linetype)")   
        diagrams.append("ax[0].legend(['X','S'])")   
        diagrams.append("ax[1].plot(t, sim_res['data_2'][12], color='r',linestyle=linetype)")   

    elif plotType == 'PhasePlane':
       
        plt.figure()
        ax[0] = plt.subplot(1,1,1)

        ax[0].set_title(title)
        ax[0].grid()
        ax[0].set_ylabel('S [g/L]')
        ax[0].set_xlabel('X [g/L]')

        # List of commands to be executed by simu() after a simulation         
        diagrams.clear()
        diagrams.append("ax[0].plot(mat_data['data_2'][2], mat_data['data_2'][3], color='b', linestyle=linetype)")
             
    else:
        print("Plot window type not correct")

#------------------------------------------------------------------------------------------------------------------
#  Startup
#------------------------------------------------------------------------------------------------------------------

FMU_explore_info()