class Config:
    INPUT_FILE = "C:/Users/fadra/PycharmProjects/find_maxima/o2-LNMO_astar_3_EDX_extract(8-122,12-152)/maxima_4D_adaptive_parallel.csv"
    OUTPUT_DIRECTORY = "C:/Users/fadra/Documents/LNMO order/"
    COLUMNS_OF_INTEREST = ['X_scan', 'X_acc','Y_acc', 'Mean']
    REAL_SPACE_IMAGE_SIZE = (114, 140)
    RADIUS_LIMIT = 25
    ##############################################
    #SPOT_COOR_OF_INTEREST: you have to change the coodinate according to the spots you want to study
    # principl spots for particle o1:
    principal_spots_o1 = {
        "p_1": (296.6, 169.2),
        "p_2": (275.8, 212.3),
        "p_3": (236.2, 296.5),
        "p_4": (217.4, 338.1)
    }

    # Extra spots for particle o1
    extra_spots_o1 = {
        "e_1": (286.2, 190.5),
        "e_2": (265.9, 233.1),
        "e_3": (246.1, 275.1),
        "e_4": (227.3, 318.3)
    }

    # Central spot for particle o1
    x_c_o1 = int(254.93)
    y_c_o1 = int(257)
    #############################################

    principal_spots_o2 = {
        "p_1": (378.8, 193),
        "p_2": (320.5, 222.4),
        "p_3": (205, 280.7),
        "p_4": (147.6, 309.5)
    }

    extra_spots_o2 = {
        "e_1": (349.1, 207.4),
        "e_2": (291, 236.6),
        "e_3": (234.5, 265.7),
        "e_4": (176.4, 293.9)
    }
    x_c_o2 = 262.599
    y_c_o2 = 252.56
    ##################################################
    # principl spots for particle o1:
    principal_spots_dis = {
        "p_1": (298, 212),
        "p_2": (282, 235),
        "p_3": (248, 279),
        "p_4": (231, 302)
    }
    # disorder lnmo does not have extra spot: i put this coord because the function needs extra spots and 0,0 has no spots
    extra_spots_dis = {
        "p_1": (0, 0),
        "p_2": (0, 0),
        "p_3": (0, 0),
        "p_4": (0, 0)
    }
    x_c_dis = 265.6133
    y_c_dis = 256.5742

    ######################################################################
    x_c_4_7 = 257
    y_c_4_7 = 257

    principal_spots_4_7 = {
        "p_1": (298, 349),
        "p_2": (351,298),
        "p_3": (275,301),
        "p_4": (226,355),
        "p_5": (203,207),
    }
    extra_spots_4_7 = {
        "e_1": (0, 0),

    }

    # principle spots for particle o3:
    principal_spots_o3 = {
        "p_1": (376, 191),
        "p_2": (318, 222),
        "p_3": (201, 281),
        "p_4": (145, 311),
    }

    # Extra spots for particle o1
    extra_spots_o3 = {
        "e_1": (346, 205),
        "e_2": (288, 238),
        "e_3": (230, 265),
        "e_4": (172, 296),
    }

    x_c_o3 = int(274)
    y_c_o3 = int(260)

    # principle spots for particle o3:
    principal_spots_o4 = {
        "p_1": (333, 258),
        "p_2": (306, 251),
        "p_3": (252, 236),
        "p_4": (226, 228),
    }

    # Extra spots for particle o1
    extra_spots_o4 = {
        "e_1": (319, 254),
        "e_2": (292, 247),
        "e_3": (266, 240),
        "e_4": (239, 232),
    }

    x_c_o4 = int(273)
    y_c_o4 = int(243)



    principal_spots_o2 = {
        "p_1": (371, 192),#(-404)
        "p_2": (315, 222),#(-202)
        "p_3": (199,281),#(20-2)
        "p_4": (142,310),#(40-4)
        "p_5": (408,261), #(-531)
        "p_6": (350,292),#(-331)
        "p_7": (293,319),#(-13-1)
        "p_8": (235,350),#(-13-3)
        "p_9": (177,380),#(13-5)
        "p_10":(337,124),#(-3-35)
        "p_11": (280,154),#(-1-33)
        "p_12": (222,183),#(-131)
        "p_13": (165, 213),#(3-3-1)
        "p_14": (107, 242),#(5-3-3)
    }

    principal_spots_o2 = {

        "p_1": (293,319),#(-13-1)
        "p_2": (222,183),#(-131)
    }



    principal_spots_o1 = {
        "p_1": (224, 188),#(-3-12)
        "p_2": (287, 322),#(31-2)
    }

    principal_spots_dis = {
        "p_1": (276, 283),# (022)
        "p_2": (254,230),#(0-2-2)
    }



    #spot rouge
    principal_spots_o1 = {
        "p_1": (276, 213),#(-220)
        "p_2": (237,298),#(2-20)
        "p_3": (250,199), #(-311)
        "p_4": (210,286),#(1-31)
        "p_5": (302,225),#(-13-1)
        "p_6": (262,309),#(3-1-1)
        "p_7": (282,267),#(11-1)
        "p_8":(229,242),#(-1-11)
    }





    #o2_spot encadrer en rouge
    principal_spots_o2 = {
        "p_1": (313, 222),#(-202)
        "p_2": (199,281),#(20-2)
        "p_3": (279,155), #(-1-33)
        "p_4": (165,212),#(3-3-1)
        "p_5": (349,289),#(-331)
        "p_6": (234,350),#(13-3)
        "p_7": (292,319),#(-13-1)
        "p_8":(222,182),#(1-31)
    }
    principal_spots_dis = {
        "p_1": (276, 283),# (022)
        "p_2": (254,230),#(0-2-2)
        "p_3": (282, 234),#(20-2)
        "p_4": (246, 279),#(-202)
        "p_5": (292, 260),#(220)
        "p_6": (236, 252),#(-2-20)
    }

    principal_spots_beam_damage= {
        "p_1": (330,229),
    }
    extra_spots_beam_damage = {
        "e_1": (200, 200),
    }


    # Define custom color for order mapping in intervals.
    custom_colors = {
        (0.00001, 0.1): [101 / 255, 162 / 255, 253 / 255, 1],  # Blue
        (0.1, 0.2): [0, 129 / 255, 118 / 255, 1],  # Green
        (0.2, 0.3): [238 / 255, 204 / 255, 22 / 255, 1],  # Yellow
        (0.3, 0.4): [1, 153 / 255, 0, 1],  # Orange
        (0.4, 1): [94 / 255, 49 / 255, 181 / 255, 1]  # Purple
    }





    DEBUG_MODE = True