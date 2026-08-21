# module fmu_explore_pyfmi
# Author: Jan Peter Axelsson
# License:  GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007
#------------------------------------------------------------------------------------------------------------------
# 2026-08-13a Now include par, init, disp
# 2026-08-13b Now include SDG, system_info, BPL_info
# 2026-08-13c Now include process_diagram
# 2026-08-13d Now include describe_general, describe_parts, describe_MSL, readParValue, readParLocation
# 2026-08-14a Corrected par() to include self.parCheck
# 2026-08-14b Add variables to class related to simu()
# 2026-08-17a Try to bring in the last functions simu() and show(), setLines() 
# 2026-08-17b Try to fix linecycler
# 2026-08-18a Corrected around linecycler, sim_res
# 2026-08-19a Changed BPL_info to FMU_explore_info, include ax1, ax2 for test
# 2026-08-19b Take away ax1 and ax2 and let them reach simu() using the new list ax part of data of class module
# 2026-08-20a Make lines a parameter and introduce resetPen() that can used by newplot() from the application
# 2026-08-21  Transferred to Github repository for running with Google Colab
#------------------------------------------------------------------------------------------------------------------

__version__ = '1.1.0'

import platform
import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.image as img
import zipfile
from importlib_metadata import version 
from pyfmi.fmi import FMUException 
from pyfmi import load_fmu
from itertools import cycle

