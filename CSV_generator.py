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

# GENERATE CSV FILE
# file = 'ecoli_83333_01.xml'
for i in range(inp_index+1, len(sys.argv)):
	file = sys.argv[i]
	print(f'Generating CSV file from {file}')

	root = (ET.parse(file)).getroot()
	it = 0
	df = pd.DataFrame(columns=['Molecule A',
								'Molecule B',
								'Identifier A',
								'Identifier B',
								'Type A','Type B',
								'Species A',
								'Species B',
								'Host Organism',
								'Detection Method',
								'Publication IDs',
								'Interaction Type',
								'Interaction AC',
								'Database',
								'Experimental Role A',
								'Experimental Role B',
								'Biological Role A',
								'Biological Role B',
								'Stoichiometry A',
								'Stoichiometry B'])

	for entry in root.findall('.//mif:entry', namespaces=namespace):
		interactorDict = {}
		experimentDict = {}
		interactionDict = {}

		for interactor in entry.findall('./mif:interactorList/mif:interactor',
		 namespaces=namespace):
			
			inter = Interactor(interactor)
			interactorDict[inter.id] = inter

		source = entry.find('./mif:source', namespaces=namespace)
		source = Source(source)

		for experiment in entry.findall(
			'./mif:experimentList/mif:experimentDescription',
			 namespaces=namespace):
			exp = ExperimentDescription(experiment)
			experimentDict[exp.id] = exp

		for interaction in entry.findall(
			'./mif:interactionList/mif:interaction',
			 namespaces=namespace):
			
			interaction = Interaction(interaction)
			interactionDict[interaction.id] = interaction 
			
			experiment = experimentDict[interaction.expRef]
			interactorList = []
			
			for participant in interaction.refDict.keys():
				interactorList.append(interactorDict[participant])
			
			interactorPairs = list(combinations(interactorList, 2))

			for pair in interactorPairs:
				# print(pair[0].name + ',' + pair[1].name + ',' +
				#  pair[0].pxref + ',' + pair[1].pxref + ',' +
				#  pair[0].mType + ',' + pair[1].mType + ',' +
				#  pair[0].organism + ',' + pair[1].organism + ',' +
				#  experiment.host + ',' + experiment.detectMethod + ',' +
				#  experiment.pxref + ',' + interaction.interType + ',' +
				#  interaction.xref + ',' + source.name + ',' + 
				#  interaction.refDict[pair[0].id][0] + ',' +
				#  interaction.refDict[pair[1].id][0] + ',' +
				#  interaction.refDict[pair[1].id][1] + ',' +
				#  interaction.refDict[pair[1].id][1]

				# )
				# print(pair[0].name)
				df = pd.concat([pd.DataFrame([[pair[0].name,
				 pair[1].name,
				 pair[0].pxref,
				 pair[1].pxref,
				 pair[0].mType, 
				 pair[1].mType,
				 pair[0].organism, 
				 pair[1].organism,
				 experiment.host, 
				 experiment.detectMethod,
				 experiment.pxref,
				 interaction.interType,
				 interaction.xref, 
				 source.name, 
				 interaction.refDict[pair[0].id][0],
				 interaction.refDict[pair[1].id][0],
				 interaction.refDict[pair[0].id][1],
				 interaction.refDict[pair[1].id][1], 
				 interaction.refDict[pair[0].id][2], 
				 interaction.refDict[pair[1].id][2]]], 
				 columns=df.columns), df], ignore_index=True)

	print(df)
	out_file = re.sub(".xml", ".csv", file)
	df.to_csv(f'./{out_file}', sep = '\t')
print("CSV files successfully generated!")