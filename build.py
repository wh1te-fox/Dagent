import argparse
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
ENTRY = SRC / "page.py"
ASSETS = SRC / "assets"
ICON = ASSETS / "logo.ico"
APP_NAME = "Dagent"


def run(command, **kwargs):
    print(f"\n> {' '.join(map(str, command))}")
    subprocess.check_call(command, **kwargs)


def ensure_dependencies():
    python = sys.executable

    run([python, "-m", "pip", "install", "--upgrade", "pyinstaller"])


def build():
    system = platform.system()

    if system not in ("Windows", "Linux"):
        print(f"ERROR: Sistema no compatible: {system}")
        sys.exit(1)

    if not ENTRY.exists():
        print(f"ERROR: No se encuentra el archivo principal: {ENTRY}")
        sys.exit(1)

    python = sys.executable
    separator = ";" if system == "Windows" else ":"

    command = [
        python, "-m", "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onefile",
        "--name", APP_NAME,
        "--paths", str(SRC),
        "--collect-all", "flet",
        "--add-data", f"{ASSETS}{separator}assets",
    ]

    if system == "Windows":
        command.append("--windowed")
        if ICON.exists():
            command.extend(["--icon", str(ICON)])
            command.extend(["--add-data", f"{ICON}{separator}assets"])
        else:
            print(f"AVISO: No se encontró el icono: {ICON}")
    elif ICON.exists():
        command.extend(["--add-data", f"{ICON}{separator}assets"])

    command.append(str(ENTRY))

    executable_name = f"{APP_NAME}.exe" if system == "Windows" else APP_NAME
    executable = ROOT / "dist" / executable_name

    if executable.exists():
        executable.unlink()

    run(command)

    if not executable.exists():
        print("\nERROR: No se generó el ejecutable.")
        sys.exit(1)

    if system == "Linux":
        executable.chmod(executable.stat().st_mode | 0o111)

    print("\n" + "=" * 45)
    print(f"{APP_NAME.upper()} COMPILADO CORRECTAMENTE")
    print(f"Ejecutable: {executable}")
    print("=" * 45)
    return executable


def windows_install_dir():
    return Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local")) / "Programs" / APP_NAME


def install_windows(executable):
    target_dir = windows_install_dir()
    target_dir.mkdir(parents=True, exist_ok=True)
    target_exe = target_dir / executable.name
    shutil.copy2(executable, target_exe)

    start_menu = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming")) / "Microsoft" / "Windows" / "Start Menu" / "Programs"
    shortcut = start_menu / f"{APP_NAME}.lnk"

    if not start_menu.exists():
        start_menu.mkdir(parents=True, exist_ok=True)

    powershell = (
        "$ws = New-Object -ComObject WScript.Shell; "
        f"$s = $ws.CreateShortcut('{shortcut}'); "
        f"$s.TargetPath = '{target_exe}'; "
        f"$s.WorkingDirectory = '{target_dir}'; "
        "$s.Save()"
    )
    run(["powershell", "-NoProfile", "-Command", powershell])

    print("\n" + "=" * 45)
    print("INSTALACIÓN COMPLETADA (Windows)")
    print(f"Ejecutable: {target_exe}")
    print(f"Acceso directo: {shortcut}")
    print("Aplicación disponible en el menú de inicio.")
    print("=" * 45)


def linux_install_paths():
    home = Path.home()
    return {
        "bin_dir": home / ".local" / "bin",
        "icon_file": home / ".local" / "share" / "icons" / "hicolor" / "256x256" / "apps" / "dagent.ico",
        "desktop_file": home / ".local" / "share" / "applications" / "dagent.desktop",
    }


def install_linux(executable):
    paths = linux_install_paths()
    paths["bin_dir"].mkdir(parents=True, exist_ok=True)
    paths["icon_file"].parent.mkdir(parents=True, exist_ok=True)
    paths["desktop_file"].parent.mkdir(parents=True, exist_ok=True)

    target_exe = paths["bin_dir"] / APP_NAME
    shutil.copy2(executable, target_exe)
    target_exe.chmod(target_exe.stat().st_mode | 0o111)

    if ICON.exists():
        shutil.copy2(ICON, paths["icon_file"])
    else:
        print(f"AVISO: No se encontró el icono: {ICON}")

    icon_ref = paths["icon_file"] if ICON.exists() else APP_NAME.lower()
    desktop_entry = (
        "[Desktop Entry]\n"
        f"Name={APP_NAME}\n"
        "Comment=Sistema de Gestión de Ventas, Productos y Clientes\n"
        f"Exec={target_exe}\n"
        "Type=Application\n"
        f"Icon={icon_ref}\n"
        "Terminal=false\n"
        "Categories=Office;Finance;\n"
        f"StartupWMClass={APP_NAME}\n"
    )
    paths["desktop_file"].write_text(desktop_entry, encoding="utf-8")

    if shutil.which("update-desktop-database"):
        run(["update-desktop-database", str(paths["desktop_file"].parent)])

    print("\n" + "=" * 45)
    print("INSTALACIÓN COMPLETADA (Linux)")
    print(f"Ejecutable: {target_exe}")
    print(f"Lanzador: {paths['desktop_file']}")
    print("Si no aparece en el menú, cierra sesión y vuelve a entrar.")
    print("=" * 45)


def install():
    executable = build()
    system = platform.system()

    if system == "Windows":
        install_windows(executable)
    else:
        install_linux(executable)


def uninstall():
    system = platform.system()
    removed = []

    if system == "Windows":
        targets = [
            windows_install_dir(),
            Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming")) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / f"{APP_NAME}.lnk",
        ]
    else:
        paths = linux_install_paths()
        targets = [paths["bin_dir"] / APP_NAME, paths["icon_file"], paths["desktop_file"]]

    for target in targets:
        if target.is_dir():
            shutil.rmtree(target)
            removed.append(target)
        elif target.exists():
            target.unlink()
            removed.append(target)

    if removed:
        print("Elementos eliminados:")
        for item in removed:
            print(f"  - {item}")
    else:
        print("No se encontraron elementos instalados.")


def main():
    parser = argparse.ArgumentParser(description=f"Instalador de {APP_NAME} (Windows/Linux).")
    parser.add_argument(
        "command",
        nargs="?",
        default="install",
        choices=["install", "build", "uninstall"],
        help="install: compila e instala (por defecto), build: solo compila, uninstall: desinstala",
    )
    args = parser.parse_args()

    if args.command == "build":
        build()
    elif args.command == "uninstall":
        uninstall()
    else:
        ensure_dependencies()
        install()


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as error:
        print(f"\nERROR: El comando falló con código {error.returncode}.")
        sys.exit(error.returncode)
    except KeyboardInterrupt:
        print("\nProceso cancelado.")
        sys.exit(130)
