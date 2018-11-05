#!/usr/bin/python
# -*- coding: UTF-8 -*-

import matplotlib.pyplot as plt
import numpy as np

def desenha(y,ic,ymax,title):

	x = np.arange(len(y))
	bar_width = 0.5

	fig,ax = plt.subplots()

	ps,pt,pe,pi = plt.bar(x,y,width=bar_width,align='center',yerr=ic,ecolor='black')
	ps.set_facecolor('m')
	ps.set_edgecolor('m')
	pt.set_facecolor('y')
	pt.set_edgecolor('y')
	pe.set_facecolor('c')
	pe.set_edgecolor('c')
	pi.set_facecolor('b')
	pi.set_edgecolor('b')

	ax.set_xticks(x)
	ax.set_xticklabels(['stp', 'traffic', 'ecmp', 'isolated'],fontsize=28)
	ax.set_ylim([0,ymax])
	ax.set_ylabel(u'Tempo (s)',fontsize=28)
	ax.tick_params(axis='y',labelsize=20,right='off')
	ax.tick_params(axis='x',top='off')
	ax.set_title(title,fontsize=18)

	plt.show()
