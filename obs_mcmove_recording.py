# Import what we need
import obspython as obs
import os
from shutil import move

# These recording paths are hardcoded but can be changed here or in the OBS Script settings if needed
input_path = "Y:\\YouTube\\PreUpload\\"
output_path = "Y:\\YouTube\\Upload\\"

# Function that takes a "path" argument and returns the path of the newest file in that directory
def get_newest(path):
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    return max(paths, key=os.path.getctime)

# Function that takes a "cd" argument and uses the get_newest function to move the newest file from the input_path to the output_path
def signal_catcher(cd):
	mcfile_path = get_newest(input_path)
	mcfile_name = os.path.basename(mcfile_path)		
	move(mcfile_path, output_path + mcfile_name)

# Function gets the recording output and connects the signal_catcher() function to the "deactivate" signal handler.
def script_load(settings):
	output = obs.obs_frontend_get_recording_output();
	print(output);
	sh = obs.obs_output_get_signal_handler(output)
	obs.signal_handler_connect(sh, "deactivate", signal_catcher)

# Function sets the default values for the input and output paths
def script_defaults(settings):
	global input_path
	global output_path
	obs.obs_data_set_default_string(settings, "inputpath", input_path)
	obs.obs_data_set_default_string(settings, "outputpath", output_path)

# Function updates the values for the input and output paths
def script_update(settings):
	global input_path
	global output_path
	input_path = obs.obs_data_get_string(settings, "inputpath")
	output_path = obs.obs_data_get_string(settings, "outputpath")

# Function sets the script description in OBS
def script_description():
	return "Moves recordings to a new location when ended."

# Function sets the script properties in OBS
def script_properties():
	props = obs.obs_properties_create()
	obs.obs_properties_add_text(props, "inputpath", "Input Path", obs.OBS_TEXT_DEFAULT)
	obs.obs_properties_add_text(props, "outputpath", "Output Path", obs.OBS_TEXT_DEFAULT)
	return props