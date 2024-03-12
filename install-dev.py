import requests
import platform
import os
import json
import subprocess

PIB_LINK = "https://github.com/packwiz/packwiz-installer-bootstrap/releases/download/v0.0.3/packwiz-installer-bootstrap.jar"
PACKWIZ_EXE = "packwiz" if platform.system() == "Linux" else "packwiz.exe" # FIXME: wont work on mac but who cares

MMC_PACK_JSON_SRC = {"components":[{"cachedName":"LWJGL 3","cachedVersion":"3.3.1","cachedVolatile":True,"dependencyOnly":True,"uid":"org.lwjgl3","version":"3.3.1"},{"cachedName":"Minecraft","cachedRequires":[{"suggests":"3.3.1","uid":"org.lwjgl3"}],"cachedVersion":"1.19.2","important":True,"uid":"net.minecraft","version":"1.19.2"},{"cachedName":"Forge","cachedRequires":[{"equals":"1.19.2","uid":"net.minecraft"}],"cachedVersion":"43.3.8","uid":"net.minecraftforge","version":"43.3.8"}],"formatVersion":1}
INSTANCE_CFG_WINDOWS = """[General]\nConfigVersion=1.2\niconKey=default\nname={}\nInstanceType=OneSix\nJoinServerOnLaunch=false\nOverrideCommands=true\nOverrideConsole=false\nnotes=\nOverrideEnv=false\nOverrideGameTime=false\nOverrideJavaArgs=false\nOverrideJavaLocation=false\nOverrideLegacySettings=false\nOverrideMemory=false\nOverrideMiscellaneous=false\nOverrideNativeWorkarounds=false\nOverridePerformance=false\nOverrideWindow=false\nPostExitCommand=cmd /c python "$INST_DIR/pack/generate.py"\nUseAccountForInstance=false\nPreLaunchCommand=cmd /c python "$INST_DIR/pack/update.py"\nWrapperCommand=\n"""
INSTANCE_CFG_LINUX = """[General]\nConfigVersion=1.2\niconKey=default\nname={}\nInstanceType=OneSix\nJoinServerOnLaunch=false\nOverrideCommands=true\nOverrideConsole=false\nnotes=\nOverrideEnv=false\nOverrideGameTime=false\nOverrideJavaArgs=false\nOverrideJavaLocation=false\nOverrideLegacySettings=false\nOverrideMemory=false\nOverrideMiscellaneous=false\nOverrideNativeWorkarounds=false\nOverridePerformance=false\nOverrideWindow=false\nPostExitCommand=python3 "$INST_DIR/pack/generate.py"\nUseAccountForInstance=false\nPreLaunchCommand=python3 "$INST_DIR/pack/update.py"\nWrapperCommand=\n"""

def main():
    os.chdir(os.path.realpath(os.path.dirname(__file__)))
    rev = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode().strip()

    print("creating .minecraft")
    os.makedirs("../.minecraft", exist_ok=True)

    print("populating .minecraft")
    os.chdir("../.minecraft")

    print("  downloading packwiz installer bootstrap")
    download_file(PIB_LINK)

    print("  creating prismlauncher files")
    create_mmc_pack_json()
    create_instance_cfg(rev)

    print("  finished populating\n")
    print("abyssus infinitum is now ready to get devved by u!!")

def create_mmc_pack_json():
    with open("../mmc-pack.json", "w") as fp:
        str_data = json.dumps(MMC_PACK_JSON_SRC, indent=2)
        fp.write(str_data)
    
    print("    created mmc-pack.json")

def create_instance_cfg(rev):
    with open("../instance.cfg", "w") as fp:
        data = INSTANCE_CFG_LINUX if platform.system() == "Linux" else INSTANCE_CFG_WINDOWS
        data = data.format("Abyssus Infinitum build " + rev)
        fp.write(data)

    print("    created instance.cfg")

def download_file(url: str):
    fname = url.split("/")[-1]
    
    with requests.get(url, stream=True) as r:
        r.raise_for_status()

        with open(fname, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

if __name__ == "__main__":
    main()