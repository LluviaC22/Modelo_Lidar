import pandas as pd

def csv_to_ply(csv_file, ply_file):
    # Read the CSV file
    df = pd.read_csv(csv_file)

    if 'x' not in df.columns or 'y' not in df.columns or 'z' not in df.columns:
        raise ValueError("CSV must contain 'x', 'y', and 'z' columns.")

  
    with open(ply_file, 'w') as f:
        
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write(f"element vertex {len(df)}\n")
        f.write("property float x\n")
        f.write("property float y\n")
        f.write("property float z\n")
        
    
        if 'red' in df.columns and 'green' in df.columns and 'blue' in df.columns:
            f.write("property uchar red\n")
            f.write("property uchar green\n")
            f.write("property uchar blue\n")

        f.write("end_header\n")

       
        for _, row in df.iterrows():
            # Write x, y, z coordinates
            f.write(f"{row['x']} {row['y']} {row['z']}")
            # If RGB values are present, write them too
            if 'red' in df.columns and 'green' in df.columns and 'blue' in df.columns:
                f.write(f" {int(row['red'])} {int(row['green'])} {int(row['blue'])}")
            f.write("\n")

    print(f"los datos an sido exportados a {ply_file}")

def main():
    # Prompt the user for the input CSV file and the output PLY file
    csv_file = input("ingresa el path al archivo CSV file: ")
    ply_file = input("ingresa el nombre del archivo PLY (default: output.ply): ") or "output.ply"

    # Convert CSV to PLY
    csv_to_ply(csv_file, ply_file)

if __name__ == "__main__":
    main()
