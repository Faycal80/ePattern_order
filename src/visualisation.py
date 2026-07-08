
import numpy as np
import matplotlib.pyplot as plt


def map_values_to_colors(aligned_df, x_dim, y_dim, group_column="group", spot_type_column="Spot_Type",
                         order_ratio_column="Order_Ratio", color_mapping=None):
    """
    Maps groups to corresponding RGBA colors based on intensity ratios.

    - Groups **without any "extra" spots** are marked in **red** (#FF0000).
    - Other groups are colored based on their Order Ratio using predefined thresholds.

    Parameters:
    - aligned_df (pd.DataFrame): DataFrame containing detected spots with group information.
    - x_dim (int): Number of columns in the reshaped grid.
    - y_dim (int): Number of rows in the reshaped grid.
    - group_column (str): Column name indicating the group.
    - spot_type_column (str): Column name containing "principal" or "extra".
    - order_ratio_column (str): Column containing precomputed order ratio values.
    - color_mapping (dict): Dictionary where keys are (min, max) thresholds, values are RGBA color lists.

    Returns:
    - colors (np.ndarray): (x_dim * y_dim, 4) NumPy array containing RGBA color values.
    """

    # Liste unique des groupes
    unique_groups = aligned_df[group_column].unique()
    colors = np.zeros((x_dim * y_dim, 4))  # Tableau de couleurs RGBA initialisé à zéro

    for i, group in enumerate(unique_groups):
        group_df = aligned_df[aligned_df[group_column] == group]

        # Vérifier si le groupe contient uniquement des spots "principal"
        if "extra" not in group_df[spot_type_column].values and "principal"  in group_df[spot_type_column].values:
            colors[i] = [1, 0, 0, 1]  # Rouge (RGBA) si aucun spot extra n'est détecté
        else:
            # Récupérer la valeur du Order Ratio pré-calculé
            ratio_value = group_df[order_ratio_column].iloc[
                0]  # On suppose que tous les éléments du groupe ont le même ratio

            # Appliquer le mapping de couleur basé sur les seuils
            for (min_val, max_val), rgba in color_mapping.items():
                if min_val < ratio_value <= max_val:
                    colors[i] = rgba  # Appliquer la couleur correspondante
                    break

                    # Afficher la carte des couleurs
    plt.imshow(colors.reshape((x_dim, y_dim, 4)))  # Reshape en (rows, cols, RGBA)
    plt.axis("off")
    plt.show()

    return colors

'''def map_values_to_colors(values, x_dim, y_dim, color_mapping):
    """
    Maps values to corresponding RGBA colors based on specified thresholds.

    - Red (#FF0000) for NaN values (no extra spots detected).

    Parameters:
    - values (np.ndarray): 1D array containing values to map to colors.
    - x_dim (int): Number of columns in the reshaped grid.
    - y_dim (int): Number of rows in the reshaped grid.
    - color_mapping (dict): Dictionary where keys are tuples (min, max) defining thresholds
                            and values are RGBA color lists.

    Returns:
    - colors (np.ndarray): (x_dim * y_dim, 4) NumPy array containing RGBA color values.
    """

    colors = np.zeros((x_dim * y_dim, 4))  # Initialize color array with zeros (RGBA)

    # Assign red color for NaN values
    nan_mask = np.isnan(values)
    colors[nan_mask] = [1, 0, 0, 1]  # Red (RGBA)

    # Apply color mapping based on given thresholds
    for (min_val, max_val), rgba in color_mapping.items():
        mask = (values > min_val) & (values <= max_val)
        colors[mask] = rgba  # Apply color

    # Reshape and visualize the color mapping
    plt.imshow(colors.reshape((x_dim, y_dim, 4)))  # Ensure correct (row, col, RGBA) shape
    plt.show()

    return colors
'''

def assign_colors(values, detected_principal, detected_extra, color_mapping, red_color=[193/255, 39/255, 45/255, 1]):
    """
    Assigns colors to an array based on defined thresholds and special conditions.

    Parameters:
    - values (np.array): Array of numerical values to color.
    - detected_principal (np.array): Array indicating the number of principal spots detected per group.
    - detected_extra (np.array): Array indicating the number of extra spots detected per group.
    - color_mapping (dict): Dictionary with (min, max) ranges as keys and RGBA colors as values.
    - red_color (list): RGBA color for cases where no extra spots are detected but spots detected > 1.

    Returns:
    - colors (np.array): Array of assigned colors.
    """

    # Initialize color array
    colors = np.zeros((values.shape[0], 4))

    for i in range(values.shape[0]):
        value = values[i]

        # Check special condition: No extra spots detected and more than one principal spot which is
        if detected_extra[i] == 0 and detected_principal[i] > 1:
            colors[i] = red_color
            continue  # Skip to next iteration

        # Assign color based on threshold mapping
        for (min_val, max_val), color in color_mapping.items():
            if min_val < value <= max_val:
                colors[i] = color
                break  # Stop checking further ranges

    return colors
