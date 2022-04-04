from BCBio import GFF
import argparse
import csv
import os
import re
parser = argparse.ArgumentParser()
parser.add_argument("--input_file", "-f", type=str, required=True)
args = parser.parse_args()

input_file = args.input_file
input_dir = os.path.dirname(os.path.abspath(input_file))
in_file = os.path.join(input_dir, input_file)
output_name = input_file.split('/')[-1].split('.')[0]+'.csv'

in_handle = open(in_file)

''' key_rank is a list of chosen keys that can be picked to be played. 
    The list contains all octaves of C, E, G, D, F#, and A on a piano 
    keyboard. The list is ordered by listing all CEG then DF#A octaves 
    from the middle C outwards.The different notes are played for 
    different gene type. The gene type that appears the most frequent 
    will get the highest ranked(towards the front of the list) note 
    from the key_rank list.'''
key_rank = [60, 64, 67, 72, 76, 79, 48, 52, 55, 84, 88, 91, 36, 40, 43, 96, 100, 103, 24, 28, 31, 
62, 66, 69, 74, 78, 81, 50, 54, 57, 86, 90, 93, 38, 42, 45, 98, 102, 105, 26, 30, 33]

''' sort gene types to see which is the most frequent
    use this info to assign notes to be played for each gene type '''
gene_types, key_match = {}, {}
with open(in_handle.name) as f1:
    lines = f1.readlines()
    for i, line in enumerate(lines):
        gt = re.search(r'gene_type=(.*?);', line)
        if (gt is not None) and (gt.group(1) not in gene_types.keys()):
            gene_types[gt.group(1)]=1
        elif (gt is not None) and (gt.group(1) in gene_types.keys()):
            gene_types[gt.group(1)]+=1
gene_types = sorted(gene_types.items(), key=lambda x: x[1], reverse=True)
for i in range(len(gene_types)):
	key_match[gene_types[i][0]] = key_rank[i]

data_csv = []
for rec in GFF.parse(in_handle):
    # The rec object is a Biopython SeqRecord containing the features described in the GFF file. 
	for i in range(len(rec.features)):
		f = rec.features[i].location
		gt = rec.features[i].qualifiers['gene_type'][0]
		csv_row_Note_on,csv_row_Note_off = {},{}

		csv_row_Note_on['Track'] = 2
		csv_row_Note_on['Time'] = int(f.start)
		csv_row_Note_on['NOC'] = "Note_on_c"
		csv_row_Note_on['Channel'] = 1
		csv_row_Note_on['Note'] = key_match[gt]
		csv_row_Note_on['Velocity'] = 81
		data_csv.append(csv_row_Note_on)

		csv_row_Note_off['Track'] = 2
		csv_row_Note_off['Time'] = int(f.end)
		csv_row_Note_off['NOC'] = "Note_off_c"
		csv_row_Note_off['Channel'] = 1
		csv_row_Note_off['Note'] = key_match[gt]
		csv_row_Note_off['Velocity'] = 0

		data_csv.append(csv_row_Note_off)
in_handle.close()

csv_file = os.path.join(input_dir, output_name)
data_csv = sorted(data_csv, key=lambda item: item['Time'])
end_time = data_csv[len(data_csv)-1]['Time']
with open(csv_file, 'w', encoding='UTF8', newline='') as f:
	fieldnames = ['Track', 'Time', 'NOC', 'Channel','Note','Velocity']
	f.write("0, 0, Header, 1, 2, 10000\n2, 0, Start_track\n")
	writer = csv.DictWriter(f, fieldnames=fieldnames)
	writer.writerows(data_csv)
	f.write("2, {}, End_track\n0, 0, End_of_file".format(str(end_time)))

print("Saved file {}. \nIt is now in the following directory: \n{}.".format(output_name, input_dir))