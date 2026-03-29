# Docker Instructions for Mini-Mesh

This guide explains how to containerize your coordination server ("The Brain").

## 🧠 Running the "Brain" in Docker
Running the Brain in a container is the best way to keep it always-on and isolated.

### Step 1: Build & Start
On your main machine (where you want the Brain to live):
```bash
docker compose up -d brain
```

### Step 2: Verify
Check if the Brain is running:
```bash
docker logs minimesh-brain
```
It should say `Registered with Virtual IP: ...` when your first agents start connecting.

---

## 🛠 Running the "Agent" (Important)

### For your 5 MacBooks & 2 Windows Desktops:
**Do NOT use Docker for the Agent.**
Because Docker on macOS/Windows runs in a virtual machine (Docker Desktop), the container doesn't have direct access to your *host machine's* network hardware. This makes it very difficult to create a tunnel for the whole computer.

**The Best Way for Mac/Windows:**
1.  Install **WireGuard** and **Python** directly on the host.
2.  Run `sudo python agent.py` (macOS) or as Administrator (Windows).

### For Linux Machines (If any):
If you have a Linux server/machine, you *can* use Docker:
1.  Uncomment the `agent` section in `docker-compose.yml`.
2.  Run:
    ```bash
    docker compose up -d agent
    ```
    *Note: The `--cap-add=NET_ADMIN` and `network_mode: host` flags are essential for this to work.*

---

## 🔗 Connection Summary
1.  **Brain:** Running in Docker on `192.168.1.10:8000`.
2.  **Agents:** Running natively on each MacBook and PC.
3.  **Virtual LAN:** All machines accessible at `10.0.0.x`.
