# Figure - Simulation of batch reactor 
#          with functions added to facilitate explorative simulation work
#
# Author: Jan Peter Axelsson
#------------------------------------------------------------------------------------------------------------------
# 2026-08-13 - Building fmu_eplore_pyfmi for the "new" class-based approach
# 2026-08-14 - Transfer states and diagrams list
# 2026-08-19 - Deal with ax1, ax2 etc - made a list ax of them and included in the class module
# 2026-08-20 - Changed setLines() to resetPen() and let tye itertools be used in the module only
#------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------
#  Specific application constructs: stateValue, parValue, parLocation, parCheck, diagrams, newplot(), describe()
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
      diagrams.append("ax[0].plot(t,sim_res['bioreactor.c[1]'],color='r',linestyle=linetype)")
      diagrams.append("ax[0].plot(t,sim_res['bioreactor.c[2]'],color='b',linestyle=linetype)")   
      diagrams.append("ax[0].legend(['X','S'])")   
      diagrams.append("ax[1].plot(t,sim_res['bioreactor.culture.q[1]'],color='r',linestyle=linetype)")   

   elif plotType == 'PhasePlane':
       
      plt.figure()
      ax[0] = plt.subplot(1,1,1)
    
      ax[0].set_title(title)
      ax[0].grid()
      ax[0].set_ylabel('S [g/L]')
      ax[0].set_xlabel('X [g/L]')

      # List of commands to be executed by simu() after a simulation         
      diagrams.clear()
      diagrams.append("ax[0].plot(sim_res['bioreactor.c[1]'],sim_res['bioreactor.c[2]'],color='b',linestyle=linetype)")
             
   else:
      print("Plot window type not correct")

# Define describtions partly coded here and partly taken from the FMU
def describe(name, decimals=3):
   """Look up description of culture, media, as well as parameters and variables in the model code"""
        
   if name == 'culture':
      print('Simplified text book model - only substrate S and cell concentration X')      
 
   elif name in ['broth', 'liquidphase', 'media']: 
      """Describe medium used"""
      X = model.get('liquidphase.X')[0] 
      X_description = model.get_variable_description('liquidphase.X') 
      X_mw = model.get('liquidphase.mw[1]')[0]
         
      S = model.get('liquidphase.S')[0] 
      S_description = model.get_variable_description('liquidphase.S')
      S_mw = model.get('liquidphase.mw[2]')[0]
         
      print()
      print('Reactor broth substances included in the model')
      print()
      print(X_description, '    index = ', X, 'molecular weight = ', X_mw, 'Da')
      print(S_description, 'index = ', S, 'molecular weight = ', S_mw, 'Da')
  
   elif name in ['parts']:
      describe_parts(component_list_minimum)
      
   elif name in ['MSL']:
      describe_MSL()

   else:
      describe_general(name, decimals)
      
#------------------------------------------------------------------------------------------------------------------
#  Startup
#------------------------------------------------------------------------------------------------------------------

FMU_explore_info()