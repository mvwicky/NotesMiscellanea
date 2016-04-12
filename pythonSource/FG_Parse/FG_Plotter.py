import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

from logger import Logger

class FG_Plotter(object):
	def __init__(self, file_name, p_tup):
		self.log = Logger('FG_Plotter')
		if not file_name.endswith('.csv'):
			self.log('Input file is not a csv', ex=True)
		self.file_name = file_name
		self.p_tup = p_tup

	def per_game(self, stat, year=None):
		dates = []
		stats = []
		with open(self.file_name, 'rt') as game_logs:
			for row in game_logs:
				fields = row.replace('"', '').split(',')
				if row.startswith('Date'):
					if stat not in fields:
						self.log('Not a supported stat')
						self.log('Supported stats are: {}'.format(fields), ex=True)
					else:
						stat_ind = fields.index(stat)
					continue
				if row.startswith('Total'):
					continue
				d = fields[0].split('-')
				c_date = datetime.date(int(d[0]), int(d[1]), int(d[2]))
				if year and c_date.year == year:
					dates.insert(0, c_date)
					stats.insert(0, fields[stat_ind])
				elif not year:
					dates.insert(0, c_date)
					stats.insert(0, fields[stat_ind])
		plt.close()
		plt.plot(dates, stats, 'r.')
		plt.title('{} per game {}'.format(p_tup[1], stat))
		plt.grid()
		plt.savefig('{}PerGame_{}.png'.format(p_tup[0], stat), bbox_inches='tight')

	def cum_avg(self, stat):
		pass

def main():
	pass

if __name__=='__main__':
	main()