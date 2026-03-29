# Home Cluster Setup: Combining Macs & Windows PCs

This guide outlines how to leverage 5 MacBooks and 2 Windows desktops for heavy distributed computing during idle time.

## 1. Core Concepts
Distributed computing doesn't create one "giant" computer; instead, it uses a **Manager/Worker** architecture where tasks are split into "chunks" and sent to different machines.

- **Head/Master Node:** The computer you use to start the job.
- **Worker Nodes:** The idle computers that perform the calculations.
- **Task Granularity:** Tasks must be "parallelizable" (e.g., rendering individual frames of a video or processing separate rows of a dataset).

---

## 2. Software Solutions by Use Case

### 🧪 Data Science & AI (Python/Terminal)
Best for training models or processing massive datasets.
- **[Ray](https://www.ray.io/):** The industry standard for scaling Python. Supports mixed-OS clusters (macOS ARM/Intel and Windows x86).
- **[Dask](https://www.dask.org/):** Ideal for "big data" analytics. It spreads memory load across the cluster so you can process files larger than any single machine's RAM.

### 🎨 3D Rendering & Creative (Blender/C4D)
Turn your machines into a "Render Farm."
- **[Crowdrender](https://www.crowdrender.com.au/):** A Blender plugin that connects Macs and PCs over a local network for distributed rendering.
- **[Deadline](https://www.awsthinkbox.com/deadline):** A professional-grade manager (free for small farms) that supports After Effects, Maya, and Cinema 4D.

### 💻 Development & Compilation
- **[Incredibuild](https://www.incredibuild.com/):** Distributes code compilation across your network to drastically reduce build times.

---

## 3. Essential Infrastructure ("The Glue")

| Component | Recommendation | Why? |
| :--- | :--- | :--- |
| **Networking** | **Ethernet (Wired)** | **Crucial.** 1Gbps or 10Gbps wired connections are required to prevent network bottlenecks. Wi-Fi is too slow for distributed RAM/IO tasks. |
| **VPN/VLAN** | **Tailscale** | Creates a secure "Virtual LAN" between your Macs and PCs automatically, handling cross-platform IP issues. |
| **File Sync** | **Syncthing** | Automatically syncs project files (textures, code, data) across all 7 machines without needing a central server. |
| **Shared Drive** | **SMB/NFS (NAS)** | For larger datasets, use a dedicated Network Attached Storage (NAS) so every computer reads from the same source. |

---

## 4. Key Technical Challenges

1.  **Architecture Mismatch:** Your Macs (likely Apple Silicon/ARM) and Windows PCs (x86) use different CPU instructions. Ensure your software (e.g., Python environment or Docker image) is compatible with both.
2.  **Latency:** Network "RAM" is ~1,000x slower than local RAM. Tasks must be large enough that the calculation time outweighs the data transfer time.
3.  **Wake-on-LAN:** Configure your Windows desktops and Macs to "Wake on LAN" so you can trigger them remotely when a job starts.
4.  **Static IPs:** Assign a fixed IP to each machine in your router settings so they don't "disappear" after a reboot.

---

## 5. Quick Start Checklist
1. [ ] Connect all machines via Ethernet to the same switch/router.
2. [ ] Install **Tailscale** on all 7 machines for easy discovery.
3. [ ] Choose a framework (Ray for AI, Crowdrender for Blender).
4. [ ] Test with a small "Hello World" distributed task.
