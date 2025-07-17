import socket
import random
import streamlit as st

st.title(zais tools")

ip = st.text_input("Target IP")
port = st.number_input("Target Port", min_value=1, max_value=65535, value=12345)
num_packets = st.number_input("Number of Packets", min_value=1, value=5)

if st.button("Send Packets"):
    if not ip:
        st.error("Please enter a target IP")
    else:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            for _ in range(num_packets):
                data = random._urandom(1024)
                sock.sendto(data, (ip, port))
            st.success(f"Sent {num_packets} UDP packets to {ip}:{port}")
        except Exception as e:
            st.error(f"Failed to send packets: {e}")
        finally:
            sock.close()
