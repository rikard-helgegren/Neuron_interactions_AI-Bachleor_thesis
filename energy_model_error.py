import sys
from parameters import Parameters
from nsoptcaller import NsoptCaller
from gaussfit import Gaussfit
from datamanager import Datamanager
from memory_profiler import profile
import numpy as np
import pickle

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import style
from matplotlib2tikz import save as tikz_save
from os import listdir
from os.path import isfile, join
from shutil import move, copyfile
from matplotlib import pyplot as plt
from matplotlib import style


# The kernels we have trained for
kernels = ['RBF', 'Exponential', 'Matern32', 'Matern52']

gauss = Gaussfit()
dm = Datamanager(echo=False)

def calculate_valid(val_lecs):
    """Wrapper function to measure time with memory profiler."""
    mod_obs, mod_var = gauss.calculate_valid(val_lecs)
    return mod_obs, mod_var

LEC_LENGTH = 16
RBF_error = []
Exponential_error = []
Matern32_error = []
Matern52_error = []
samples = range(100, 3001, 100)

# Kernel loop
for kernel in kernels:
    for training_number in xrange(100, 3001, 100):
        
        params_load_path = '/net/data1/ml2017/gpyparams/valid100-3000/' + kernel + '_validation_' + str(training_number) + '_memcenter100lhs_sgt50.pickle'

        with open(params_load_path, 'r') as f:
            tagsidx = 2
            training_tags = pickle.load(f)[tagsidx]



        train_obs = np.array([0])
        train_energy = np.array([0])
        train_lecs = np.array(np.zeros(LEC_LENGTH))

        #Read database data with the specified tags
        for row in dm.read(training_tags):
            train_obs = np.vstack((train_obs, row.observable))
            train_energy = np.vstack((train_energy, row.energy))
            train_lecs = np.vstack((train_lecs, row.LECs))

        # Clean up initialized zeros
        train_obs = np.delete(train_obs, 0, 0)
        train_energy = np.delete(train_energy, 0, 0)
        train_lecs = np.delete(train_lecs, 0, 0)
        
        gauss.load_model_parameters(train_obs, train_lecs, params_load_path)

        model_error = 0


        # Loop over all validation
        for validation_number in xrange(1, 2):

            validation_tags = ['sgt50', 'training3000','mem_center_100%_lhs_lecs']

            val_obs = np.array([0])
            val_energy = np.array([0])
            val_lecs = np.array(np.zeros(LEC_LENGTH))
    
            #validation_tags[1] = 'validation' + str(sample)
            for row in dm.read(validation_tags):
                val_obs = np.vstack((val_obs, row.observable))
                val_energy = np.vstack((val_energy, row.energy))
                val_lecs = np.vstack((val_lecs, row.LECs))
                
            val_obs = np.delete(val_obs, 0, 0)
            val_energy = np.delete(val_energy, 0, 0)
            val_lecs = np.delete(val_lecs, 0,0)

            mod_obs, mod_var = calculate_valid(val_lecs)

            model_error += gauss.get_model_error(mod_obs, val_obs)

            print('Completed ' + kernel + ' training ' + str(training_number) + ' validation ' + str(validation_number) + '/50')

        if kernel == 'RBF':
            RBF_error.append(model_error)
            
        if kernel == 'Exponential':
            Exponential_error.append(model_error)

        if kernel == 'Matern32':
            Matern32_error.append(model_error)

        if kernel == 'Matern52':
            Matern52_error.append(model_error)
        

print(RBF_error)
print(Exponential_error)
print(Matern32_error)
print(Matern52_error)


# fig = plt.figure()
# style.use('seaborn-bright')
# plt.figure(1)


# plt.plot(samples, RBF_error, label='RBF')
# plt.plot(samples, Matern52_error, label='Matern52')
# plt.legend(loc='upper left')
# plt.xlabel('Number of sample points')   #****Edit****
# plt.ylabel('Model error')   #****Edit****
# plt.grid(True)
# #plt.show()


# fileName = 'energy_error.tex'
# save_path = '/net/home/dakarlss/ml2017'

# #The folowing saves the file to folder as well as adding 3 rows. 
# #The "clip mode=individual" was a bit tricky to add so this is the ugly way to solve it.
# tikz_save(save_path + '/' + fileName, 
#           figureheight = '\\textwidth*0.8,\nclip mode=individual',
#           figurewidth = '\\textwidth*0.8')
    
# #Last fix of tikz.
# from fix_tikz import EditText
# edit = EditText()
# #Making transformable to PNG
# edit.fix_file(save_path + '/' + fileName, '% This file was created by matplotlib2tikz v0.6.3.', '\documentclass{standalone}\n\usepackage{tikz}\n\usepackage{pgfplots}\n\usepackage{siunitx}\n\n\\begin{document}')
        
# edit.fix_file(save_path + '/' + fileName, '\end{document}', '')
# edit.fix_file(save_path + '/' + fileName, '\end{tikzpicture}', '\end{tikzpicture}\n\end{document}')




            


