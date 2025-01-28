import argparse
import subprocess
import os
import sys
import time

DEBIAN = "Debian"
FEDORA = "Fedora"


appsBase = {
    "Dependencias": {
        FEDORA: ["sudo dnf install -y git wget curl"],
        DEBIAN: ["sudo apt install -y git wget curl software-properties-common apt-transport-https gpg"]
    },
    "Brave": {
        FEDORA: ["curl -fsS https://dl.brave.com/install.sh | sh"],
        DEBIAN: ["curl -fsS https://dl.brave.com/install.sh | sh"]
    },
    "Visual Studio Code": {
        FEDORA: [
            "sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc",
            "echo -e \"[code]\\nname=Visual Studio Code\\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\\nenabled=1\\ngpgcheck=1\\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc\" | sudo tee /etc/yum.repos.d/vscode.repo > /dev/null",
            "dnf check-update",
            "sudo dnf install code -y"
        ],
        DEBIAN: [
            "wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg",
            "sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg",
            "echo \"deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main\" |sudo tee /etc/apt/sources.list.d/vscode.list > /dev/null",
            "rm -f packages.microsoft.gpg"
        ]
    },
    "TLP y tlp-rdw": {
        FEDORA: ["sudo dnf install tlp tlp-rdw -y"],
        DEBIAN: ["sudo apt install -y tlp tlp-rdw"]
    },
    "auto-cpufreq": {
        FEDORA: [
            "git clone https://github.com/AdnanHodzic/auto-cpufreq.git",
            "cd auto-cpufreq && sudo ./auto-cpufreq-installer"
        ],
        DEBIAN: [
            "git clone https://github.com/AdnanHodzic/auto-cpufreq.git",
            "cd auto-cpufreq && sudo ./auto-cpufreq-installer"
        ]
    },
    "snap": {
        FEDORA: [
            "sudo dnf install snapd -y",
            "sudo ln -s /var/lib/snapd/snap /snap"
        ],
        DEBIAN: [
            "sudo apt install -y snapd",
            "sudo snap install core"
        ]
    },
    "htop": {
        FEDORA: ["sudo dnf install htop -y"],
        DEBIAN: ["sudo apt install -y htop"]
    },
    "fastfetch": {
        FEDORA: ["sudo dnf install fastfetch -y"],
        DEBIAN: ["sudo apt install -y fastfetch"]
    },
    "easy effects": {
        FEDORA: ["sudo dnf install easyeffects -y"],
        DEBIAN: [
            "sudo add-apt-repository ppa:mjblenner/easyeffects",
            "sudo apt update",
            "sudo apt install -y easyeffects"
            ]    
    }
}


appsDesarolladores = {
    "Dependencias": {
        FEDORA: ["sudo dnf -y install dnf-plugins-core",],
        DEBIAN: ["sudo apt install apt-transport-https ca-certificates curl software-properties-common -y"]
    },
    "docker": {
        FEDORA: [
            "sudo dnf-3 config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo",
            "sudo dnf -y install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin",
            "sudo systemctl enable --now docker"
            ],
        DEBIAN: [
            "sudo install -m 0755 -d /etc/apt/keyrings",
            "sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc",
            "sudo chmod a+r /etc/apt/keyrings/docker.asc",
            "echo \"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo \\\"$VERSION_CODENAME\\\") stable\" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null",
            "sudo apt update",
            "sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin"
        ]
    },
    "Java JDK": {
        FEDORA: ["sudo dnf install java-latest-openjdk-devel -y"],
        DEBIAN: ["sudo apt -y install default-jdk"]
    },
    "PHP": {
        FEDORA: [
            "sudo dnf install php php-cli php-common php-json php-xml php-mbstring php-zip php-mysqlnd php-pdo php-gd php-xmlrpc php-opcache php-pecl-imagick php-pecl-xdebug -y",
            ],
        DEBIAN: [
            "sudo apt install -y php php-cli php-common php-json php-xml php-mbstring php-zip php-mysql php-pdo php-gd php-xmlrpc php-opcache php-imagick php-xdebug"
        ]
    },
    "gcc": {
        FEDORA: ["sudo dnf groupinstall \"Development Tools\" -y"],
        DEBIAN: ["sudo apt install -y build-essential"]
    }
}

