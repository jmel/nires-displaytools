from nires.settings import CALIBRATION_PATH

WAVELENGTH_REG = "tspec_wavelength.reg"


def generate_wavelength_file_from_reg():
    with open("{}/{}".format(CALIBRATION_PATH, WAVELENGTH_REG), "r") as file:
        for line in file:
            if "text" in line:
                pass
                # x_pos = line[]
                # y_pos =
                # lam =
