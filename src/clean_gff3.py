import argparse
import os
import re
parser = argparse.ArgumentParser()
parser.add_argument("--input_file", "-f", type=str, required=True)
parser.add_argument('--chro_num', "-n", type=str, required=True)
parser.add_argument("--start", "-s", default=-1, type=int)
parser.add_argument("--end", "-e", default=-1, type=int)
args = parser.parse_args()

input_gff3 = args.input_file
start = args.start #start position of user's desired translating region
end = args.end     #end position of user's desired translating region
chro_num = args.chro_num
input_dir = os.path.dirname(os.path.abspath(input_gff3))
in_file = os.path.join(input_dir, input_gff3)
output_txt = input_gff3.split('/')[-1].split('.')[0]+"_chro"+chro_num+'_cleaned.gff3'
# output_txt = input_gff3.split('/')[-1].split('.')[0]+"_MHC_cleaned.gff3"

search_chro = "chr"+chro_num+"$"
with open(input_gff3) as f1:
    with open(output_txt, 'a') as f2:
        lines = f1.readlines()
        for i, line in enumerate(lines):
            line_list = line.split()
            is_desired_data = re.match(search_chro, line_list[0]) and bool(re.match("gene", line_list[2]))
            
            if end >= 0: 
                if start >= 0:
                    within_range = (int(line_list[3]) >= start) and (int(line_list[4]) <= end)
                else:
                    within_range = int(line_list[4]) <= end
            elif start >= 0:
                within_range = int(line_list[3]) >= start
            else:
                within_range = True
                
            if bool(is_desired_data) and within_range:
                f2.write(line)


print("Saved file {}. \nIt is now in the following directory: \n{}.".format(output_txt, input_dir))