class fmu_explore:
   
   # Set the actual variables associated with the application given
   def __init__(self, model, parValue, parLocation, parCheck, fmu_model, fmu_process_diagram, \
                      MSL_usage, MSL_version, BPL_version, \
                      opts_std, simulationTime, timeDiscreteStates, stateValue, \
                      diagrams, ax, lines):
                     
      self.FMU_explore_version = 'FMU-explore version 1.1.0'
      self.model = model
      self.parValue = parValue  
      self.parLocation = parLocation
      self.parCheck = parCheck
      self.MSL_usage = MSL_usage
      self.MSL_version = MSL_version
      self.BPL_version = BPL_version
      self.fmu_model = fmu_model
      self.fmu_process_diagram = fmu_process_diagram
      self.opts_std = opts_std
      self.simulationTime = simulationTime                                    
      self.timeDiscreteStates = timeDiscreteStates
      self.stateValue = stateValue
      self.diagrams = diagrams     
      self.ax = ax                 
      self.lines = lines

   # Define how to read dictionary for parameter values
   def readParValue(self, file, sheet):
      """ Read parameter short names and values from an Excel-file from defined sheet. For use in the notebook!
          Return a dictionary."""
      
      parValue = self.parValue
      
      parValue_local = {} 
      table = pd.ExcelFile(file).parse(sheet)
      for k in list(range(len(table))):
         parValue_local[table['Par'][k]] = table['Value'][k]
      parValue.update(parValue_local)

   # Define how to read dictionary for parameter location
   def readParLocation(self, file, sheets):
      """ Read parameter short and long names from an Excel-file sheet by sheet. For use in the notebook!
          Return a dictionary."""
      
      parLocation = self.parLocation
      
      parLocation_local = {}
      for sheet in sheets:
         table = pd.ExcelFile(file).parse(sheet)
         for k in list(range(len(table))):
            parLocation_local[table['Par'][k]] = table['Location'][k]
      parLocation.update(parLocation_local)      
 
   # Define function par() for parameter update
   def par(self, *x, **x_kwarg):
      """ Set parameter values if available in the predefined dictionaryt parValue. """
      
      parValue = self.parValue
      parCheck = self.parCheck
      
      x_kwarg.update(*x)
      x_temp = {}
      
      for key in x_kwarg.keys():
         if key in parValue.keys():
            x_temp.update({key: x_kwarg[key]})
         else:
            print('Error:', key, '- seems not an accessible parameter - check the spelling')
      parValue.update(x_temp)
   
      parErrors = [requirement for requirement in parCheck if not(eval(requirement))]
      if not parErrors == []:
         print('Error - the following requirements do not hold:')
         for index, item in enumerate(parErrors): print(item)

   # Define function init() for initial values update
   def init(self, *x, **x_kwarg):
      """ Set initial values and the name should contain string '_start' to be accepted.
          The function can handle general parameter string location names if entered as a dictionary. """
      
      parValue = self.parValue
      
      x_kwarg.update(*x)
      x_init={}

      for key in x_kwarg.keys():
         if '_start' in key: 
            x_init.update({key: x_kwarg[key]})
         else:
            print('Error:', key, '- seems not an initial value, use par() instead - check the spelling')
      parValue.update(x_init)
      
   def disp(self, name='', decimals=3, mode='short'):
      """ Display intial values and parameters in the model that include "name" and is in parLocation list.
          Note, it does not take the value from the dictionary par but from the model. """

      model = self.model
      parValue = self.parValue
      parLocation = self.parLocation

      def dict_reverser(d):
         seen = set()
         return {v: k for k, v in d.items() if v not in seen or seen.add(v)}
   
      if mode in ['short']:
         k = 0
         for Location in [parLocation[k] for k in parValue.keys()]:
            if name in Location:
               if type(model.get(Location)[0]) != np.bool_:
                  print(dict_reverser(parLocation)[Location] , ':', np.round(model.get(Location)[0],decimals))
               else:
                  print(dict_reverser(parLocation)[Location] , ':', model.get(Location)[0])               
            else:
               k = k+1
         if k == len(parLocation):
            for parName in parValue.keys():
               if name in parName:
                  if type(model.get(Location)[0]) != np.bool_:
                     print(parName,':', np.round(model.get(parLocation[parName])[0],decimals))
                  else: 
                     print(parName,':', model.get(parLocation[parName])[0])
      if mode in ['long','location']:
         k = 0
         for Location in [parLocation[k] for k in parValue.keys()]:
            if name in Location:
               if type(model.get(Location)[0]) != np.bool_:       
                  print(Location,':', dict_reverser(parLocation)[Location] , ':', np.round(model.get(Location)[0],decimals))
            else:
               k = k+1
         if k == len(parLocation):
            for parName in parValue.keys():
               if name in parName:
                  if type(model.get(Location)[0]) != np.bool_:
                     print(parLocation[parName], ':', dict_reverser(parLocation)[Location], ':', parName,':', 
                        np.round(model.get(parLocation[parName])[0],decimals))

   # Reset the pen for the diagrams
   def resetPen(self):
      self.linecycler = cycle(self.lines)


   # Show plots from sim_res, just that
   def show(self):
      """Show diagrams chosen by newplot()"""
      
      diagrams = self.diagrams
      ax = self.ax  
      linecycler = self.linecycler
      
      # Plot pen
      linetype = next(linecycler)    
      
      # Plot diagrams 
      for command in diagrams: eval(command)

   # Simulation
   def simu(self, simulationTimeLocal=5, mode='Initial'):        
      """Model loaded and given intial values and parameter before,
         and plot window also setup before."""

      options = self.opts_std      
      simulationTime = self.simulationTime
      diagrams = self.diagrams 
      ax = self.ax  
      linecycler = self.linecycler
      timeDiscreteStates = self.timeDiscreteStates      
      stateValue = self.stateValue      
      parValue = self.parValue
      parLocation = self.parLocation
      fmu_model = self.fmu_model
      model = self.model
    
      # Global variables
      global prevFinalTime, t, sim_res
   
      # Simulation flag
      simulationDone = False
   
      # Transfer of argument to global variable
      simulationTime = simulationTimeLocal 
      
      # Check parValue
      value_missing = 0
      for key in parValue.keys():
         if parValue[key] in [np.nan, None, '']:
            print('Value missing:', key)
            value_missing =+1
      if value_missing>0: return
         
      # Load model
      if model is None:
         model = load_fmu(fmu_model) 
      model.reset()
      
      # Run simulation
      if mode in ['Initial', 'initial', 'init']:
         # Set parameters and intial state values:
         for key in parValue.keys():
            model.set(parLocation[key],parValue[key])   
         # Simulate
         sim_res = model.simulate(final_time=simulationTime, options=options)  
         simulationDone = True
      elif mode in ['Continued', 'continued', 'cont']:

         if prevFinalTime == 0: 
            print("Error: Simulation is first done with default mode = init'")      
         else:
         
            # Set parameters and intial state values:
            for key in parValue.keys():
               model.set(parLocation[key],parValue[key])                

            for key in stateValue.keys():
               if not key[-1] == ']':
                  if key[-3:] == 'I.y': 
                     model.set(key[:-10]+'I_start', stateValue[key]) 
                  elif key[-3:] == 'D.x': 
                     model.set(key[:-10]+'D_start', stateValue[key]) 
                  else:
                     model.set(key+'_start', stateValue[key])
               elif key[-3] == '[':
                  model.set(key[:-3]+'_start'+key[-3:], stateValue[key]) 
               elif key[-4] == '[':
                  model.set(key[:-4]+'_start'+key[-4:], stateValue[key]) 
               elif key[-5] == '[':
                  model.set(key[:-5]+'_start'+key[-5:], stateValue[key]) 
               else:
                  print('The state vecotr has more than 1000 states')
                  break

            # Simulate
            sim_res = model.simulate(start_time=prevFinalTime,
                                    final_time=prevFinalTime + simulationTime,
                                    options=options) 
            simulationDone = True             
      else:
         print("Simulation mode not correct")

      if simulationDone:
    
         # Extract data
         t = sim_res['time']
 
         # Plot diagrams
         linetype = next(linecycler)    
         for command in diagrams: eval(command)
            
         # Store final state values stateValue:
         for key in list(stateValue.keys()): stateValue[key] = model.get(key)[0]        

         # Store time from where simulation will start next time
         prevFinalTime = model.time
   
      else:
         print('Error: No simulation done')

   # Describe model parts of the combined system
   def describe_parts(self, component_list=[]):
      """List all parts of the model""" 
      
      model = self.model
       
      def model_component(variable_name):
         i = 0
         name = ''
         finished = False
         if not variable_name[0] == '_':
            while not finished:
               name = name + variable_name[i]
               if i == len(variable_name)-1:
                   finished = True 
               elif variable_name[i+1] in ['.', '(']: 
                   finished = True
               else: 
                   i=i+1
         if name in ['der', 'temp_1', 'temp_2', 'temp_3', 'temp_4', 'temp_5', 'temp_6', 'temp_7']: name = ''
         return name
    
      variables = list(model.get_model_variables().keys())
        
      for i in range(len(variables)):
         component = model_component(variables[i])
         if (component not in component_list) \
         & (component not in ['','BPL', 'Customer', 'today[1]', 'today[2]', 'today[3]', 'temp_2', 'temp_3']):
            component_list.append(component)
      
      print(sorted(component_list, key=str.casefold))
   
   def describe_MSL(self):
      """List MSL version and components used"""
      
      MSL_usage = self.MSL_usage
      
      print('MSL:', MSL_usage)

   # Describe parameters and variables in the Modelica code
   def describe_general(self, name, decimals):
      
      parLocation = self.parLocation
      model = self.model
  
      if name == 'time':
         description = 'Time'
         unit = 'h'
         print(description,'[',unit,']')
      
      elif name == 'process':
         print(model.get_description())    
      
      elif name in parLocation.keys():
         description = model.get_variable_description(parLocation[name])
         value = model.get(parLocation[name])[0]
         try:
            unit = model.get_variable_unit(parLocation[name])
         except FMUException:
            unit =''
         if unit =='':
            if type(value) != np.bool_:
               print(description, ':', np.round(value, decimals))
            else:
               print(description, ':', value)            
         else:
           print(description, ':', np.round(value, decimals), '[',unit,']')
                  
      else:
         description = model.get_variable_description(name)
         value = model.get(name)[0]
         try:
            unit = model.get_variable_unit(name)
         except FMUException:
            unit =''
         if unit =='':
            if type(value) != np.bool_:
               print(description, ':', np.round(value, decimals))
            else:
               print(description, ':', value)     
         else:
            print(description, ':', np.round(value, decimals), '[',unit,']')


   # Plot process diagram
   def process_diagram(self):  
      
      fmu_model = self.fmu_model
      fmu_process_diagram = self.fmu_process_diagram
      
      try:
          process_diagram = zipfile.ZipFile(fmu_model, 'r').open('documentation/processDiagram.png')
      except KeyError:
          print('No processDiagram.png file in the FMU, but try the file on disk.')
          process_diagram = fmu_process_diagram
      try:
          plt.imshow(img.imread(process_diagram))
          plt.axis('off')
          plt.show()
      except FileNotFoundError:
          print('And no such file on disk either')

   # Describe FMU_explore commands
   def FMU_explore_info(self):
      print()
      print('Model for the process has been setup. Key commands:')
      print(' - par()       - change of parameters and initial values')
      print(' - init()      - change initial values only')
      print(' - simu()      - simulate and plot')
      print(' - newplot()   - make a new plot')
      print(' - show()      - show plot from previous simulation')
      print(' - disp()      - display parameters and initial values from the last simulation')
      print(' - describe()  - describe culture, broth, parameters, variables with values/units')
      print()
      print('Note that both disp() and describe() takes values from the last simulation')
      print('and the command process_diagram() brings up the main configuration')
      print()
      print('Brief information about a command by help(), eg help(simu)') 
      print('Key system information is listed with the command system_info()')
      
   # Dexribe framework
   def system_info(self):
      """Print system information"""
      
      model = self.model 
      MSL_version = self.MSL_version
      BPL_version = self.BPL_version 
      FMU_explore_version = self.FMU_explore_version    
      
      FMU_type = model.__class__.__name__
      print()
      print('System information')
      print(' -OS:', platform.system())
      print(' -Python:', platform.python_version())
      try:
          scipy_ver = scipy.__version__
          print(' -Scipy:',scipy_ver)
      except NameError:
          print(' -Scipy: not installed in the notebook')
      print(' -PyFMI:', version('pyfmi'))
      print(' -FMU by:', model.get_generation_tool())
      print(' -FMI:', model.get_version())
      print(' -Type:', FMU_type)
      print(' -Name:', model.get_name())
      print(' -Generated:', model.get_generation_date_and_time())
      print(' -MSL:', MSL_version)    
      print(' -Description:', BPL_version)   
      print(' -Interaction:', FMU_explore_version)
      
   # Acknowledgement
   def SDG(self, explanation=False):
     if explanation:
       print('"Soli Deo Gloria"')
       print(' It is latin and means "To the honour of God".') 
       print(' The great composer Johan Sebastian Bach used to end his compositions with this small remark SDG.')
       print(' And I like to do that too :).')    