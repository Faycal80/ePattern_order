
import numpy as np
import pandas as pd


def align_diffraction_patterns(df, x_c, y_c, x_al=256, y_al=256, radius_limit=12, output_file="aligned_data.csv"):
    """
    Aligns diffraction patterns by centering the central spot to a desired position.
    If no spot is found within the radius limit, selects the spot with the highest intensity.

    Parameters:
        df (pd.DataFrame): DataFrame containing diffraction pattern data.
        x_c (int): X-coordinate of the central spot.
        y_c (int): Y-coordinate of the central spot.
        x_al (int, optional): Desired X-coordinate for alignment. Defaults to 256.
        y_al (int, optional): Desired Y-coordinate for alignment. Defaults to 256.
        radius_limit (float, optional): The radius limit for considering the central spot. Defaults to 12.
        output_file (str, optional): Path to save the aligned data. Defaults to "aligned_data.csv".

    Returns:
        pd.DataFrame: The aligned DataFrame.
        list: List of dx values for each diffraction pattern.
        list: List of dy values for each diffraction pattern.
    """
    aligned_data = []
    dx_list, dy_list = [], []

    # Process each group independently
    for group_id, group in df.groupby("group"):  # Assuming "group" is the column name
        group = group.copy()  # Avoid SettingWithCopyWarning

        # Calculate the distance Rc for each point
        Rc = np.sqrt((x_c - group['X_acc']) ** 2 + (y_c - group['Y_acc']) ** 2)

        # Check if any points are within the radius limit
        central_points = group[(Rc > 0) & (Rc <= radius_limit)]  # Points within the radius

        if not central_points.empty:
            # Take the first central point within the radius
            central_point = central_points.iloc[0]
        else:
            # If no point is within the radius, choose the one with the highest intensity
            central_point = group.loc[group['Mean'].idxmax()]  # Find max intensity spot

        # Calculate dx and dy for the detected central point
        dx = x_al - central_point['X_acc']
        dy = y_al - central_point['Y_acc']

        # Apply the shift to all points in the group
        group.loc[:, 'X_acc'] += dx
        group.loc[:, 'Y_acc'] += dy

        # Store the shift for this diffraction pattern
        dx_list.append(dx)
        dy_list.append(dy)

        aligned_data.append(group)

    # Combine and save updated data
    if aligned_data:
        aligned_df = pd.concat(aligned_data, ignore_index=True)  # Avoid index duplication
        aligned_df.to_csv(output_file, index=False)
        print(f"Aligned data saved to '{output_file}'.")
    else:
        aligned_df = pd.DataFrame()  # Empty DataFrame if no valid data

    print(f"Total groups processed: {df['group'].nunique()}")

    return aligned_df, dx_list, dy_list


# Function to apply alignment
def apply_alignment_for_the_selected_coord(spots, dx, dy):
    """
    Adjusts the coordinates of a set of spots by applying a given shift.

    Parameters:
    -----------
    spots : dict
        A dictionary where keys are spot identifiers (e.g., "p_1", "e_2")
        and values are tuples representing (x, y) coordinates.
    dx : float
        The shift to be applied in the x-direction.
    dy : float
        The shift to be applied in the y-direction.

    Returns:
    --------
    dict
        A new dictionary with the same keys but updated (x, y) coordinates
        after applying the alignment shift.

    Example:
    --------
    spots = {"p_1": (100, 200), "p_2": (150, 250)}
    dx, dy = 10, -5
    aligned_spots = apply_alignment(spots, dx, dy)
    # aligned_spots -> {"p_1": (110, 195), "p_2": (160, 245)}
    """
    return {key: (x + dx, y + dy) for key, (x, y) in spots.items()}


def detect_points_within_radius(aligned_df, principal_spots, extra_spots, radius_limit, output_csv="detected_points.csv"):
    """
    Detects points within a given radius from principal and extra spots and updates the input DataFrame.

    Parameters:
    - aligned_df (pd.DataFrame): DataFrame containing detected points with 'X_acc' and 'Y_acc' columns.
    - principal_spots (dict): Dictionary of principal spot coordinates {spot_name: (x, y)}.
    - extra_spots (dict): Dictionary of extra spot coordinates {spot_name: (x, y)}.
    - radius_limit (float): Maximum distance to consider a point as detected.
    - output_csv (str): Name of the output CSV file.

    Returns:
    - aligned_df (pd.DataFrame): Updated DataFrame with "Detected" and "Spot_Type" columns.
    """

    # Initialize columns
    aligned_df["Detected"] = 0  # Default: Not detected
    aligned_df["Spot_Type"] = None  # Default: No type

    # Iterate over DataFrame rows
    for index, row in aligned_df.iterrows():
        x, y = row["X_acc"], row["Y_acc"]

        # Check for principal spots first
        for spot, (x_s, y_s) in principal_spots.items():
            distance = np.sqrt((x - x_s) ** 2 + (y - y_s) ** 2)
            if distance <= radius_limit :
                aligned_df.at[index, "Detected"] = 1
                aligned_df.at[index, "Spot_Type"] = "principal"
                break  # Stop checking after first match

        # If no principal spot was found, check extra spots
        if aligned_df.at[index, "Detected"] == 0:
            for spot, (x_s, y_s) in extra_spots.items():
                distance = np.sqrt((x - x_s) ** 2 + (y - y_s) ** 2)
                if distance <= radius_limit :
                    aligned_df.at[index, "Detected"] = 1
                    aligned_df.at[index, "Spot_Type"] = "extra"
                    break  # Stop checking after first match

    # Save the updated DataFrame to CSV
    aligned_df.to_csv(output_csv, index=False)
    print(f"Updated DataFrame saved to {output_csv}")

    return aligned_df



