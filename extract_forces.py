import pandas as pd
import os
import glob

# Path to the postProcessing folder
base_path = "postProcessing/forces1"
output_file = "merged_turbine_forces.csv"

all_data = []

# 1. Loop through time-step folders (1000, 2000, 2500, etc.)
# sorted() ensures the time steps are processed in the correct order
for folder in sorted(os.listdir(base_path), key=lambda x: int(x) if x.isdigit() else 0):
    folder_path = os.path.join(base_path, folder)
    
    if os.path.isdir(folder_path):
        # 2. Look for .dat files in each folder
        for file in glob.glob(os.path.join(folder_path, "*.dat")):
            print(f"Reading data from: {file}")
            
            # 3. Read data, skipping OpenFOAM '#' comment headers
            # Using sep='\s+' handles irregular spacing in OpenFOAM files
            try:
                df = pd.read_csv(file, sep=r'\s+', comment='#', header=None)
                all_data.append(df)
            except Exception as e:
                print(f"Skipping {file} due to error: {e}")

# 4. Merge all data into one single sequence
if all_data:
    final_df = pd.concat(all_data, ignore_index=True)
    
    # Standard columns for OpenFOAM forceCoefficients
    # Adjust names if your specific .dat file has different columns
    final_df.columns = ['Time', 'Cd', 'Cl', 'CmRoll', 'CmPitch', 'CmYaw', 'Cd(f)', 'Cd(v)', 'Cl(f)', 'Cl(v)']
    
    # 5. Final Sort and Save
    final_df = final_df.sort_values(by='Time')
    final_df.to_csv(output_file, index=False)
    print(f"\n--- SUCCESS ---")
    print(f"All time-steps merged into: {output_file}")
else:
    print("\n--- ERROR ---")
    print(f"No .dat files found in {base_path}. Check your simulation output.")