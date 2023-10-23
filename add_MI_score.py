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
	print("Define input files: -in <inp_1.csv> ... <inp_n.csv>")
	exit(1)

for i in range(inp_index+1, len(sys.argv)):
	
	file = sys.argv[i]
	MI_file = re.sub(".csv", "_MI_scores.csv", file) 
	out_file = re.sub(".csv", "_w_MI_score.csv", file) 
	print(f'Adding MI score column to {out_file}')

	df = pd.read_csv(f'{file}', sep = '\t')
	df2 = pd.read_csv(f'{MI_file}', sep = '\t')
	df2 = df2[['MIscores']]

	df['MI score'] = df2.loc[:,"MIscores"]

	df.to_csv(f"{out_file}", index=False, na_rep='N/A')

print("CSV files with MI scores successfully generated!")