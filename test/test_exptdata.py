
"""
Tests: src/python/exptdata.py
"""

from odin import exptdata
from odin.testing import skip, ref_file, expected_failure
from mdtraj import trajectory, io

import numpy as np
from numpy.testing import (assert_almost_equal, assert_array_almost_equal, 
                           assert_allclose, assert_array_equal)

class TestDistanceRestraint(object):
    
    # note that the DistanceRestraint class is super simple (though useful!),
    # to the extent that this test should also provide an easy way to test all
    # the underlying functionality of the ExptData abstract base class
    
    def setup(self):
        
        self.t = trajectory.load( ref_file('ala2.pdb') )
        
        # make a fake restraint array
        self.restraint_array = np.zeros((2,4))
        self.restraint_array[0,:] = np.array([0, 5,   1.0, 1])
        self.restraint_array[1,:] = np.array([4, 10, 10.0, 0])
        
        self.dr = exptdata.DistanceRestraint(self.restraint_array)
        
    def test_num_data(self):
        assert self.dr.num_data == 2
    
    def test_values(self):
        values = self.dr.values
        assert_array_almost_equal( self.dr.values, self.restraint_array[:,3] )
    
    def test_prediction(self):
        # these values were checked out by TJL and deemed sane
        assert_array_equal( np.array([[ 0., 1.]]), self.dr.predict(self.t) )
        
    # def test_log_likelihood(self):
    #     # only smoke right now
    #     print self.dr.log_likelihood(self.t)
    #     
    # def test_prediction_log_likelihood(self):
    #     prediction = self.dr.predict(self.t)
    #     pll = self.dr.prediction_log_likelihood(prediction)
    #     ll  = self.dr.log_likelihood(self.t)
    #     assert_array_almost_equal(pll, ll)
    # 
    # def test_errors(self):
    #     # smoke test only right now
    #     err = self.dr.errors
    #     assert len(err) == self.dr.num_data
    # 
    # def test_default_error(self):
    #     assert_array_almost_equal( self.dr.errors, self.dr._default_error() )
    
    def test_load(self):
        dr2 = exptdata.DistanceRestraint.load( ref_file('exptdata_ref.dat') )
        assert_array_equal(dr2.values, self.dr.values)
        