from lib.miXMLparser import Interactor, Source, ExperimentDescription, Interaction
import xml.etree.ElementTree as ET
from itertools import combinations
import pandas as pd
import sys
import re
# Define the namespace dictionary based on the MIF300 schema
namespace = {
    'xs': 'http://www.w3.org/2001/XMLSchema',
    'mif': 'http://psi.hupo.org/mi/mif300'
}
try:
  inp_index = sys.argv.index('-in')
except ValueError:
  print("-in argument not found")
  exit(1)

if(inp_index == len(sys.argv)-1):
	print("Define input files: -in <inp_1.xml> ... <inp_n.xml>")
	exit(1)

for i in range(inp_index+1, len(sys.argv)):
	
	file = sys.argv[i]
	
	print(f'Generating FASTA file from {file}')

	out_file = re.sub(".xml", ".fasta", file)
	
	open(f'{out_file}', 'w').close()
	
	f = open(f'{out_file}', "a")
	
	root = (ET.parse(file)).getroot()
	
	dictor = {}
	
	for entry in root.findall('.//mif:entry', namespaces=namespace):

		for interactor in entry.findall('./mif:interactorList/mif:interactor',
		 namespaces=namespace):
			
			inter = Interactor(interactor)
			header = ">" + inter.pxref + "\n"
			seq = inter.sequence + "\n"
			
			if seq != "N/A\n":
				dictor[header] = seq
		
	for header in dictor.keys():
		f.write(header + dictor[header])

	f.close()
print("FASTA files successfully generated!")