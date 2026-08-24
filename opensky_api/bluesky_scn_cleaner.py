import re
import pandas as pd

def replace_ids(input_file, output_file):
    counter = 1
    
    with open(input_file, "r") as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        match = re.search(r'>CRE\s+([0-9a-fA-F]+),', line)
        if match:
            original_id = match.group(1)
            new_id = f"kl{counter}"
            counter += 1
            line = line.replace(original_id, new_id, 1)
        new_lines.append(line)
    
    with open(output_file, "w") as f:
        f.writelines(new_lines)

replace_ids("schiphol_arrivals_july_2024.scn", "schiphol_arrivals_july_2024_final.scn")
