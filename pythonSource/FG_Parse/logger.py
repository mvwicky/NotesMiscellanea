from sys import stdout 
from datetime import datetime

class Logger(object):
	'''class that logs output to a log file and stdout'''
	def __init__(self, name,attr=None, ovrw=False):
		'''Constructor
		   name: the name for the log file 
		   attr: an optional additional name for the file
		   ovrw: whether or not to overwrite and existing file
		'''
		year = datetime.today().year 
		month = datetime.today().month 
		day = datetime.today().day
		today = '{}-{}-{}'.format(year, month, day)

		if attr is None: # use just script name
			self.logName = '{}_{}.log'.format(name, today)
		else: # use script name and type
			self.logName = '{}_{}_{}.log'.format(name, attr, today) 

		if ovrw:
			log = open(self.logName, 'w')
			log.close()
	def __call__(self, msg, ex=False, exitCode=-1):
		'''writes msg to log file and stdout 
		   msg: message to log 
		   ex: whether or not to exit 
		   exitCode: the exit code to emit, unused if not exiting 
		'''
		msg = str(msg)
		stdout.write('{}\r\n'.format(msg))
		stdout.flush()
		now = datetime.now().strftime("%X")
		with open(self.logName, 'a') as log:
			log.write('{} -> {}\r\n'.format(now, msg))
			log.flush()
		if ex:
			exitMessage = 'Exiting with code: {}'.format(exitCode)
			stdout.write('{}\r\n'.format(exitMessage))
			stdout.flush()
			with open(self.logName, 'a') as log:
				log.write('{} -> {}\r\n'.format(now, exitMessage))
				log.flush()
			exit(exitCode)



def main():
	pass

if __name__ == '__main__':
	main()
