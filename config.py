# For relative file paths, use the application_path variable like so:
SPREADSHEET = application_path + "/../raw_data/Elephants.xlsx"
SHEETNUM = 0
# Or, just use the absolute path
PHOTODIR = "/home/jonathan/Elephant_MAY/HIP_ID_PHOTOS_TIM_MAY"

# What does verbose do? Nothing, yet
VERBOSE = False

# To speed up launch time for debugging, set this to false.
# Will ignore the photo_size var if small photos are available
SCALE_SMALLS = False

# Set this to true to generate small images for all images on startup
# Doesn't create .smalls if they are already present
GENERATE_SMALLS = True

# Can set this to, foreg, 'template' to order the images a certain way.
# Or, open the app and use 'reorder images' to do the same thing
DEFAULT_ORDER = ''

# The default size of the window created when the app is run.
MAIN_WINDOW_SIZE = (1200, 800)
# The size of the inspector dialog window (open when clicking on an elephant)
E_INSPECTOR_SIZE = (1200, 800)

# The size of images in the grid of the main window.
PHOTO_SIZE = 600
