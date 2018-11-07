#!/usr/bin/python
# -*- coding: UTF-8 -*-

import matplotlib.pyplot as plt
import numpy as np

def desenha(y,ic,ymax,title, teste):
	teste = teste
	x = np.arange(len(y))
	bar_width = 0.5

	fig,ax = plt.subplots()

	if teste == 'SemIperf':
		ps,pt = plt.bar(x,y,width=bar_width,align='center',yerr=ic,ecolor='black')
		ps.set_facecolor('m')
		ps.set_edgecolor('m')
		pt.set_facecolor('y')
		pt.set_edgecolor('y')
		ax.set_xticklabels(['Entrada\nVideo', 'Saida\nVideo'],fontsize=12)
	elif teste == '1Iperf':
		ps,pt,pe,pi = plt.bar(x,y,width=bar_width,align='center',yerr=ic,ecolor='black')
		ps.set_facecolor('m')
		ps.set_edgecolor('m')
		pt.set_facecolor('y')
		pt.set_edgecolor('y')
		pe.set_facecolor('c')
		pe.set_edgecolor('c')
		pi.set_facecolor('b')
		pi.set_edgecolor('b')
		ax.set_xticklabels(['Entrada\nVideo', 'Saida\nVideo', 'Entrada\nIperf', 'Saida\nIperf 1'],fontsize=12)
	else:
		ps,pt,pe,pi,pa = plt.bar(x,y,width=bar_width,align='center',yerr=ic,ecolor='black')
		ps.set_facecolor('m')
		ps.set_edgecolor('m')
		pt.set_facecolor('y')
		pt.set_edgecolor('y')
		pe.set_facecolor('c')
		pe.set_edgecolor('c')
		pi.set_facecolor('b')
		pi.set_edgecolor('b')
		pa.set_facecolor('g')
		pa.set_edgecolor('g')
		ax.set_xticklabels(['Entrada\nVideo', 'Saida\nVideo', 'Entrada\nIperf', 'Saida\nIperf 1','Saida\nIperf 2'],fontsize=12)

	ax.set_xticks(x)
	ax.set_ylim([0,ymax])
	ax.set_ylabel(u'Megabits',fontsize=15)
	ax.tick_params(axis='y',labelsize=13,right='off')
	ax.tick_params(axis='x',top='off')
	ax.set_title(title,fontsize=18)

	plt.show()
