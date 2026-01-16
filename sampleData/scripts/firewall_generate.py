import random
import time
from datetime import datetime

OUTPUT_FILE = "/tmp/splunk/firewall_attack_logs.log"
HOSTNAME = "fw01"

def timestamp():
    return datetime.now().strftime("%b %d %H:%M:%S")

def write_log(line):
    with open(OUTPUT_FILE, "a") as f:
        f.write(line + "\n")
    print(line)

# -------------------------------
# Attack Simulations
# -------------------------------

def port_scan():
    src_ip = "203.0.113.45"
    dest_ip = "10.0.0.10"
    ports = [22, 23, 80, 443, 3389, 8080, 21]
    for port in ports:
        log = f"<134>{timestamp()} {HOSTNAME} action=blocked src_ip={src_ip} dest_ip={dest_ip} dest_port={port} protocol=TCP"
        write_log(log)
        time.sleep(0.3)

def brute_force():
    src_ip = "198.51.100.77"
    dest_ip = "10.0.0.20"
    for _ in range(8):
        log = f"<134>{timestamp()} {HOSTNAME} action=blocked src_ip={src_ip} dest_ip={dest_ip} dest_port=22 protocol=TCP"
        write_log(log)
        time.sleep(0.5)

def ddos():
    dest_ip = "10.0.0.30"
    for _ in range(50):
        src_ip = f"192.0.2.{random.randint(1,254)}"
        log = f"<134>{timestamp()} {HOSTNAME} action=allowed src_ip={src_ip} dest_ip={dest_ip} dest_port=80 protocol=TCP"
        write_log(log)
        time.sleep(0.05)

def c2_callback():
    src_ip = "10.0.0.50"
    dest_ip = "185.220.101.45"
    for _ in range(3):
        log = f"<134>{timestamp()} {HOSTNAME} action=allowed src_ip={src_ip} dest_ip={dest_ip} dest_port=4444 protocol=TCP"
        write_log(log)
        time.sleep(2)

# -------------------------------
# Main
# -------------------------------

if __name__ == "__main__":
    print("[+] Generating firewall attack logs...\n")

    port_scan()
    brute_force()
    ddos()
    c2_callback()

    print("\n[+] Log generation complete!")
    print(f"[+] Output file: {OUTPUT_FILE}")
