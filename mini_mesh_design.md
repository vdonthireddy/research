# Design Doc: Mini-Mesh (Lightweight Tailscale Alternative)

## 1. Goal
To create a zero-config mesh network for 5 MacBooks and 2 Windows PCs to enable distributed computing without using third-party cloud services.

## 2. Components

### A. The "Brain" (Coordination Server)
- **Language:** Python (FastAPI).
- **Function:** A simple database (in-memory or SQLite) that maps `machine_name` -> `public_key`, `virtual_ip`, and `endpoint_ip`.
- **API Endpoints:**
    - `POST /register`: Machine sends its name, public key, and current local IP.
    - `GET /peers`: Machine downloads the list of all other registered peers.

### B. The "Agent" (Client Script)
- **Language:** Python.
- **Dependencies:** `wireguard-tools` (the `wg` command).
- **Workflow:**
    1. Check if `private.key` exists; if not, generate a new pair using `wg genkey`.
    2. Detect local IP address.
    3. Call `/register` on the Brain.
    4. Call `/peers` every 60 seconds.
    5. If the peer list changes, regenerate `/etc/wireguard/wg0.conf` and run `wg-quick up wg0`.

## 3. Virtual IP Strategy
We will use the `10.0.0.x` subnet.
- Brain: `10.0.0.1` (Assumed to be the first registered)
- Peers: `10.0.0.2` to `10.0.0.254`

## 4. Technical Hurdles
- **Root/Admin Access:** WireGuard requires `sudo` (macOS/Linux) or Administrator (Windows) to create network interfaces.
- **NAT Traversal:** In a pure local environment, we don't need STUN/ICE. If moving outside the home, we would need a "Relay" (DERP) similar to Tailscale.
