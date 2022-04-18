from BCBio import GFF
import argparse
import csv
import os
import re
import pickle
parser = argparse.ArgumentParser()
parser.add_argument("--input_file", "-f", type=str, required=True)
args = parser.parse_args()

input_file = args.input_file
input_dir = os.path.dirname(os.path.abspath(input_file))
in_file = os.path.join(input_dir, input_file)
output_name = input_file.split('/')[-1].split('.')[0]+'.csv'

in_handle = open(in_file)

''' key_match is a dictionary that assigns notes to be played for each gene type.
	Its key is gene type, and its value is an int that represents that gene type's 
	assigned note in midi convention.'''
a_file = open("key_assignment.pkl", "rb")
key_match = pickle.load(a_file)
a_file.close()

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