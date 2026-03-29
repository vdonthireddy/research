# Mini-Mesh: Lightweight Home Cluster Network

Mini-Mesh is a zero-cloud, lightweight alternative to Tailscale designed to connect multiple Macs and Windows PCs for distributed computing (rendering, AI training, etc.).

---

# ⚡️ Quickstart Guide

Get your 5 MacBooks and 2 Windows PCs connected in under 5 minutes.

## 1. Start the Brain (Main Machine)
Run this on your primary machine (e.g., your Windows desktop).
```bash
docker compose up -d brain
```
*Your Brain is now waiting for connections on port `8000`.*

---

## 2. Start the Agents (All Machines)
Run this on your 5 MacBooks and 2 Windows desktops.

1.  **Configure:** Edit `agent.py` and set `BRAIN_URL` to your Brain's local IP:
    ```python
    BRAIN_URL = "http://192.168.1.10:8000"
    ```
2.  **Run (macOS):**
    ```bash
    sudo python3 agent.py
    ```
3.  **Run (Windows):** Open Command Prompt as Administrator:
    ```cmd
    python agent.py
    ```

---

## 3. Enable the Tunnel
Once the Agent says `Updated wg0.conf`:

- **macOS:** `sudo wg-quick up wg0`
- **Windows:** Import the `C:/WireGuard/wg0.conf` file into the WireGuard desktop app and click **Activate**.

---

## 4. Test the Connection
Ping any machine in your cluster using its **Virtual IP**:
- Brain: `10.0.0.1`
- First Worker: `10.0.0.2`
- Second Worker: `10.0.0.3`

**Success!** Your 7 machines are now connected via a secure, private Virtual LAN.

---

## 📂 Documentation
- [Distributed Computing Setup Guide](distributed_computing_setup.md)
- [Mini-Mesh Detailed User Guide](MINI_MESH_GUIDE.md)
- [Docker Setup Guide](DOCKER_GUIDE.md)
- [Technical Design Doc](mini_mesh_design.md)
