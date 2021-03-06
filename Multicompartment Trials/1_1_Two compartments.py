# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 14:46:28 2020

@author: eshor

This trial is simply to see if I can model diffusion and drift between two compartments
Each compartment will have the same pump and leak mechanisms as in the single compartment.
The only difference will be incorporating electrodiffusion

"""
import numpy as np
from constants import F
from common import default_radius, default_length, \
    clo, ko, nao, xo_z, oso, \
    default_p, \
    gk, gna, gcl, \
    ck, cna, \
    pw, vw, km, \
    RTF, RT

class Compartment():
    
    def __init__(self, name, radius = default_radius, length=default_length, pkcc2 = 2e-3/F, z = -0.85, p=default_p):
      self.name = name
      self.radius = radius #in um
      self.length = length #in um
      self.w = (np.pi)*(self.radius**2)*self.length
      self.w_temp = self.w
      self.sa = 2*(np.pi)*(self.radius)*(self.length)
      self.ar = self.sa / self.w
      self.C = 2e-4
      self.FinvCAr = F /(self.C *self.Ar)
      self.p_kcc2 = pkcc2
      self.p = p
     
    def set_ion_properties(self, na_i = 0.033, k_i = 0.1038, cl_i = 0.0052, x_i = 0,z_i=-0.85, g_x =0e-9 ):
      
      # A) Intracellular ion properties:
      self.na_i = na_i
      self.k_i = k_i
      self.cl_i = cl_i 
      self.x_i = x_i 
      self.z = z_i
      if cl_i == 0:
            # setting chloride that is osmo- and electro-neutral initially.
            self.cl_i = (oso + (self.na_i + self.k_i) * (1 / self.z_i - 1)) / (1 + self.z_i)
      
      if self.k_i == 0:
            self.x_i = 155.858e-3
            self.k_i = self.cl_i-self.z_i*self.x_i-self.na_i
      else:
            self.x_i = (self.cl_i - self.k_i - self.na_i) / self.z_i 
            
      self.g_x = g_x #basically 0 ... therefore impermeant
      
          
      if self.x_i < 0 or self.cl_i < 0:
          raise Exception("""Initial choice of either ki or nai resulted in negative concentration of
                                    intracellular ion - choose different starting values.""") 
                                    
      # B) Osmolality:
      self.osm_i = self.na_i + self.k_i + self.cl_i + self.x_i
      self.osm_o = oso
      if self.osm_i != self.osm_o:
          print("Compartement {} not osmo-neutral".format(self.name))
                              
      # C) Extracellular ion properties:
      self.na_o = nao
      self.k_o = ko
      self.cl_o = clo 
      
      # D) Zeroing Delta values
      self.d_na_i = 0
      self.d_k_i = 0
      self.d_cl_i = 0
      self.d_x_i = 0
      self.d_z = 0
        
    def calc_voltages(self):
        
        self.V=self.FinvCAr * (self.na_i + self.k_i + (self.z_i*self.x_i) - self.cl_i)
        self.E_k = RTF * np.log(self.k_o / self.k_i)
        self.E_cl = RTF * np.log(self.cl_i / self.cl_o)
        self.j_kcc2 = self.p_kcc2 * (self.E_k - self.E_cl)  # Doyon
        self.j_p = self.p * (self.na_i / self.na_o) ** 3