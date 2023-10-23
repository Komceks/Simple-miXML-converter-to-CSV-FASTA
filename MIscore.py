import requests
import json
import csv
import pandas as pd 
import sys
import re
try:
  inp_index = sys.argv.index('-in')
except ValueError:
  print("-in argument not found")
  exit(1)

if(inp_index == len(sys.argv)-1):
    print("Define input files: -in <inp_1.csv> ... <inp_n.csv>")
    exit(1)
# Define the base URL
base_url = "https://www.ebi.ac.uk/intact/ws/interaction"

# Define the endpoint you want to use (/findInteractions/{query})
endpoint = "/findInteractions/{query}"

for i in range(inp_index+1, len(sys.argv)):
    
    file = sys.argv[i]
    print(f'Getting MI scores from {file}')
    AC_ids = pd.read_csv(file, sep="\t")
    AC_ids = AC_ids.iloc[:, 12]
    df = pd.DataFrame(data={"MIscores": []});

    # Define the taxon ID as the query parameter
    prev_ac_id = 0

    # with open('Interaction_ACs.txt') as openfileobject:
    for ac_id in AC_ids:
        ac_id = ac_id.strip()
        # print(ac_id)
        if ac_id == prev_ac_id:
            df.loc[len(df.index)] = [confidence_value]

        elif(ac_id != "N/A"):
            # Make the GET request
            response = requests.get(base_url + endpoint.format(query=ac_id))

            # Check the response status code
            if response.status_code == 200:
                # Parse and use the response data as needed
                data = response.json()
                formatted_data = json.dumps(data, indent=4)
                # Extract the value for "intact-miscore" from the "content" list
                
                content_list = data["content"]
                confidence_value = None

                for content_item in content_list:
                    confidence_values = content_item.get("confidenceValues", [])
                    # print(confidence_values)
                    for value in confidence_values:
                        if(re.search("intact-miscore", value)):
                            key, val = value.split(":")
                            confidence_value = float(val)
                            break
                    if confidence_value is not None:
                        break

                df.loc[len(df.index)] = [confidence_value] 
            else:
                print("Error:", response.status_code)
        else:
            confidence_value = "N/A"
            df.loc[len(df.index)] = [confidence_value] 
        prev_ac_id = ac_id
    out_file = re.sub(".csv", "", file)
    df.to_csv(f"{out_file}_MI_scores.csv", sep='\t', encoding='utf-8')


print("MIscore files successfully generated!")