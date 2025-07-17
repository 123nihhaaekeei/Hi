import socket
import os
import streamlit as st
import time

st.title("Zais Sigma Tools")

ip = st.text_input("Target IP")
port = st.number_input("Port", min_value=1, max_value=65535, value=12345)
num_packets = st.number_input("Number of Packets", min_value=1, value=5)

if st.button("Send Packets"):
    if not ip:
        st.error("Please enter a target IP")
    else:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            progress_bar = st.progress(0)
            for i in range(num_packets):
                data = os.urandom(1024)  # Better than random._urandom
                sock.sendto(data, (ip, port))
                progress_bar.progress((i + 1) / num_packets)
                time.sleep(0.01)  # Prevents blocking / freezing UI
            st.success(f"✅ Sent {num_packets} UDP packets to {ip}:{port}")
        except Exception as e:
            st.error(f"❌ Failed to send packets: {e}")
        finally:
            sock.close()
