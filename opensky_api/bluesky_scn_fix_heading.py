import math
import re

# Target point (destination)
TARGET_LAT = 52.3068953
TARGET_LON = 4.760783

def calculate_bearing(lat1, lon1, lat2, lon2):
    # Convert to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    dlon = lon2 - lon1
    x = math.sin(dlon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
    bearing = math.degrees(math.atan2(x, y))
    return (bearing + 360) % 360  # Normalize

def fix_headings(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            # Match pattern like: 01:14:30.00>CRE 4853d4, A320 ,49.9049,2.8553,20,FL380,246
            match = re.match(r'(.*A320\s*,)([^,]+),([^,]+),([^,]+),FL(\d+),([^,\n]+)', line)
            if match:
                prefix, lat, lon, heading, flight_level, speed = match.groups()
                lat, lon = float(lat), float(lon)
                
                # Compute new heading
                new_heading = round(calculate_bearing(lat, lon, TARGET_LAT, TARGET_LON))
                
                # Replace old heading with new one
                new_line = re.sub(r',([^,]+),FL', f',{new_heading},FL', line)
                outfile.write(new_line)
            else:
                outfile.write(line)

def fix_headings_and_altitudes(input_file, output_file):
    pattern = re.compile(
        r'^(?P<prefix>.*A320\s*,)'
        r'(?P<lat>[-+]?\d+\.\d+),'
        r'(?P<lon>[-+]?\d+\.\d+),'
        r'(?P<heading>[-+]?\d+),'
        r'FL(?P<altitude>[-+]?\d+),'
        r'(?P<speed>\d+)\s*$'
    )

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            match = pattern.match(line.strip())
            if not match:
                outfile.write(line)
                continue

            data = match.groupdict()
            lat, lon = float(data['lat']), float(data['lon'])
            altitude = int(data['altitude'])

            # --- Fix heading ---
            new_heading = round(calculate_bearing(lat, lon, TARGET_LAT, TARGET_LON))

            # --- Fix altitude if below 10 or negative ---
            if altitude < 10:
                altitude = 350
                data['speed'] = 250

            # Reconstruct the line
            new_line = (
                f"{data['prefix']}{lat:.4f},{lon:.4f},{new_heading},FL{altitude},{data['speed']}\n"
            )

            outfile.write(new_line)
# Example usage:
fix_headings_and_altitudes('schiphol_arrivals_march_2024_final.scn', 'schiphol_arrivals_march_2024_final3.scn')