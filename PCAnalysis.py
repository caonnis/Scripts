import psutil
import platform
import cpuinfo
import GPUtil
import wmi
from tabulate import tabulate
from colorama import init, Fore, Style

init(autoreset=True)

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def print_section(title):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{title}")
    print(f"{Fore.CYAN}{Style.BRIGHT}{'=' * len(title)}")

def analyze_system():
    print_section("Información del Sistema")
    c = wmi.WMI()
    system = c.Win32_ComputerSystem()[0]
    os = c.Win32_OperatingSystem()[0]
    bios = c.Win32_BIOS()[0]
    
    system_data = [
        ["Fabricante", system.Manufacturer],
        ["Modelo", system.Model],
        ["Nombre", system.Name],
        ["Sistema Operativo", f"{os.Caption} {os.Version}"],
        ["Arquitectura", os.OSArchitecture],
        ["Versión de BIOS", bios.Version],
        ["Fecha de BIOS", bios.ReleaseDate]
    ]
    print(tabulate(system_data, tablefmt="grid"))

def analyze_cpu():
    print_section("Información de CPU")
    try:
        cpu_info = cpuinfo.get_cpu_info()
        cpu_freq = psutil.cpu_freq()
        c = wmi.WMI()
        processor = c.Win32_Processor()[0]
        
        cpu_data = [
            ["Procesador", cpu_info.get('brand_raw', 'N/A')],
            ["Fabricante", processor.Manufacturer],
            ["Modelo", processor.Name],
            ["Arquitectura", cpu_info.get('arch', 'N/A')],
            ["Bits", cpu_info.get('bits', 'N/A')],
            ["Frecuencia base", f"{processor.MaxClockSpeed}MHz"],
            ["Frecuencia actual", f"{cpu_freq.current:.2f}MHz" if cpu_freq else 'N/A'],
            ["Núcleos físicos", psutil.cpu_count(logical=False)],
            ["Núcleos lógicos", psutil.cpu_count(logical=True)],
            ["Uso de CPU", f"{psutil.cpu_percent()}%"],
            ["Cache L2", get_size(processor.L2CacheSize * 1024) if processor.L2CacheSize else 'N/A'],
            ["Cache L3", get_size(processor.L3CacheSize * 1024) if processor.L3CacheSize else 'N/A']
        ]
        print(tabulate(cpu_data, tablefmt="grid"))
    except Exception as e:
        print(f"{Fore.RED}Error al obtener información de la CPU: {e}")

def analyze_memory():
    print_section("Memoria")
    svmem = psutil.virtual_memory()
    c = wmi.WMI()
    physical_memory = c.Win32_PhysicalMemory()
    
    memory_data = [
        ["Total", get_size(svmem.total)],
        ["Disponible", get_size(svmem.available)],
        ["Usada", get_size(svmem.used)],
        ["Porcentaje", f"{svmem.percent}%"]
    ]
    print(tabulate(memory_data, tablefmt="grid"))
    
    print("\nMódulos de memoria:")
    for module in physical_memory:
        module_data = [
            ["Fabricante", module.Manufacturer],
            ["Parte", module.PartNumber.strip()],
            ["Capacidad", get_size(int(module.Capacity))],
            ["Velocidad", f"{module.Speed} MHz"],
            ["Tipo", module.MemoryType]
        ]
        print(tabulate(module_data, tablefmt="grid"))