apssRedes = {
    "Dependencias": {
        FEDORA: ["sudo dnf install -y dnf-plugins-core"],
        DEBIAN: ["sudo apt install -y gnupg"]
    },
    
    "Proton VPN": {
        FEDORA: [
            "wget \"https://repo.protonvpn.com/fedora-$(cat /etc/fedora-release | cut -d' ' -f 3)-stable/protonvpn-stable-release/protonvpn-stable-release-1.0.2-1.noarch.rpm\"",
            "sudo dnf install -y ./protonvpn-stable-release-1.0.2-1.noarch.rpm && sudo dnf check-update --refresh ",
            "sudo dnf install proton-vpn-gnome-desktop -y"
            ],
        DEBIAN: [
            "wget https://repo.protonvpn.com/debian/dists/stable/main/binary-all/protonvpn-stable-release_1.0.6_all.deb",
            "sudo dpkg -i ./protonvpn-stable-release_1.0.6_all.deb && sudo apt update",
            "echo \"e5e03976d0980bafdf07da2f71b14fbc883c091e72b16772199742c98473002f protonvpn-stable-release_1.0.6_all.deb\" | sha256sum --check -",
            "sudo apt install proton-vpn-gnome-desktop -y",
            "sudo apt install libayatana-appindicator3-1 gir1.2-ayatanaappindicator3-0.1 gnome-shell-extension-appindicator -y"
        ]
    },
    "tor": {
        FEDORA: [
            "sudo dnf config-manager --add-repo https://rpm.torproject.org/torrepo.repo",
            "sudo rpm --import https://support.torproject.org/static/keys/tpa.asc",
            "sudo dnf install -y tor torbrowser-launcher",
            "sudo systemctl enable tor"
            ],
        DEBIAN: [
            "gpg --keyserver hkp://keyserver.ubuntu.com --recv-keys 74A941BA219EC810",
            "echo \"deb [arch=amd64 signed-by=/usr/share/keyrings/tor-archive-keyring.gpg] https://deb.torproject.org/torproject.org $(lsb_release -cs) main\" | sudo tee /etc/apt/sources.list.d/tor.list",
            "sudo apt update",
            "sudo apt install -y tor torbrowser-launcher",
            "sudo systemctl enable tor"
        ]
    },
    "net-tools (ifconfig)": {
        FEDORA: ["sudo dnf install net-tools -y"],
        DEBIAN: ["sudo apt install net-tools -y"]
    },
    "nmap": {
        FEDORA: ["sudo dnf install nmap -y"],
        DEBIAN: ["sudo apt install nmap -y"]
    }
}

def check_sudo():
    """Verifica si el script se está ejecutando como root."""
    if os.geteuid() != 0:
        print("Este script debe ejecutarse con privilegios de superusuario (sudo).")
        sys.exit(1)

def detectar_gestor_paquetes() -> str | None: 
    try:
        # Intentar encontrar `apt`
        result = subprocess.run(
            ["which", "apt"], 
            capture_output=True,
            text=True
            )
        
        if result.returncode == 0:
            print("El gestor de paquetes es apt (Debian/Ubuntu).")
            return DEBIAN
        
        # Intentar encontrar `dnf`
        result = subprocess.run(
            ["which", "dnf"], 
            capture_output=True,
            text=True
            )
        
        if result.returncode == 0:
            print("El gestor de paquetes es dnf (Fedora).")
            return FEDORA
        # Ningún gestor de paquetes compatible detectado
        print("No se detectó un gestor de paquetes compatible.")
        return None
    
    except Exception as e:
        # Ningún gestor de paquetes compatible detectado
        print("No se detectó un gestor de paquetes compatible.")
        print(e)
        return None
        
def instalacion_basica():
    for app, sistema in appsBase.items():
        print(f"Instalando {app}...")
        time.sleep(1)
        for comando in sistema[gestor_paquetes]:
            print(f"Comando a ejecutar: \n\033[94>> {comando}\033[0m")
            time.sleep(1)
            subprocess.run(comando, shell=True, check=True)
        print("-" * 50)  # Separador entre aplicaciones
        
