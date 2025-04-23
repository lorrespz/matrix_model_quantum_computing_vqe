# Code written by HLD for the work arXiv: 2503.13368 [quant-ph, hep-th]
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import warnings
warnings.filterwarnings('ignore')

def load_drop(link, drop = True):
	df = pd.read_csv(link)
	if drop:
		df.drop(['Unnamed: 0', 'ev_op_H40', 'ev_op_Hp40_2f'], axis = 1, inplace=True)
	else:
		df.drop(['Unnamed: 0'], axis = 1, inplace=True)
	return df

class EvOpAnsatz_data_collate():
	"""
	ll: The lambda coupling constant of the SU2 matrix model
	df_c_seed_1, df_c_seed_2: full values of VQE runs using COBYLA optimizers at 2 different seeds
	df_s_seed_1, df_s_seed_2: full values of VQE runs using SPSA optimizers at 2 different seeds
	returns:
	df_l_best: A new df files containing the last values 
	df_c_best: A new df files containing the best full values for COBYLA optimizer
	df_s_best: A new df files containing the best full values for SPSA optimizer
	"""
	def __init__(self, df_c_seed_1, df_c_seed_2, df_s_seed_1, df_s_seed_2, seed_1, seed_2, Ee, ll):
		self.df_c_s1 = df_c_seed_1
		self.df_c_s2 = df_c_seed_2
		self.df_s_s1 = df_s_seed_1
		self.df_s_s2 = df_s_seed_2
		self.s1 = seed_1
		self.s2 = seed_2
		self.E = Ee
		self.ll = ll
		self.df_l1_name = f'seed_{self.s1}'
		self.df_l2_name = f'seed_{self.s2}'

		self.df_last_s1 = self.create_df_last_val(self.df_s_s1, self.df_c_s1, self.s1)
		self.df_last_s2 = self.create_df_last_val(self.df_s_s2, self.df_c_s2, self.s2)
		self.df_last_best, self.cc_lc, self.cc_ls = self.create_best_df_last_val(self.df_last_s1, self.df_last_s2)

		self.df_c_best = self.merge_data_cc(self.df_c_s1, self.df_c_s2, self.cc_lc)
		self.df_s_best = self.merge_data_cc(self.df_s_s1, self.df_s_s2, self.cc_ls)

	def get_last_val(self,df):
	    val_list = []
	    name_list = []
	    for i in range(len(df.columns)):
	        lv = df[df.columns[i]].dropna().to_numpy()[-1]
	        val_list.append(np.round(lv,5))
	        name_list.append(df.columns[i])
	    return name_list, val_list
	        
	def create_df_last_val(self, df_s, df_c, seed): 
	    ns1, vs1 = self.get_last_val(df_s)
	    nc1, vc1 = self.get_last_val(df_c)
	    df = pd.DataFrame({'name': ns1, 'cobyla_values': vc1, 'spsa_values': vs1})
	    df.set_index('name', inplace = True)
	    df_name =f'results_tests/l{self.ll}_last_val_{seed}.csv'
	    df.to_csv(df_name)
	    print(f'file saved as {df_name}')
	    return df

	def merge_best_val(self, df_l1, df_l2, column_name):
	    new_values = []
	    dc_1 = df_l1[column_name] - self.E
	    dc_2 = df_l2[column_name]  - self.E
	    df_curve_list = []
	    for i in range(len(dc_1)):
	        if dc_1[i] < 0 and dc_2[i] >0:
	            new_values.append(df_l2[column_name][i])
	            print(f'{df_l1.index[i]}: {self.df_l2_name}')
	            df_curve_list.append((df_l1.index[i], self.df_l2_name))
	            
	        if dc_1[i] > 0 and dc_2[i] < 0:
	            new_values.append(df_l1[column_name][i])
	            print(f'{df_l1.index[i]}: {self.df_l1_name}')
	            df_curve_list.append((df_l1.index[i], self.df_l1_name))
	            
	        if (dc_1[i] < 0 and dc_2[i] <0) or (dc_1[i]>0 and dc_2[i] >0):
	            if np.abs(dc_1[i])< np.abs(dc_2[i]):
	                new_values.append(df_l1[column_name][i])
	                print(f'{df_l1.index[i]}: {self.df_l1_name}')
	                df_curve_list.append((df_l1.index[i], self.df_l1_name))
	            else:
	                new_values.append(df_l2[column_name][i])
	                print(f'{df_l1.index[i]}: {self.df_l2_name}')
	                df_curve_list.append((df_l1.index[i], self.df_l2_name))
	    return new_values, df_curve_list

	def create_best_df_last_val(self, df1, df2):
	    print(f'Checking COBYLA column')
	    new_cobyla_vals, cc_lc = self.merge_best_val(df1, df2, 'cobyla_values')
	    print(f'Checking SPSA column')
	    new_spsa_vals, cc_ls = self.merge_best_val(df1, df2, 'spsa_values')
	    df = pd.DataFrame({'name': df1.index, 'cobyla_values': new_cobyla_vals, 'spsa_values': new_spsa_vals})
	    df.set_index('name', inplace = True)
	    df_name = f'results_tests/l{self.ll}_last_val_best.csv'
	    df.to_csv(df_name)
	    print(f'file saved as {df_name}')
	    return df, cc_lc, cc_ls

	def merge_data_cc(self, df_v1, df_v2, cc_l):
	    curve_list =[]
	    for i in range(len(cc_l)):
	        if cc_l[i][1][5:] == f'{self.s1}':
	            curve_list.append(df_v1[cc_l[i][0]])
	        if cc_l[i][1][5:] == f'{self.s2}':
	            curve_list.append(df_v2[cc_l[i][0]])
	        df = pd.concat(curve_list, axis = 1)
	    return df    