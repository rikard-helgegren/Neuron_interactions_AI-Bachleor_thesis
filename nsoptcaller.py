from resources import python_nsopt
import numpy as np
import os
from matplotlib import pyplot as plt
import sys
import ConfigParser
import StringIO


# Init files and path to nsopt
PATH_LIBNSOPT = b'/net/home/andeks/software/nsopt/nucleon-scattering/libs/libnsopt.so.1.8.78.ml'
PATH_INIFILES = b'/'

class NsoptCaller:
    '''
    Rewriting this as a class

    The idea is that we use separate files for the physical problems, working something like:
    Generate data (with this class) -> Save data -> Use Gaussfit to fit GP -> analyze ....
    //Martin
    '''

    def __init__(self):
        '''Defining class variables'''
        self.energies = None
        self.observable = None

    def read_ini(self, args):
        """Reads .ini-file line by line and determines input arguments."""
        

        # Preparing and opening init file "set_parameters"
        config_set = StringIO.StringIO()
        config_set.write(open('resources/set_parameters.ini').read())
        config_set.seek(0, os.SEEK_SET)

        cp_set = ConfigParser.ConfigParser()
        cp_set.readfp(config_set)
        
        # Read and store the desiered lines
        txt_set = open('resources/set_parameters.ini', 'r')
        txt='[section]\n'
        for line in txt_set:
            if 'evaluate_exsec' in line: break # takes me to the line containg "evaluate_exsec" 
        
        for line in txt_set:
            if 'evaluate_ncsm' in line: break # saves the line until "evaluate_ncsm"
            txt += line
        
        # Replace the content of evaluate_exsec.ini with the desired lines.
        txt_exsec = open('resources/evaluate_exsec.ini', 'w')
        txt_exsec.write(txt)
        
        
        # Read and store the desiered lines
        txt_set = open('resources/set_parameters.ini', 'r')
        txt='[section]\n'
        for line in txt_set:
            if 'evaluate_ncsm' in line: break # takes me to the line containg "evaluate_ncsm" 
        
        for line in txt_set:
            txt += line
        
        # Replace the content of evaluate_exsec.ini with the desired lines.
        txt_ncsm = open('resources/evaluate_ncsm.ini', 'w')
        txt_ncsm.write(txt)



        # TODO(DANIEL/ERIK): Add functionality to use different .ini-files
        config = StringIO.StringIO()
        config.write(open('resources/evaluate_xsec.ini').read())
        config.seek(0, os.SEEK_SET)
    
        cp = ConfigParser.ConfigParser()
        cp.readfp(config)
    
        observable = cp.get('section','observable')

        # List of input energies
        Elist = None

        # tries to read Elist
        try:
            Elist = cp.get('section','Elist')
            Elist = np.fromstring(Elist,sep=" ")
            Elist = Elist[1:]
        except ConfigParser.NoOptionError:
            print "No Elist entry"

        # tries to read Emin, Emax, Esteps
        if Elist is None:
            try:
                Emin = cp.getfloat('section','Emin')
                Emax = cp.getfloat('section','Emax')
                Esteps = cp.getint('section','Esteps')
            except ConfigParser.NoOptionError:
                print "No entries for Emin, Emax or Esteps"

        if args.nsopt:
            if observable == "SGT":
                if Elist is not None:
                    X = Elist
                    X = X.reshape(len(Elist),1)
                else:
                    X = np.linspace(Emin,Emax,Esteps)
                    X = X.reshape(Esteps, 1)
                    #print "X from Emin, Emax, Esteps"
        else:
            X = np.random.uniform(-3.,3.,(20,1))
        
        self.energies = X
        return X
    
   
    def get_nsopt_observable(self, LECM=None):    
        """
        Takes a matrix of LECs LECM and calls nsopt to calculate the observable. Each row in LECM is a
        set of LECs. Returns nsopt_observable where each row corresponds to a different set of LECs.
        Reads a set of default LEC values if no LECM is given.
        """

        # sets default LECM
        if LECM is None:
            pot = 'N2LOsim'
            lam = 500
            cut = 290

            # remove some LECs from analysis
            removed_LECs = (14,17,18,19,20,21,22,23,24,25)

            # reads 1 set of default LEC-values from text file
            LECM = np.loadtxt(b'./resources/%s-%d-%d.LEC_values.txt' %(pot,lam,cut) )
            LECM = np.delete(LECM,removed_LECs)

        # makes LECM 2D array if it is 1D array to work with code
        if len(LECM.shape) == 1:
            LECM = LECM.reshape(1,-1)

        evaluate = 'include evaluate_xsec.ini'
        # evaluate = 'include evaluate_ncsm.ini'
        nsopt = python_nsopt.PythonNsopt(PATH_LIBNSOPT, PATH_INIFILES, ini_string=evaluate)

        # calls nsopt for each set of LECs in LECM
        for i in range(len(LECM)):
            temp = nsopt.calculate_observable(LECM[i,:])

            if i == 0:
                nsopt_observables = temp
            else:
                nsopt_observables = np.vstack((nsopt_observable, temp))
        

            #print nsopt_observables
    
        nsopt.terminate()

        self.observable = nsopt_observables
        return nsopt_observables
    
#if __name__ == '__main__':
#    ml = ml2017()
#    ml.main()
