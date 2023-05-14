from pathlib import Path
import os

file_path = "C://Users//joemc//Games//Age of Empires 2 DE//76561198202630125//savegame//SP Replay v101.102.15522.0 #(81058) @2023.04.14 173448.aoe2record"
path = Path(file_path)

try:
     path.rename(path)
    # If the above is successful the file is no longer in use, STOP OBS RECORDING!
except PermissionError:
     print("Specified file is currently being written to!")