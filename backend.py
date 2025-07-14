import subprocess
import shutil
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Scan options mapping to nmap commands and required inputs
SCAN_OPTIONS = {
    "1": {"name": "Ping Scan", "cmd": ["nmap", "-sn"], "inputs": ["target"]},
    "2": {"name": "TCP SYN Scan", "cmd": ["nmap", "-sS"], "inputs": ["target"]},
    "3": {"name": "UDP Scan", "cmd": ["nmap", "-sU"], "inputs": ["target"]},
    "4": {"name": "OS Detection", "cmd": ["nmap", "-O"], "inputs": ["target"]},
    "5": {"name": "Version Detection", "cmd": ["nmap", "-sV"], "inputs": ["target"]},
    "6": {"name": "Aggressive Scan", "cmd": ["nmap", "-A"], "inputs": ["target"]},
    "7": {"name": "Fast Scan", "cmd": ["nmap", "-F"], "inputs": ["target"]},
    "8": {"name": "All Ports Scan", "cmd": ["nmap", "-p-"], "inputs": ["target"]},
    "9": {"name": "Top Ports Scan", "cmd": ["nmap", "--top-ports", "100"], "inputs": ["target"]},
    "10": {"name": "Firewall Evasion", "cmd": ["nmap", "-f", "--data-length", "200"], "inputs": ["target"]},
    "11": {"name": "Vulnerability Scan", "cmd": ["nmap", "--script", "vuln"], "inputs": ["target"]},
    "12": {"name": "NSE Script Scan", "cmd": ["nmap", "--script", "default,vuln"], "inputs": ["target"]},
    "13": {"name": "Decoy Scan", "cmd": ["nmap", "-D"], "inputs": ["target", "decoy"]},
    "14": {"name": "Traceroute", "cmd": ["nmap", "--traceroute"], "inputs": ["target"]},
    "15": {"name": "Custom Ports", "cmd": ["nmap", "-p"], "inputs": ["target", "ports"]},
    "16": {"name": "Output to File", "cmd": ["nmap", "-A", "-oA"], "inputs": ["target", "filename"]},
    "17": {"name": "Spoof MAC", "cmd": ["nmap", "--spoof-mac"], "inputs": ["target", "mac"]},
    "18": {"name": "DNS Brute Force", "cmd": ["nmap", "--script", "dns-brute"], "inputs": ["target"]},
    "19": {"name": "HTTP Title Enumeration", "cmd": ["nmap", "--script", "http-title"], "inputs": ["target"]},
    "20": {"name": "SMB Enumeration", "cmd": ["nmap", "--script", "smb-enum-shares,smb-enum-users"], "inputs": ["target"]},
    "21": {"name": "FTP Anonymous Login Check", "cmd": ["nmap", "--script", "ftp-anon"], "inputs": ["target"]},
    "22": {"name": "SSL Certificate Info", "cmd": ["nmap", "--script", "ssl-cert"], "inputs": ["target"]},
    "23": {"name": "Detect Web Application Firewall", "cmd": ["nmap", "--script", "http-waf-detect"], "inputs": ["target"]},
    "24": {"name": "HTTP Methods Check", "cmd": ["nmap", "--script", "http-methods"], "inputs": ["target"]},
    "25": {"name": "Extract HTTP Robots.txt", "cmd": ["nmap", "--script", "http-robots.txt"], "inputs": ["target"]},
    "26": {"name": "Whois Lookup", "cmd": ["nmap", "--script", "whois"], "inputs": ["target"]},
    "27": {"name": "Run All Safe Scripts", "cmd": ["nmap", "--script", "safe"], "inputs": ["target"]},
}

def check_dependencies():
    missing = []
    for dep in ["nmap"]:
        if shutil.which(dep) is None:
            missing.append(dep)
    return missing

@app.route("/")
def index():
    return render_template("index.html", options=SCAN_OPTIONS)

@app.route("/scan", methods=["POST"])
def scan():
    data = request.json
    option = data.get("option")
    if option not in SCAN_OPTIONS:
        return jsonify({"error": "Invalid scan option"}), 400

    scan_info = SCAN_OPTIONS[option]
    cmd = scan_info["cmd"][:]
    inputs = scan_info["inputs"]

    # Build command with inputs
    try:
        if "target" in inputs:
            target = data.get("target")
            if not target:
                return jsonify({"error": "Target is required"}), 400
        if "decoy" in inputs:
            decoy = data.get("decoy")
            if not decoy:
                return jsonify({"error": "Decoy IP is required"}), 400
        if "ports" in inputs:
            ports = data.get("ports")
            if not ports:
                return jsonify({"error": "Ports are required"}), 400
        if "filename" in inputs:
            filename = data.get("filename")
            if not filename:
                return jsonify({"error": "Filename is required"}), 400
        if "mac" in inputs:
            mac = data.get("mac")
            if not mac:
                return jsonify({"error": "MAC type is required"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    # Append inputs to command
    if option == "13":  # Decoy scan
        cmd.append(decoy)
        cmd.append(target)
    elif option == "15":  # Custom ports
        cmd.append(ports)
        cmd.append(target)
    elif option == "16":  # Output to file
        cmd.append(filename)
        cmd.append(target)
    elif option == "17":  # Spoof MAC
        cmd.append(mac)
        cmd.append(target)
    else:
        if "target" in inputs:
            cmd.append(target)

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        output = result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Scan timed out"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"output": output})

if __name__ == "__main__":
    missing = check_dependencies()
    if missing:
        print(f"Missing dependencies: {', '.join(missing)}. Please install them and try again.")
        exit(1)
    app.run(host="0.0.0.0", port=5000, debug=True)
