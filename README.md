# 🔍 Elite Nmap Scanner

**Elite Nmap Scanner** is a professional-grade Flask-based web application that provides an intuitive and powerful interface to run a wide variety of **Nmap scans**. Designed for cybersecurity researchers, students, and network admins, it combines an elegant frontend with a robust Python backend to deliver fast, detailed scan results.

---

## 🚀 Features

- 🧠 Smart scan type selection from 27 advanced Nmap techniques.
- ⚙️ Backend execution via secure `subprocess` handling.
- 📡 Real-time asynchronous output with AJAX.
- 🛡️ Terminal-like styled result display.
- 📘 Sidebar tips for network security awareness.
- ✅ Automatic check for Nmap installation.

## 🏗️ Tech Stack

| Layer      | Technology             |
|------------|------------------------|
| Frontend   | HTML5, CSS3, JavaScript |
| Backend    | Python, Flask          |
| Scanner    | Nmap (via subprocess)  |

---

## 🛠️ Supported Scan Types (27)

The application supports the following **27 Nmap scan types**, defined in the `SCAN_OPTIONS` dictionary of `backend.py`:

1. 🔍 Ping Scan  
2. 🔓 TCP SYN Scan  
3. 🌊 UDP Scan  
4. 🧠 OS Detection  
5. 🔢 Version Detection  
6. ⚔️ Aggressive Scan  
7. ⚡ Fast Scan  
8. 🌐 All Ports Scan  
9. 📊 Top Ports Scan  
10. 🔥 Firewall Evasion  
11. 🚨 Vulnerability Scan  
12. 🧪 NSE Script Scan  
13. 👻 Decoy Scan  
14. 🧭 Traceroute  
15. 🎯 Custom Ports  
16. 📁 Output to File  
17. 🕵️ Spoof MAC  
18. 🌎 DNS Brute Force  
19. 🏷️ HTTP Title Enumeration  
20. 🖥️ SMB Enumeration  
21. 📂 FTP Anonymous Login Check  
22. 🔐 SSL Certificate Info  
23. 🛡️ Detect Web Application Firewall  
24. 🚪 HTTP Methods Check  
25. 🤖 Extract HTTP Robots.txt  
26. 🧾 Whois Lookup  
27. 🧼 Run All Safe Scripts  

Each scan type is automatically mapped to its corresponding Nmap command with required parameters.

---

## ⚙️ Installation

> **Prerequisites**:  
> - Python 3.7+  
> - Nmap (installed and added to your system’s PATH)

```bash
# Clone the repository
git clone https://github.com/your-username/elite-nmap-scanner.git
cd elite-nmap-scanner

# Create and activate virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
