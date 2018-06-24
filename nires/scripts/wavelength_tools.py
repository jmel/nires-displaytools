
def generate_wavelength_file_from_reg():
    with open("/Users/jlmelbourne/Projects/nires-displaytools/calibrations/tspec_wavelength.reg", "r") as file:
        for line in file:
            if "text" in line:
                pass
                # x_pos = line[]
                # y_pos =
                # lam =
