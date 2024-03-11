# another script stolen from modern modpacks!!

from os import system, chdir, path
from subprocess import Popen

def main():
    chdir(path.dirname(path.realpath(__file__)))

    server = Popen(["packwiz", "serve"])

    chdir(path.join("..", ".minecraft"))
    system("java -jar packwiz-installer-bootstrap.jar http://localhost:8080/pack.toml")

    server.kill()

if __name__ == "__main__":
    main()