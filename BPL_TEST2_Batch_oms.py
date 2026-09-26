# Setup data TEST2_Batch_oms 
# Author: Jan Peter Axelsson
#------------------------------------------------------------------------------------------------------------------
# 2026-09-24 - Created
#------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------
#  Framework
#------------------------------------------------------------------------------------------------------------------

# Setup framework
import platform
import locale

# Set the environment - for Linux a JSON-file in the FMU is read
if platform.system() == 'Linux': 
   locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

#------------------------------------------------------------------------------------------------------------------
#  Setup application FMU
#------------------------------------------------------------------------------------------------------------------

# Provde the right FMU and load for different platforms in user dialogue:
if platform.system() == 'Windows':
    print('Windows - run FMU pre-compiled JModelica 2.14')
    flag_vendor = 'JM'
    flag_type = 'CS'
#    fmu_model ='BPL_TEST2_Batch_windows_jm_cs.fmu'
elif platform.system() == 'Linux':
    flag_vendor = 'OM'
    flag_type = 'ME'
    if flag_vendor in ['OM','om']:
        print('Linux - run FMU pre-compiled OpenModelica')
        if flag_type in ['CS','cs']:
            fmu_model ='BPL_TEST2_Batch_linux_om_cs.fmu'
        if flag_type in ['ME','me']:
            fmu_model ='BPL_TEST2_Batch_linux_om_me.fmu'
    else:
        print('There is no FMU for this platform')


opts_std = None


  
# Provide various MSL and BPL versions
if flag_vendor in ['JM', 'jm']:
#    MSL_usage = model.get('MSL.usage')[0]
    MSL_version = model.get('MSL.version')[0]
    BPL_version = model.get('BPL.version')[0]
elif flag_vendor in ['OM', 'om']:
    MSL_usage = '4.1.0 - used components: none'
    MSL_version = '4.1.0'
    BPL_version = 'Bioprocess Library version 2.3.2'
else:    
    print('There is no FMU for this platform')

# Simulation time
simulationTime = 5.0

# Dictionary of time discrete states
timeDiscreteStates = {} 

# Define a minimal compoent list of the model as a starting point for describe('parts')
component_list_minimum = ['bioreactor', 'bioreactor.culture']

# Process diagram on disk
fmu_process_diagram ='BPL_TEST2_Batch_process_diagram_om.png'

#------------------------------------------------------------------------------------------------------------------

# Create dictionaries parValue[] and parLocation[]
parValue = {}
parValue['V_start'] = 1.0
parValue['VX_start'] = 1.0
parValue['VS_start'] = 10.0

parValue['Y'] = 0.5
parValue['qSmax'] = 1.0
parValue['Ks'] = 0.1

parLocation = {}
parLocation['V_start'] = 'bioreactor.V_start'
parLocation['VX_start'] = 'bioreactor.m_start[1]'
parLocation['VS_start'] = 'bioreactor.m_start[2]'

parLocation['Y'] = 'bioreactor.culture.Y'
parLocation['qSmax'] = 'bioreactor.culture.qSmax'
parLocation['Ks'] = 'bioreactor.culture.Ks'

# Extra only for describe()
parLocation['mu'] = 'bioreactor.culture.mu'

# Parameter value check 
parCheck = []
parCheck.append("parValue['Y'] > 0")
parCheck.append("parValue['qSmax'] > 0")
parCheck.append("parValue['Ks'] > 0")
parCheck.append("parValue['V_start'] > 0")
parCheck.append("parValue['VX_start'] >= 0")
parCheck.append("parValue['VS_start'] >= 0")

#------------------------------------------------------------------------------------------------------------------

# Create an empty list of diagrams to be plotted by simu()
diagrams = []

# Create an empty list axes to be defined in newplot() and plotted by simu() or show()
ax = []

# Create list of pens for the diagrams
lines = ['-','--',':','-.']
