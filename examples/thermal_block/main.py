#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 10:24:47 2018

@author: Niccolo' Dal Santo
@email : niccolo.dalsanto@epfl.ch
"""

#%%

import numpy as np

import sys
sys.path.insert(0, '../../core')

import rb_manager as rm
import affine_decomposition as ad
import parameter_handler as ph

print( rm.__doc__ )


mu0_min = 1.0; mu0_max = 50.
mu1_min = 1.0; mu1_max = 50.
mu2_min = 1.0; mu2_max = 50.

param_min = np.array([mu0_min, mu1_min, mu2_min])
param_max = np.array([mu0_max, mu1_max, mu2_max])
num_parameters = param_min.shape[0]


my_parameter_handler = ph.Parameter_handler( )
my_parameter_handler.assign_parameters_bounds( param_min, param_max )

my_affine_decomposition = ad.AffineDecompositionHandler( )
my_affine_decomposition.set_Q( 4, 1 )                   # number of affine terms
my_affine_decomposition.import_affine_matrices( 'affine_matrix_A' )
my_affine_decomposition.import_affine_vectors(  'affine_vector_f' )


my_rb_manager = rm.RbManager( )
my_rb_manager.set_affine_decomposition_handler( my_affine_decomposition )

snapshots_file = 'train_snapshots_matrix_20_50.txt'
my_rb_manager.import_snapshots_matrix( snapshots_file )

#my_rb_manager.set_save_basis_functions( True, "basis.txt" )
my_rb_manager.build_rb_approximation( 10**(-4) )




my_rb_manager.print_rb_summary( )