def compute_intensity_ratio_by_group(aligned_df, group_column="group", intensity_column="Intensity"):
    """
    Computes the ratio of mean intensity of extra spots to principal spots for each group
    and returns the results as a NumPy array.

    Parameters:
    - aligned_df (pd.DataFrame): DataFrame containing spot data with "Detected", "Spot_Type", and intensity column.
    - group_column (str): Column name indicating the group.
    - intensity_column (str): Column name for intensity values.

    Returns:
    - group_ratios (dict): Dictionary with group numbers as keys and their intensity ratio as values.
    """

    unique_groups = aligned_df[group_column].unique()
    group_ratios = {}

    for group in unique_groups:
        group_df = aligned_df[aligned_df[group_column] == group]

        # Filter detected spots by type
        principal_spots_df = group_df[(group_df["Detected"] == 1) & (group_df["Spot_Type"] == "principal")]
        extra_spots_df = group_df[(group_df["Detected"] == 1) & (group_df["Spot_Type"] == "extra")]

        # Compute sums and counts
        sum_principal = principal_spots_df[intensity_column].sum()
        sum_extra = extra_spots_df[intensity_column].sum()
        count_principal = len(principal_spots_df)
        count_extra = len(extra_spots_df)

        # Compute ratio if valid
        if count_principal > 0 and count_extra > 0:
            ratio_spot = (sum_extra / 4) / (sum_principal / 4) #change the denominator in fuction of the number of spot considered
        else:
            ratio_spot = np.nan  # Assign NaN if no valid computation is possible

        group_ratios[group] = ratio_spot


    return group_ratios



def find_nearest_spots_by_group(aligned_df, reference_positions, group_column,
                                x_column="X_acc", y_column="Y_acc", intensity_column="Intensity", radius=10):
    """
    Finds the nearest spots for each group in `aligned_df` to predefined reference positions (principal or extra),
    within a given radius.

    Parameters:
        - aligned_df (pd.DataFrame): DataFrame containing diffraction spots data.
        - reference_positions (dict): Dictionary with spot names as keys and (x, y) tuples as values.
        - group_column (str): Column name for grouping the data (e.g., 'group').
        - x_column (str): Column name for X coordinates.
        - y_column (str): Column name for Y coordinates.
        - intensity_column (str): Column name for intensity values.
        - radius (float): Maximum distance allowed for a spot to be considered a match.

    Returns:
        - matched_spots_by_group (dict): Dictionary where keys are group names and values are dictionaries
                                         containing matched spots for each group.
    """

    matched_spots_by_group = {}

    # Liste des groupes pour garantir qu'ils apparaissent tous
    all_groups = aligned_df[group_column].unique()

    for group in all_groups:
        group_df = aligned_df[aligned_df[group_column] == group]
        matched_spots = {}

        for spot_name, (ref_x, ref_y) in reference_positions.items():
            # Filtrer les valeurs NaN dans X et Y
            valid_spots = group_df.dropna(subset=[x_column, y_column])

            # Calculer les distances
            distances = np.sqrt((valid_spots[x_column] - ref_x) ** 2 + (valid_spots[y_column] - ref_y) ** 2)

            # Garder uniquement les spots dans le rayon
            close_spots = valid_spots.loc[distances[distances <= radius].index]

            if not close_spots.empty:
                # Prendre le spot le plus proche dans le rayon
                min_index = distances[distances <= radius].idxmin()
                closest_spot = group_df.loc[min_index]

                matched_spots[spot_name] = {
                    "position": (closest_spot[x_column], closest_spot[y_column]),
                    "intensity": closest_spot[intensity_column]
                }
            else:
                # Assurer que tous les groupes ont les mêmes clés, même si pas trouvé
                matched_spots[spot_name] = {"position": (0, 0), "intensity": 0}

        matched_spots_by_group[group] = matched_spots

    return matched_spots_by_group


