"""
Simple PrismLauncher instance installer.

You are free to use this as long as you comply with the MIT license.
"""

import requests
import colorama
import platform
import os
import json
import subprocess
colorama.init()

WINDOWS = platform.system() == "Windows"
LINUX = platform.system() == "Linux"

PACK_NAME = "Abyssus Infinitum"
MC_VERSION = "1.19.2"
FORGE_VERSION = "43.3.8"

PIB_LINK = "https://github.com/packwiz/packwiz-installer-bootstrap/releases/download/v0.0.3/packwiz-installer-bootstrap.jar"

MMC_PACK_JSON_SRC = {"components":[{"cachedName":"LWJGL 3","cachedVersion":"3.3.1","cachedVolatile":True,"dependencyOnly":True,"uid":"org.lwjgl3","version":"3.3.1"},{"cachedName":"Minecraft","cachedRequires":[{"suggests":"3.3.1","uid":"org.lwjgl3"}],"cachedVersion":MC_VERSION,"important":True,"uid":"net.minecraft","version":MC_VERSION},{"cachedName":"Forge","cachedRequires":[{"equals":MC_VERSION,"uid":"net.minecraft"}],"cachedVersion":FORGE_VERSION,"uid":"net.minecraftforge","version":FORGE_VERSION}],"formatVersion":1}
INSTANCE_CFG_WINDOWS = """[General]\nConfigVersion=1.2\niconKey=default\nname={}\nInstanceType=OneSix\nJoinServerOnLaunch=false\nOverrideCommands=true\nOverrideConsole=false\nnotes=\nOverrideEnv=false\nOverrideGameTime=false\nOverrideJavaArgs=false\nOverrideJavaLocation=false\nOverrideLegacySettings=false\nOverrideMemory=false\nOverrideMiscellaneous=false\nOverrideNativeWorkarounds=false\nOverridePerformance=false\nOverrideWindow=false\nPostExitCommand=cmd /c python "$INST_DIR/pack/generate.py"\nUseAccountForInstance=false\nPreLaunchCommand=cmd /c python "$INST_DIR/pack/update.py"\nWrapperCommand=\n"""
INSTANCE_CFG_LINUX = """[General]\nConfigVersion=1.2\niconKey=default\nname={}\nInstanceType=OneSix\nJoinServerOnLaunch=false\nOverrideCommands=true\nOverrideConsole=false\nnotes=\nOverrideEnv=false\nOverrideGameTime=false\nOverrideJavaArgs=false\nOverrideJavaLocation=false\nOverrideLegacySettings=false\nOverrideMemory=false\nOverrideMiscellaneous=false\nOverrideNativeWorkarounds=false\nOverridePerformance=false\nOverrideWindow=false\nPostExitCommand=python3 "$INST_DIR/pack/generate.py"\nUseAccountForInstance=false\nPreLaunchCommand=python3 "$INST_DIR/pack/update.py"\nWrapperCommand=\n"""

rpath = os.path.realpath
dirn = os.path.dirname
join = os.path.join

def main():
    os.chdir(rpath(dirn(__file__)))

    is_in_correct_directory()

    rev = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode().strip()

    info("creating .minecraft")
    os.makedirs("../.minecraft", exist_ok=True)

    os.chdir("../.minecraft")

    info("downloading packwiz installer bootstrap")
    download_file(PIB_LINK)
    info("downloaded")

    info("creating prismlauncher specific files")
    create_mmc_pack_json()
    create_instance_cfg(rev)

    info(f"`{PACK_NAME} {rev}` instance created\n")
    success("restart prismlauncher if the instance has not showed up")

def create_mmc_pack_json():
    with open("../mmc-pack.json", "w") as fp:
        str_data = json.dumps(MMC_PACK_JSON_SRC, indent=2)
        fp.write(str_data)
    
    info("created mmc-pack.json")

def create_instance_cfg(rev):
    with open("../instance.cfg", "w") as fp:
        data = INSTANCE_CFG_LINUX if platform.system() == "Linux" else INSTANCE_CFG_WINDOWS
        data = data.format(f"{PACK_NAME} ver " + rev)
        fp.write(data)

    info("created instance.cfg")

def download_file(url: str):
    fname = url.split("/")[-1]
    
    with requests.get(url, stream=True) as r:
        r.raise_for_status()

        with open(fname, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

def is_in_correct_directory():
    """Parent directory's parent directory should be where Prism Launcher instances are stored."""

    if WINDOWS:
        appdata = os.getenv("APPDATA")
        if not appdata: error(f"%APPDATA% does not exist on this machine (what)")

        prismdir = join(appdata, "PrismLauncher", "instances")
    elif LINUX:
        prismdir = "~/.local/share/PrismLauncher/instances"

    given_prismdir = rpath(join(rpath(os.curdir), "..", ".."))
    
    if given_prismdir != prismdir:
        error(f"given prism dir ({given_prismdir}) is not wanted prism dir ({prismdir})")

def info(*msgs):
    print(f"{colorama.Fore.LIGHTBLACK_EX}info {colorama.Fore.RESET}{' '.join(msgs)}")

def disclaimer(*msgs):
    print(f"{colorama.Fore.LIGHTYELLOW_EX}disclaimer {colorama.Fore.RESET}{' '.join(msgs)}")

def error(*msgs):
    print(f"{colorama.Fore.LIGHTRED_EX}error {colorama.Fore.RESET}{' '.join(msgs)}")
    exit(0)

def success(*msgs):
    print(f"{colorama.Fore.LIGHTGREEN_EX}success {colorama.Fore.RESET}{' '.join(msgs)}")

if __name__ == "__main__":
    main()