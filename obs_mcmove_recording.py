# Import what we need
import obspython as obs
import os
from easygui import *
from shutil import move


# Function that takes a "path" argument and returns the path of the newest file in that directory
def get_newest(path):
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    return max(paths, key=os.path.getctime)


# Function that takes a "cd" argument and uses the get_newest function to move the newest file from the input_path to the output_path
def signal_catcher(cd):
    mcfile_path = get_newest(input_path)
    mcfile_name = os.path.basename(mcfile_path)

    # appending button to the button list
    # button list
    button_list = []
    button_list.append("Multiplayer Recording")
    button_list.append("Campaign Recording")
    button_list.append("Other")

    # creating a button box
    output = buttonbox("Where do you want to save the current recording?", "McMove", button_list)

    if output == "Multiplayer Recording":
        move(mcfile_path, output_path1 + mcfile_name)
        return
    if output == "Campaign Recording":
        move(mcfile_path, output_path2 + mcfile_name)
        return
    if output == "Other":
        move(mcfile_path, output_path3 + mcfile_name)
        return


# Function gets the recording output and connects the signal_catcher() function to the "deactivate" signal handler.
def script_load(settings):
    output = obs.obs_frontend_get_recording_output()
    print(output)
    sh = obs.obs_output_get_signal_handler(output)
    obs.signal_handler_connect(sh, "deactivate", signal_catcher)


# Function sets the default values for the input and output paths
def script_defaults(settings):
    global input_path
    global output_path1
    global output_path2
    global output_path3

    # Set defaults/hardcoded paths here:
    obs.obs_data_set_default_string(settings, "inputpath", "Y:\\YouTube\\PreUpload\\")
    obs.obs_data_set_default_string(settings, "outputpath1", "Y:\\YouTube\\Upload\\MultiplayerRecording\\")
    obs.obs_data_set_default_string(settings, "outputpath2", "Y:\\YouTube\\Upload\\CampaignRecording\\")
    obs.obs_data_set_default_string(settings, "outputpath3", "Y:\\YouTube\\Upload\\Other\\")


# Function updates the values for the input and output paths
def script_update(settings):
    global input_path
    global output_path1
    global output_path2
    global output_path3
    input_path = obs.obs_data_get_string(settings, "inputpath")
    output_path1 = obs.obs_data_get_string(settings, "outputpath1")
    output_path2 = obs.obs_data_get_string(settings, "outputpath2")
    output_path3 = obs.obs_data_get_string(settings, "outputpath3")


# Function sets the script description in OBS
def script_description():
    return "Moves recordings to a new location when ended."


# Function sets the script properties in OBS
def script_properties():
    props = obs.obs_properties_create()
    obs.obs_properties_add_text(props, "inputpath", "Input Path", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(
        props, "outputpath1", "Output Path 1", obs.OBS_TEXT_DEFAULT
    )
    obs.obs_properties_add_text(
        props, "outputpath2", "Output Path 2", obs.OBS_TEXT_DEFAULT
    )
    obs.obs_properties_add_text(
        props, "outputpath3", "Output Path 3", obs.OBS_TEXT_DEFAULT
    )
    return props