"""
Main script to run simulation
"""
import time

import compartment
import simulator2
import pandas as pd
import h5py

file_name = "test"
# 1) CREATE COMPARTMENTS:
comp1 = compartment.Compartment("Comp1")
comp1.set_ion_properties()
comp2 = compartment.Compartment("Comp2")
comp2.set_ion_properties()
comp3 = compartment.Compartment("Comp3")
comp3.set_ion_properties()


# 2) DEFINE SIMULATOR CLASS AND ADD COMPARTMENTS
sim = simulator2.simulator(file_name)
sim.add_compartment(comp1)
sim.add_compartment(comp2)
sim.add_compartment(comp3)

#print(sim.df_comps)

#df1 = sim.hdf.get("COMPARTMENTS")



# 3) SET SIMULATION SETTINGS
sim.set_electrodiffusion_properties(ED_on=True)


sim.set_external_ion_properties()
sim.set_j_atp(constant_j_atp=False)
sim.set_area_scale(constant_ar=False)
total_t =600
time_step =0.001*1e-3
sim.set_timing(total_t=10, time_step=1e-6, intervals=1000)

#sim.set_xflux(comps=["Comp2"], flux_type="dynamic", start_t=0.2, end_t=0.8, x_conc=1e-7, z=-1.0)
# sim.set_zflux()
##sim.set_xoflux()
#run_t_arr = np.arange[0:total_t:time_step]

sim.run_simulation()
print("fin")
# 4) RUN SIMULATION
"""

sim.start_t = time.time()
while sim.run_t <=sim.start_t:
    sim.run_simulation()

print(sim.output_arr)
#]print(sim.output_intervals)
print(sim.run_t)
"""


# 5) ACCESS RESULTS

