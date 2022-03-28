import argparse
import os
import re
parser = argparse.ArgumentParser()
parser.add_argument("--input_file", "-f", type=str, required=True)
parser.add_argument('--chro_num', "-n", type=str, required=True)
args = parser.parse_args()

input_gff3 = args.input_file
chro_num = args.chro_num
input_dir = os.path.dirname(os.path.abspath(input_gff3))
in_file = os.path.join(input_dir, input_gff3)
output_txt = input_gff3.split('/')[-1].split('.')[0]+'_cleaned.gff3'

# searchquery = '##sequence-region'
search_chro = "chr"+chro_num+"$"
with open(input_gff3) as f1:
    with open(output_txt, 'a') as f2:
        lines = f1.readlines()
        for i, line in enumerate(lines):
            line_list = line.split()
            if bool(re.match(search_chro, line_list[0])) and bool(re.match("gene", line_list[2])):
                f2.write(line)
            # if line.startswith(searchquery):
            #     f2.write(lines[i+1])

print("Saved file {}. \nIt is now in the following directory: \n{}.".format(output_txt, input_dir))