def instalacion_desarrolladores():        
    for app, sistema in appsDesarolladores.items():
        print(f"Instalando {app}...")
        time.sleep(1)
        for comando in sistema[gestor_paquetes]:
            print(f"Comando a ejecutar: \n\033[94>> {comando}\033[0m")
            time.sleep(1)
            subprocess.run(comando, shell=True, check=True)
        print("-" * 50)  # Separador entre aplicaciones
        
def instalacion_redes():
    for app, sistema in apssRedes.items():
        print(f"Instalando {app}...")
        time.sleep(1)
        for comando in sistema[gestor_paquetes]:
            print(f"Comando a ejecutar: \n>> {comando}")
            time.sleep(1)
            subprocess.run(comando, shell=True, check=True)
        print("-" * 70)  # Separador entre aplicaciones

if __name__ == "__main__":
    # Verificar si se está ejecutando como superusuario
    check_sudo()

    # Detectar el gestor de paquetes
    gestor_paquetes = detectar_gestor_paquetes()
    if not gestor_paquetes:
        exit(1)
        
    # Crear el parser
    parser = argparse.ArgumentParser(
        description="Aplicación para instalar paquetes específicos."
    )
    
    # Agregar los argumentos
    group = parser.add_mutually_exclusive_group()  # Crear un grupo mutuamente exclusivo
    group.add_argument(
        "--all", "-a",
        action="store_true",
        help="Instala todas las aplicaciones (por defecto)."
    )
    group.add_argument(
        "--basic", "-b",
        action="store_true",
        help="Instala las aplicaciones básicas."
    )
    group.add_argument(
        "--dev", "-d",
        action="store_true",
        help="Instala las aplicaciones de desarrollo."
    )
    group.add_argument(
        "--net", "-n",
        action="store_true",
        help="Instala las aplicaciones de red."
    )
    
    # Parsear los argumentos
    args = parser.parse_args()
    
    print("Bienvenido a la aplicación de instalación de paquetes.")
    print("Primero actualizaremos el sistema...")
    
    # Actualizar el sistema
    if gestor_paquetes == DEBIAN:
        subprocess.run(["sudo", "apt", "update"])
        subprocess.run(["sudo", "apt", "upgrade", "-y"])
    else:
        subprocess.run(["sudo", "dnf", "update", "-y"])
        
    print("Sistema actualizado.")
    print("ADVERTENCIA: Por seguridad del sistema despues de ejecutar este script, se recomienda reiniciar el sistema.")
    
    arg_all = bool(args.all or not (args.basic or args.dev or args.net))
    arg_basic = bool(args.basic)
    arg_dev = bool(args.dev)
    arg_net = bool(args.net)
    
    #Lista de apps 
    keys_resultantes = [
    key
    for dic, cond in [
        (appsBase, arg_all or arg_basic),
        (appsDesarolladores, arg_all or arg_dev),
        (apssRedes, arg_all or arg_net),
    ]
    if cond  # Solo considerar los diccionarios cuyo booleano sea True
    for key in dic.keys()
]
    
    print("Lista de apps a instalar:")
    for key in keys_resultantes:
        print(key)
        
    print("Desea continuar con la instalación? (y/n)")
    respuesta = input()
    
    if respuesta.lower() not in ["y", "yes", "s", "si"]:
        print("Instalación cancelada.")
        exit(0)
    
    # Lógica para manejar los argumentos
    if args.all or not (args.basic or args.dev or args.net):  # Por defecto, --all
        print("Instalando todas las aplicaciones...")
        
        instalacion_basica()
        instalacion_desarrolladores()
        instalacion_redes()
        
    elif args.basic:
        print("Instalando las aplicaciones básicas...")
        
        instalacion_basica()
        
    elif args.dev:
        print("Instalando las aplicaciones de desarrollo...")
        
        instalacion_desarrolladores()
        
    elif args.net:
        print("Instalando las aplicaciones de red...")
        
        instalacion_redes()
        
    else:
        print("Ninguna opción válida seleccionada.")
    
    

