import numpy as np
import pyDOE as pydoe
class Parameters():
    """Handles input and generation of LECs.
    
    All 
    """

    def __init__(self, interval, center_lecs, nbr_of_samples):
        """Set up parameter volume from supplied intervals.
        
        Args:
        Center_lecs - numpy array with center points which we would like to sample lecs around
        Interval - interval around the center point in parts (0 to 1 where 0.10 means 10 percent)
        nbr_of_samples - number of data points we want to generate in the volume.

        """
        

        #TODO(Erik,Daniel): fixa default center_lecs

        
        # A dictionary containing all 16 LEC:s as keys and their intervals as values in a tuple
        # (min, max, interval, +-sigma)

        # Commented out LECS are for higher order approximations.
        self.lecs_dict = {
            'Ct_1S0np': (-0.1519, -0.1464, 0.0055 , 0.002),
            'Ct_1S0pp': (-0.1512, -0.1454, 0.0058, 0.002),
            'Ct_1S0nn': (-0.1518, -0.1463, 0.0053, 0.0021),
            'C_1S0': (2.4188, 2.5476, 0.1288 ,0.0511),
            'Ct_3S1': (-0.1807, -0.1348, 0.0459, 0.0032),
            'C3S1': (0.5037, 0.7396, 0.2359 ,0.0521),
            'C_3S1-3D1': (0.2792. 0.6574, 0.3782 ,0.0428),
            'C_3P0': (0.9924, 1.6343, 0.6419, 0.0428),
            'C_1P1': (0.0618, 0.6635, 0.6017, 0.0438),
            'C_3P1': (-0.9666, -0.4724, 0.4942, 0.0438),
            'C_3P2': (-0.7941, -0.6324, 0.1617, 0.0327),
            'c_D': (0.5933, 0.8348, 0.2415, 0.0833),
            'c_E': (-2.4019, -0.0893, 2.3126, 0.2282),
            'c1': (-0.8329, 0.2784, 1.1113,0.3043),
            #'c2': (2.7946, 5.3258, 1.0754),
            'c3': (-4.3601, -3.4474, 0.9128, 0.1506),
            'c4': (1.8999, 4.2353, , 2.3354, 0.2179),
            #'d1+d2': (4.4636, 5.4505, 0.1378),
            #'d3': (-4.8549, -4.4583, 0.2302),
            #'d5': (-0.2992, 0.0233, 0.1407),
            #'d14-d15': (-10.3220, -9.6902, 0.2820),
            #'e14': (-0.3700, -9.1307, 2.4962),
            #'e15': (-11.9223, -9.1307, 2.4962),
            #'e16': (-0.6847, 7.4463, 4.2436),
            #'e17': (0.9322, 1.4896, 1.8143),
            #'e18': (-2.5068. 8.3777, 1.9022),
            }

        # Array with lec names to be used with dict above, for looping etc
        #TODO(DANIEL): Change this into something nicer and easier to work with.
        self.lecs_name = [
            'Ct_1S0np',
            'Ct_1S0pp',
            'Ct_1S0nn',
            'C_1S0',
            'Ct_3S1',
            'C3S1',
            'C_3S1-3D1',
            'C_3P0',
            'C_1P1',
            'C_3P1',
            'C_3P2',
            'c_D',
            'c_E',
            'c1',
            'c3',
            'c4',
            ]

        # Set up dimensions of sample size and lecs.
        self.nbr_of_samples = nbr_of_samples

        self.center_lecs = center_lecs.reshape(1,len(center_lecs))
        self.nbr_of_lecs = len(lec_dict.keys())

        # Array with the interval length in which each lec can vary with the current interval settings
        self.volume_length = np.zeros(nbr_of_lecs)
        for idx,name in self.lecs_name:
            self.volume_length[idx] = self.lect_dict[name][2]*self.interval
        
    def create_monospaced_lecs(self):
        # num_of_points must be an integer on the imaginary  axis

        range_list = []

        for idx,name in self.lecs_name:
            range_list.append((self.center_lecs[idx]-self.volume_length[idx]/2,
                               self.center_lecs[idx]+self.volume_length[idx]/2,
                               self.num_of_samples))
                            
        lecs_grid = np.mgrid[[slice(i,j,k) for i,j,k in range_list]].reshape(len(range_list),-1).T


                               
            
        """
        lecs_grid = np.mgrid[
            lecs_dict['Ct_1S0np'][0]:lecs_dict['Ct_1S0np'][1]:num_of_points,
            lecs_dict['Ct_1S0pp'][0]:lecs_dict['Ct_1S0pp'][1]:num_of_points,
            lecs_dict['Ct_1S0nn'][0]:lecs_dict['Ct_1S0nn'][1]:num_of_points,
            lecs_dict['C_1S0'][0]:lecs_dict['C_1S0'][1]:num_of_points,
            lecs_dict['Ct_3S1'][0]:lecs_dict['Ct_3S1'][1]:num_of_points,
            lecs_dict['C_3S1-3D1'][0]:lecs_dict['C_3S1-3D1'][1]:num_of_points,
            lecs_dict['C_3P0'][0]:lecs_dict['C_3P0'][1]:num_of_points,
            lecs_dict['C_1P1'][0]:lecs_dict['C_3PO'][1]:num_of_points,
            lecs_dict['C_3P1'][0]:lecs_dict['C_3P1'][1]:num_of_points,
            lecs_dict['C_3P2'][0]:lecs_dict['C_3P2'][1]:num_of_points,
            lecs_dict['c_D'][0]:lecs_dict['c_D'][1]:num_of_points,
            lecs_dict['c_E'][0]:lecs_dict['c_E'][1]:num_of_points,
            lecs_dict['c1'][0]:lecs_dict['c1'][1]:num_of_points,
            lecs_dict['c2'][0]:lecs_dict['c2'][1]:num_of_points,
            lecs_dict['c3'][0]:lecs_dict['c3'][1]:num_of_points,
            lecs_dict['c4'][0]:lecs_dict['c4'][1]:num_of_points,
            lecs_dict['d1+d2'][0]:lecs_dict['d1+d2'][1]:num_of_points,
            lecs_dict['d3'][0]:lecs_dict['d3'][1]:num_of_points,
            lecs_dict['d5'][0]:lecs_dict['d5'][1]:num_of_points,
            lecs_dict['d14-d15'][0]:lecs_dict['d14-d15'][1]:num_of_points,
            lecs_dict['e14'][0]:lecs_dict['e14'][1]:num_of_points,
            lecs_dict['e15'][0]:lecs_dict['e15'][1]:num_of_points,
            lecs_dict['e16'][0]:lecs_dict['e16'][1]:num_of_points,
            lecs_dict['e17'][0]:lecs_dict['e17'][1]:num_of_points,
            lecs_dict['e18'][0]:lecs_dict['e18'][1]:num_of_points,
            ].reshape(num_of_lecs,-1).T
        """
        
        return lecs_grid

    
    def create_lhs_lecs(self):
        """Returns matrix of LECS sampled using latin hypercube sampling"""
        lec_samples = pydoe.lhs(self.nbr_of_lecs, samples=self.nbr_of_samples)
        lec_min = self.center_lecs - self.volume_length

        lec_samples = 2*np.multiply(self.volume_length, lec_samples)
        for i in xrange(self._nbr_of_samples):
            lec_samples = lec_samples[:,i]

        return lec_samples
        
                               
        
        
    
    def create_random_uniform_lecs(lecs_intervals, num_of_samples):

        num_of_lecs = len(lecs_intervals.keys())
        
        # LEC_grid = np.random.uniform([vector of min values], [vector of max values], (num of
        # samples, num_of_LECs)
        
    @property
    def nbr_of_samples(self):
        return self.nbr_of_samples
    
    @nbr_of_samples.setter
    def nbr_of_samples(self, nbr_of_samples):
        self._nbr_of_samples = nbr_of_samples

    