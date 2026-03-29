import subprocess
import requests
import socket
import os
import time

BRAIN_URL = "http://YOUR_BRAIN_IP:8000"  # Update this to your Brain's IP
MACHINE_NAME = socket.gethostname()

# Paths for WireGuard config and keys
WG_DIR = "/etc/wireguard" if os.name != "nt" else "C:/WireGuard"
PRIVATE_KEY_PATH = f"{WG_DIR}/private.key"
PUBLIC_KEY_PATH = f"{WG_DIR}/public.key"
WG_CONF_PATH = f"{WG_DIR}/wg0.conf"

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def generate_keys():
    if not os.path.exists(PRIVATE_KEY_PATH):
        print("Generating WireGuard keys...")
        priv = subprocess.check_output(["wg", "genkey"]).decode().strip()
        pub = subprocess.check_output(["wg", "pubkey"], input=priv.encode()).decode().strip()
        with open(PRIVATE_KEY_PATH, "w") as f: f.write(priv)
        with open(PUBLIC_KEY_PATH, "w") as f: f.write(pub)
    
    with open(PRIVATE_KEY_PATH, "r") as f: priv = f.read().strip()
    with open(PUBLIC_KEY_PATH, "r") as f: pub = f.read().strip()
    return priv, pub

def build_wg_conf(virtual_ip, private_key, peers):
    conf = f"""[Interface]
PrivateKey = {private_key}
Address = {virtual_ip}/24
ListenPort = 51820

"""
    for peer in peers:
        if peer['name'] == MACHINE_NAME: continue
        conf += f"""[Peer]
PublicKey = {peer['public_key']}
AllowedIPs = {peer['virtual_ip']}/32
Endpoint = {peer['local_ip']}:51820
PersistentKeepalive = 25

"""
    with open(WG_CONF_PATH, "w") as f:
        f.write(conf)
    print(f"Updated {WG_CONF_PATH}")

def run_agent():
    print(f"Starting Mini-Mesh Agent for {MACHINE_NAME}...")
    priv, pub = generate_keys()
    local_ip = get_local_ip()
    
    # 1. Register with Brain
    resp = requests.post(f"{BRAIN_URL}/register", json={
        "name": MACHINE_NAME,
        "public_key": pub,
        "local_ip": local_ip
    }).json()
    
    virtual_ip = resp['virtual_ip']
    print(f"Registered with Virtual IP: {virtual_ip}")
    
    # 2. Main Loop: Refresh peers and update config
    while True:
        try:
            peers = requests.get(f"{BRAIN_URL}/peers").json()
            build_wg_conf(virtual_ip, priv, peers)
            
            # Note: You need sudo/Admin to run these
            # subprocess.run(["wg-quick", "down", "wg0"])
            # subprocess.run(["wg-quick", "up", "wg0"])
            
            time.sleep(60)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    run_agent()
