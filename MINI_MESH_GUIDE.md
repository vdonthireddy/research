# Mini-Mesh User Guide

Mini-Mesh is a lightweight, zero-cloud alternative to Tailscale for creating a secure network between your 5 MacBooks and 2 Windows desktops.

## 📋 Prerequisites

### On All Machines (macOS & Windows)
1.  **Python 3.x:** Installed and added to PATH.
2.  **WireGuard Tools:**
    - **macOS:** `brew install wireguard-tools`
    - **Windows:** Install the official [WireGuard for Windows](https://www.wireguard.com/install/) client.

### On the Brain Machine (1 machine only)
1.  Install FastAPI and Uvicorn:
    ```bash
    pip install fastapi uvicorn pydantic requests
    ```

---

## 🚀 Step 1: Start the "Brain"
Choose one computer (e.g., your Windows desktop) to be the coordination server.

### Option A: Using Docker (Recommended)
1. Ensure Docker is installed on the machine.
2. Build and start the Brain:
   ```bash
   docker compose up -d brain
   ```
3. The Brain is now listening on port `8000`.

### Option B: Running Manually
1. Find the local IP of this machine (e.g., `192.168.1.10`).
2. Run the Brain:
   ```bash
   python brain.py
   ```
3. The Brain is now listening on port `8000`.

---

## 🛠 Step 2: Configure the "Agent"
On **every** computer in your cluster:

1.  Open `agent.py` and update the `BRAIN_URL` at the top:
    ```python
    BRAIN_URL = "http://192.168.1.10:8000"  # Replace with your Brain's actual IP
    ```
2.  Run the agent with Admin/Root privileges:
    - **macOS:** `sudo python agent.py`
    - **Windows:** Run Command Prompt as Administrator, then `python agent.py`

---

## 🔗 Step 3: Connect
The agent will automatically:
1.  Generate WireGuard keys.
2.  Register with the Brain.
3.  Get a Virtual IP (e.g., `10.0.0.2`).
4.  Generate a `wg0.conf` file.

### Activating the Tunnel
Because creating network interfaces requires OS-level permissions, you manually start the tunnel once the config is generated:
- **macOS:** `sudo wg-quick up wg0`
- **Windows:** Open the WireGuard app, click **"Import tunnel from file,"** and select the `C:/WireGuard/wg0.conf` file created by the agent.

---

## 🔍 Testing the Connection
From any machine, try to ping another machine using its **Virtual IP**:
```bash
ping 10.0.0.1  # Ping the Brain
ping 10.0.0.3  # Ping the first MacBook
```

## 💡 Troubleshooting
1.  **Firewall:** Ensure port `51820` (UDP) is open on your Windows/macOS firewalls for local traffic.
2.  **IP Changes:** If you reboot your router and a machine gets a new local IP, the `agent.py` will automatically update the Brain and tell all other peers about the change within 60 seconds.
