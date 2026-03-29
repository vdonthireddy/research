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

## 🛠 Running the "Agent" in Docker

The Agent is now containerized and can be configured with environment variables.

### Step 1: Run on each machine
```bash
BRAIN_URL=http://your-brain-ip:8000 MACHINE_NAME=macbook-1 docker compose up -d agent
```

### Step 2: Environment Variables
- `BRAIN_URL`: The URL of the Brain server (e.g., `http://192.168.1.10:8000`).
- `MACHINE_NAME`: A unique name for each machine in the cluster.
- `WG_DIR`: (Optional) The directory to store WireGuard configuration. Defaults to `/etc/wireguard`.

### Important Notes:
- **Privileges:** The agent needs `--cap-add=NET_ADMIN` to configure the network interface.
- **Mac/Windows Compatibility:** You still need the **WireGuard** driver installed on your host machine. On macOS/Windows, the "Native Python" method is still recommended if you encounter networking issues.

---

## 🔗 Connection Summary
1.  **Brain:** Running in Docker on `192.168.1.10:8000`.
2.  **Agents:** Running natively on each MacBook and PC.
3.  **Virtual LAN:** All machines accessible at `10.0.0.x`.
