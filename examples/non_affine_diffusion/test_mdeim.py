#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 10:56:42 2018

@author: Niccolo' Dal Santo
@email : niccolo.dalsanto@epfl.ch
"""

import numpy as np

import sys
sys.path.insert(0, '../../')
print(sys.path)


import pyorb_core.tpl_managers.external_engine_manager as mee

# playing around with engine manager 
my_matlab_engine_manager = mee.external_engine_manager( 'matlab', '/usr/scratch/dalsanto/EPFL/DeepLearning/feamat' )
my_matlab_engine_manager.start_engine( )
my_matlab_external_engine = my_matlab_engine_manager.get_external_engine( )


import pyorb_core.pde_problem.parameter_handler as ph

mu0_min = 0.4; mu0_max = 0.6
mu1_min = 0.4; mu1_max = 0.6
mu2_min = 0.25; mu2_max = 0.5

param_min = np.array([mu0_min, mu1_min, mu2_min])
param_max = np.array([mu0_max, mu1_max, mu2_max])
num_parameters = param_min.shape[0]

# preparing the parameter handler
my_parameter_handler = ph.Parameter_handler( )
my_parameter_handler.assign_parameters_bounds( param_min, param_max )

# define the fem problem 
import nonaffine_diffusion_problem as ndp

my_ndp = ndp.nonaffine_diffusion_problem( my_parameter_handler )

fem_size = 20
fem_size_str = str( fem_size )

fom_specifics = { 
        'number_of_elements': fem_size, 
        'polynomial_degree' : 'P1',
        'model': 'nonaffine' }

my_ndp.configure_fom( my_matlab_external_engine, fom_specifics )

import pyorb_core.rb_library.m_deim as m_deim
my_mdeim = m_deim.Mdeim( my_ndp )

base_offline_folder = 'offline/'

my_mdeim.set_save_offline( True, base_offline_folder )
my_mdeim.perform_mdeim( 20, 10**(-2) )

my_mdeim.compute_theta_coefficients( param_min )

my_mdeim.print_reduced_indices( )
my_mdeim.print_reduced_indices_mat( )
my_mdeim.print_reduced_elements( )


my_mdeim_2 = m_deim.Mdeim( my_ndp )
my_mdeim_2.load_offline( base_offline_folder )
my_mdeim_2.print_reduced_indices( )
my_mdeim_2.print_reduced_indices_mat( )
my_mdeim_2.print_reduced_elements( )
my_mdeim_2.compute_theta_coefficients( param_min )

A = my_ndp.assemble_fom_matrix( param_min )
AA_mu_min = np.array(  A['A'] )
AA_mu_min = AA_mu_min[:, 2]

theta = my_mdeim.compute_theta_coefficients( param_min )

approximated_AA_mu_min = my_mdeim.get_basis( ).dot( theta )

error_AA_mu_min = AA_mu_min - approximated_AA_mu_min

error_norm = np.sqrt( np.sum( error_AA_mu_min * error_AA_mu_min ) / np.sum( AA_mu_min * AA_mu_min ) )

print( 'error  while approximating AA_mu_min is %f' % error_norm )

my_mdeim.compute_theta_bounds( 3 )



## Check whether deim works wihtin the fom problem once it is set

my_ndp.set_mdeim( my_mdeim )

my_mdeim.compute_theta_coefficients_q( param_min, 1 )

my_ndp.get_theta_a( param_min, 1 )