def analyze_disk():
    print_section("Disco")
    c = wmi.WMI()
    for disk in c.Win32_DiskDrive():
        print(f"{Fore.YELLOW}Disco: {disk.Caption}")
        disk_data = [
            ["Modelo", disk.Model],
            ["Fabricante", disk.Manufacturer],
            ["Número de Serie", disk.SerialNumber.strip()],
            ["Tipo de Interfaz", disk.InterfaceType],
            ["Tamaño", get_size(int(disk.Size))],
            ["Particiones", disk.Partitions]
        ]
        print(tabulate(disk_data, tablefmt="grid"))
        
        partitions = c.Win32_DiskPartition(DiskIndex=disk.Index)
        for partition in partitions:
            logical_disks = c.Win32_LogicalDisk(DeviceID=partition.DeviceID)
            for logical_disk in logical_disks:
                try:
                    usage = psutil.disk_usage(logical_disk.DeviceID)
                    partition_data = [
                        ["Letra de Unidad", logical_disk.DeviceID],
                        ["Sistema de Archivos", logical_disk.FileSystem],
                        ["Total", get_size(usage.total)],
                        ["Usado", get_size(usage.used)],
                        ["Libre", get_size(usage.free)],
                        ["Porcentaje", f"{usage.percent}%"]
                    ]
                    print(tabulate(partition_data, tablefmt="grid"))
                except:
                    pass

def analyze_gpu():
    print_section("GPU")
    try:
        c = wmi.WMI()
        gpus = c.Win32_VideoController()
        
        for gpu in gpus:
            gpu_data = [
                ["Nombre", gpu.Name],
                ["Fabricante", gpu.AdapterCompatibility],
                ["Memoria de Video", get_size(int(gpu.AdapterRAM)) if gpu.AdapterRAM else 'N/A'],
                ["Resolución Actual", f"{gpu.CurrentHorizontalResolution}x{gpu.CurrentVerticalResolution}"]
            ]
            print(tabulate(gpu_data, tablefmt="grid"))
        
        gpus_gpu_util = GPUtil.getGPUs()
        if gpus_gpu_util:
            for gpu in gpus_gpu_util:
                gpu_util_data = [
                    ["Uso de GPU", f"{gpu.load*100:.2f}%"],
                    ["Temperatura", f"{gpu.temperature} °C"],
                    ["Memoria Libre", f"{gpu.memoryFree}MB"],
                    ["Memoria Usada", f"{gpu.memoryUsed}MB"],
                    ["Memoria Total", f"{gpu.memoryTotal}MB"]
                ]
                print(tabulate(gpu_util_data, tablefmt="grid"))
    except Exception as e:
        print(f"{Fore.RED}Error al obtener información detallada de la GPU: {e}")

def analyze_network():
    print_section("Red")
    try:
        c = wmi.WMI()
        nics = c.Win32_NetworkAdapterConfiguration(IPEnabled=True)
        
        for nic in nics:
            print(f"{Fore.YELLOW}Adaptador de Red: {nic.Description}")
            network_data = [
                ["Dirección MAC", nic.MACAddress],
                ["DHCP Habilitado", nic.DHCPEnabled],
                ["Dirección IP", nic.IPAddress[0] if nic.IPAddress else 'N/A'],
                ["Máscara de Subred", nic.IPSubnet[0] if nic.IPSubnet else 'N/A'],
                ["Gateway Predeterminado", nic.DefaultIPGateway[0] if nic.DefaultIPGateway else 'N/A'],
                ["Servidores DNS", ', '.join(nic.DNSServerSearchOrder) if nic.DNSServerSearchOrder else 'N/A']
            ]
            print(tabulate(network_data, tablefmt="grid"))
        
        net_io = psutil.net_io_counters()
        print("\nEstadísticas de red generales:")
        net_stats = [
            ["Bytes enviados", get_size(net_io.bytes_sent)],
            ["Bytes recibidos", get_size(net_io.bytes_recv)],
            ["Paquetes enviados", net_io.packets_sent],
            ["Paquetes recibidos", net_io.packets_recv]
        ]
        print(tabulate(net_stats, tablefmt="grid"))
    except Exception as e:
        print(f"{Fore.RED}Error al obtener información de red: {e}")

def main():
    analyze_system()
    analyze_cpu()
    analyze_memory()
    analyze_disk()
    analyze_gpu()
    analyze_network()

if __name__ == "__main__":
    main()