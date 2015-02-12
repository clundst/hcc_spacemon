#!/usr/bin/python

#Need to format fsimage from hadoop for spacemon

import os, sys, getopt
from datetime import *

# take the RAW fsimage given from hadoop 
# -i <input image file>

def get_checksum(file):
	checksum = "N/A"
	cksum_data = [0,0]
	if os.path.isfile(file):
		cksum_file = open(file,'r')
		for line in cksum_file:
			if line.find("CKSUM") != -1:
				cksum_data = line.split(":")
				if len(cksum_data) == 2:
					print "cksum_data, length = ", cksum_data, len(cksum_data)
					checksum = int(cksum_data[1])		
				#print "line, cksum_data, length =", line, cksum_data, len(cksum_data)
		cksum_file.close()
	return checksum 
def main(argv):
	inputfile = ''
	outputfile = ''
	filename=''
	filesize=''
	total_seconds = 0
	unix_second = datetime(1970,1,1)
	checksum_file = ""
	try:
		opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
	except getopt.GetoptError:
		print 'test.py -i <inputfile> -o <outputfile>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'test.py -i <inputfile> -o <outputfile>'
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg
	print 'Input file is ', inputfile
	print 'Output file is ', outputfile
	formatted_file = open(outputfile,'w')
	for row in  open(inputfile,'r'):
		interesting_file = True
		checksum = "N/A"
		data = row.split()
		if len(data) == 8:
			if row.find("chukwa") != -1:
				interesting_file = False
			if data[7].find(".") == -1:
				interesting_file = False
			if row.find("cksums") != -1:
				interesting_file = False
			if interesting_file :
				filename = "/mnt/hadoop"+data[7]
				checksum_file = "/mnt/hadoop/cksums"+data[7]
				checksum = get_checksum(checksum_file)
				filesize = data[4]
				date = datetime.strptime(data[5]+" "+data[6],'%Y-%m-%d %H:%M')	
				days, seconds = (date - unix_second).days, (date - unix_second).seconds
				total_seconds = days * 24 * 3600 + seconds
				print >> formatted_file, filename, " | ", filesize , " | ", total_seconds, " | ", checksum
	
	formatted_file.close()

if __name__ == "__main__":
   main(sys.argv[1:])
