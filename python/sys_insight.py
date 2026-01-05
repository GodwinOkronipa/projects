import os
import time
import platform
import shutil

def get_platform_info():
    return f"{platform.system()} {platform.release()} ({platform.machine()})"

def get_cpu_info():
    # Fallback if psutil is not installed
    try:
        import psutil
        return f"{psutil.cpu_percent()}%"
    except ImportError:
        return "Install 'psutil' for real-time CPU data"

def get_mem_info():
    try:
        import psutil
        mem = psutil.virtual_memory()
        return f"{mem.percent}% ({mem.used // (1024**2)}MB / {mem.total // (1024**2)}MB)"
    except ImportError:
        return "Install 'psutil' for real-time Memory data"

def get_disk_info():
    total, used, free = shutil.disk_usage("/")
    return f"{(used/total)*100:.1f}% ({used // (1024**3)}GB / {total // (1024**3)}GB)"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    try:
        while True:
            clear_screen()
            print("="*50)
            print(" 🖥️  SYSTEM RESOURCE MONITOR")
            print("="*50)
            print(f"📅 Time:     {time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"💻 OS:       {get_platform_info()}")
            print(f"🧠 CPU:      {get_cpu_info()}")
            print(f"💾 Memory:   {get_mem_info()}")
            print(f"💿 Disk (/): {get_disk_info()}")
            print("="*50)
            print("Press Ctrl+C to exit...")
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nExiting monitor...")

if __name__ == "__main__":
    main()
