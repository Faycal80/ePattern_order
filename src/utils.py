import pandas as pd
import os
def load_csv(file_path):
    """
    Loads a CSV file into a Pandas DataFrame.

    Parameters:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Data loaded into a Pandas DataFrame.
    """
    try:
        df = pd.read_csv(file_path)
        print(f"CSV file '{file_path}' loaded successfully!")
        return df
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return None




def save_matched_spots_to_csv(matched_spots_by_group, filename="matched_spots.csv"):
    """
    Saves the matched spots data into a CSV file.

    Parameters:
    - matched_spots_by_group (dict): Dictionary containing matched spots for each group.
    - filename (str): Name of the CSV file to save the data.
    """

    if not matched_spots_by_group:
        print("⚠️ Warning: No matched spots to save!")
        return

    data = []

    for group, spots in matched_spots_by_group.items():
        for spot_name, details in spots.items():
            x, y = details.get("position", (None, None))
            intensity = details.get("intensity", None)
            data.append([group, spot_name, x, y, intensity])

    # Convert to DataFrame
    df = pd.DataFrame(data, columns=["Group", "Spot_Name", "X", "Y", "Intensity"])

    # Assure que le fichier a bien l'extension .csv
    if not filename.endswith(".csv"):
        filename += ".csv"

    # Sauvegarde avec formatage pour éviter la notation scientifique
    df.to_csv(filename, index=False, float_format="%.6f")

    print(f"✅ Matched spots saved to: {os.path.abspath(filename)}")


# Usage
