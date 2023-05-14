from pathlib import Path
import obspython as obs
import os

print("Script Initialised. Let's see if it works...")
folder_path = "C://Users//joemc//Games//Age of Empires 2 DE//76561198202630125//savegame"
existing_files = [f for f in os.listdir(folder_path) if f.endswith('.aoe2record')]

def wait2start(): # Sent every 500ms
    global existing_files, file_path
    current_files = [f for f in os.listdir(folder_path) if f.endswith('.aoe2record')]
    new_file = set(current_files) - set(existing_files)
    

    # call the is_file_in_use function with the new file as argument
    file_path = os.path.join(folder_path, new_file)
    # New file detected! START OBS RECORDING!
    obs.obs_frontend_recording_start()
    obs.timer_remove(wait2start)
    obs.timer_add(wait2stop, 500)
    
    # update the existing files
    existing_files = current_files

def wait2stop(): # Sent every 500ms
    global existing_files, file_path
    path = Path(file_path)
    
    try:
        path.rename(path)
        # If the above is successful the file is no longer in use, STOP OBS RECORDING!
        obs.obs_frontend_recording_stop()
        obs.timer_remove(wait2stop)
        obs.timer_add(wait2start, 500)

    except PermissionError:
        pass
        
obs.timer_add(wait2start, 500)