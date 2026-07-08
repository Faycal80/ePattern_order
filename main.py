from src.config import Config
from src.utils import load_csv,save_matched_spots_to_csv
import src.preprocessing as ppr
import src.processing as pr
import src.visualisation as vs
import numpy as np
import matplotlib.pyplot as plt




def main():

    file_path = Config.INPUT_FILE
    output_path = Config.OUTPUT_DIRECTORY
    # Load and preprocess
    df = load_csv(file_path)
    #select thye columns of interest (position of the spot and their mean intensity)
    columns= Config.COLUMNS_OF_INTEREST

    # extract the needed columns
    df_extract_needed_columns = ppr.extract_needed_columns(df, columns)
    # group the diffraction pattern by the changing in x_scan (the real image x coordinate)
    df_group = ppr.group_by_diffraction_pattern(df_extract_needed_columns,"X_scan")
    #align the diffraction patterns, save the alignened data, extract the alignned data, the dx and the dy (coefficient correction appliyed for the alignement)
    df_al,dx,dy = pr.align_diffraction_patterns(df=df_group,
                                                x_c=Config.x_c_o3,
                                                y_c=Config.y_c_o3,
                                                radius_limit=Config.RADIUS_LIMIT,
                                                output_file=output_path+'aligned_df_o3.csv')
    #compute the mean intensity of the shift correction dx an dy
    dx_mean = (np.array(dx)).mean()
    dy_mean = (np.array(dy).mean())
    #apply the correction for the inputs coordinates
    principal_spots_o3= pr.apply_alignment_for_the_selected_coord(spots=Config.principal_spots_o3,
                                                                          dx=dx_mean,
                                                                          dy=dy_mean)
    extra_spots_o3= pr.apply_alignment_for_the_selected_coord(spots=Config.extra_spots_o3,
                                                                      dx=dx_mean,
                                                                      dy=dy_mean)
    #check if there are principal and extra spot
    df_al_selection = pr.detect_points_within_radius(df_al,
                                   principal_spots= principal_spots_o3,
                                   extra_spots= extra_spots_o3,
                                   radius_limit=Config.RADIUS_LIMIT,
                                   output_csv=output_path+'detection_o3.csv')


    group_ratios = pr.compute_intensity_ratio_by_group(aligned_df=df_al_selection,
                                                       group_column="group",
                                                       intensity_column="Mean")


   # Convert dictionary values to a NumPy array and handle NaNs
    group_ratios_array = np.array(list(group_ratios.values()))
    group_ratios_array = np.nan_to_num(group_ratios_array, nan=0)  # Replace NaNs with 0

    # Compute order ratio safely
    #normalizing according to the theoritical maximum degree of order
    order_ratio = group_ratios_array / 0.8

    np.save( output_path+'order_ratio_o3.npy',order_ratio)
    # Map the computed values back to the DataFrame
    df_al_selection["Intensity_Ratio"] = df_al_selection["group"].map(group_ratios)
    df_al_selection["Order_Ratio"] = df_al_selection["Intensity_Ratio"] / 0.8  # Safe division
    print(df_al_selection.columns)

    order_ratio_in_colors_interval=vs.map_values_to_colors(aligned_df=df_al_selection,
                            x_dim=Config.REAL_SPACE_IMAGE_SIZE[0],
                            y_dim=Config.REAL_SPACE_IMAGE_SIZE[1],
                            group_column="group",
                            spot_type_column="Spot_Type",
                            order_ratio_column="Order_Ratio",
                            color_mapping=Config.custom_colors)


    np.save(output_path + 'o3_order_ratio_in_colors',order_ratio_in_colors_interval)

    matched_principal_spots = pr.find_nearest_spots_by_group(aligned_df=df_al_selection,
                                                    reference_positions=principal_spots_o3,
                                                    group_column="group",
                                                    x_column="X_acc",
                                                    y_column="Y_acc",
                                                    intensity_column="Mean",
                                                    radius=Config.RADIUS_LIMIT)
    matched_extra_spots = pr.find_nearest_spots_by_group(aligned_df=df_al_selection,
                                                    reference_positions=extra_spots_o3,
                                                    group_column="group",
                                                    x_column="X_acc",
                                                    y_column="Y_acc",
                                                    intensity_column="Mean",
                                                    radius=Config.RADIUS_LIMIT)

    save_matched_spots_to_csv(matched_principal_spots,
                              output_path + 'principle_spots_o3_intensities_positions.csv')
    save_matched_spots_to_csv(matched_extra_spots,
                              output_path + 'extra_spots_o3_intensities_positions.csv')



if __name__ == "__main__":
    main()