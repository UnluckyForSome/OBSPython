from pathlib import Path
import obspython as obs
import os

folder_path = "C://Users//joemc//Games//Age of Empires 2 DE//76561198202630125//savegame"
existing_files = [f for f in os.listdir(folder_path) if f.endswith('.aoe2record')]



def wait2start(): # Sent every 500ms
    global existing_files, file_path
    current_files = [f for f in os.listdir(folder_path) if f.endswith('.aoe2record')]
    new_files = set(current_files) - set(existing_files)
    
    if obs.obs_frontend_recording_active() is False:
    
        for new_file in new_files:
            # call the is_file_in_use function with the new file as argument
            file_path = os.path.join(folder_path, new_file)
            # New file detected! START OBS RECORDING!

            obs.obs_frontend_recording_start()
            obs.timer_remove(wait2start)
            obs.timer_add(wait2stop, 500)
    
    # update the existing files
    existing_files = current_files

def wait2stop(): # Sent every 500ms
    global existing_files, file_path, userecstop
    path = Path(file_path)
    print ("userecstop@wait2stop:", userecstop)
    if userecstop is True:
        try:
            path.rename(path)
            print ("checking if file in use...")
            # If the above is successful the file is no longer in use, STOP OBS RECORDING!
            obs.obs_frontend_recording_stop()
            obs.timer_remove(wait2stop)
            obs.timer_add(wait2start, 500)

        except PermissionError:
            pass
    else:   
            obs.timer_remove(wait2stop)
            obs.timer_add(wait2start, 500)

def script_defaults(settings):
    global toggle, userecstop
    obs.obs_data_set_default_bool(settings, "toggle", False)

def script_update(settings):
    global toggle, userecstop
    userecstop = obs.obs_data_get_bool(settings, "toggle")
    print ("userecstop:", userecstop)

# Function sets the script description in OBS
def script_description():
    return "Automagically detects AOE2:DE matches and starts recording"

def script_properties():
    props = obs.obs_properties_create()
    obs.obs_properties_add_bool(props, "toggle", "Allow script to end recordings?")
    return props
        
obs.timer_add(wait2start, 500)