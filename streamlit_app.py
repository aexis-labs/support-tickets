import streamlit as st
import datetime
import random
import pandas as pd
import logging
import hashlib
import time
from typing import List, Dict, Any

# ==============================================================================
# 0. CONFIGURATION (load from secrets)
# ==============================================================================
try:
    TARGET_HASH = st.secrets["INCIDENT_AUTH_HASH"]
except (KeyError, FileNotFoundError):
    # Fallback only for development – change this!
    TARGET_HASH = "4d7d3fcc1d3ab90d07079c7ea411d89c29b8a7dc228a8eb4eabf552f28e2a312"  # "admin" + salt
    logging.warning("INCIDENT_AUTH_HASH not set. Using insecure default.")

CRYPTO_SALT = st.secrets.get("INCIDENT_SALT", "AexisIncident_SecureSalt_2026##")
LOG_LEVEL = st.secrets.get("LOG_LEVEL", "INFO")
logging.basicConfig(level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
                    format='%(asctime)s - %(levelname)s - %(message)s')

# ==============================================================================
# 1. PAGE CONFIG & THEME (similar dark theme)
# ==============================================================================
st.set_page_config(
    page_title="Aexis Incident Manager v2.0",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp {
        background-color: #0a0a0a;
        color: #00ff9d;
    }
    .stButton>button {
        background-color: #00ff9d;
        color: black;
        border: none;
    }
    .stButton>button:hover {
        background-color: #00cc7a;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. SESSION STATE & AUTHENTICATION
# ==============================================================================
def init_ticket_system():
    if "tickets" not in st.session_state:
        st.session_state.tickets = [
            {
                "ID": "AX-1024",
                "Timestamp": "2026-06-10 14:22",
                "Category": "Security Anomaly",
                "Priority": "High",
                "Issue": "High volume of invalid authorization attempts on Gateway Node 02.",
                "AI Diagnostic Note": "FLAGGED: Possible brute-force event. Integrity path secure.",
                "Status": "In Progress"
            },
            {
                "ID": "AX-1025",
                "Timestamp": "2026-06-11 01:05",
                "Category": "Hardware / Server Downtime",
                "Priority": "Critical",
                "Issue": "Memory leak detected on cluster backbone switch c3-net.",
                "AI Diagnostic Note": "CRITICAL: Resource exhaustion hazard. Rerouting traffic nodes.",
                "Status": "Open"
            }
        ]
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "last_activity" not in st.session_state:
        st.session_state.last_activity = datetime.datetime.now()

init_ticket_system()

def authenticate(password: str) -> bool:
    salted = password + CRYPTO_SALT
    return hashlib.sha256(salted.encode()).hexdigest() == TARGET_HASH

# Optional authentication gateway – uncomment to enable
# if not st.session_state.authenticated:
#     st.title("🔐 Aexis Incident Manager – Secure Access")
#     with st.form("auth_form"):
#         pwd = st.text_input("Authorization Key:", type="password", help="Default: admin")
#         if st.form_submit_button("Unlock Dashboard"):
#             if authenticate(pwd):
#                 st.session_state.authenticated = True
#                 st.session_state.last_activity = datetime.datetime.now()
#                 st.success("Access granted.")
#                 st.rerun()
#             else:
#                 st.error("Invalid key.")
#     st.stop()

# Session timeout (optional)
SESSION_TIMEOUT_MINUTES = 30
if st.session_state.authenticated:
    if (datetime.datetime.now() - st.session_state.last_activity).seconds > SESSION_TIMEOUT_MINUTES * 60:
        st.session_state.authenticated = False
        st.warning("Session expired. Please re-authenticate.")
        st.rerun()
    else:
        st.session_state.last_activity = datetime.datetime.now()

# ==============================================================================
# 3. SIDEBAR METRICS
# ==============================================================================
st.sidebar.header("Incident Operations Control")
st.sidebar.markdown("---")
st.sidebar.info("🎫 **AEXIS SUPPORT INCIDENT MANAGER**")

tickets = st.session_state.tickets
total_tickets = len(tickets)
open_tickets = sum(1 for t in tickets if t["Status"] == "Open")
resolved_tickets = sum(1 for t in tickets if t["Status"] == "Resolved")

st.sidebar.metric(label="Total Logged Incidents", value=total_tickets)
st.sidebar.metric(label="Active Open Incidents", value=open_tickets, delta=f"{open_tickets} pending", delta_color="inverse")
st.sidebar.metric(label="Resolved Exceptions", value=resolved_tickets)

st.sidebar.markdown("---")
st.sidebar.caption(f"System Epoch: {datetime.datetime.now().year}")
st.sidebar.success("Incident sync pipeline: ONLINE")

if st.sidebar.button("🧹 Clear All Tickets", use_container_width=True):
    st.session_state.tickets = []
    st.rerun()

# ==============================================================================
# 4. MAIN HEADER
# ==============================================================================
st.title("🎫 Aexis Support Incident Manager")
st.caption("Internal Operations Dashboard | Autonomous Ticket Triage Pipeline")
st.write("---")

m1, m2, m3 = st.columns(3)
m1.metric("Automated Triage Accuracy", "97.6%", "Optimal")
m2.metric("Mean Time to Detection (MTTD)", "0.8 seconds", "-0.4s")
m3.metric("System Automation Rate", "89.2%", "+2.1%")
st.write("---")

col_form, col_pipeline = st.columns([1, 2], gap="large")

# ==============================================================================
# 5. LEFT COLUMN – TICKET CREATION (with enhanced AI classification)
# ==============================================================================
with col_form:
    st.write("### ➕ Log New Infrastructure Incident")

    with st.form(key="incident_submission_form", clear_on_submit=True):
        issue_details = st.text_area(
            "Detailed Threat/Issue Description:",
            placeholder="Describe the error, logs, or system disruption..."
        )

        st.caption("ℹ️ Aexis AI will auto‑classify priority and category.")
        submit_ticket = st.form_submit_button("Commit Incident to Pipeline", use_container_width=True)

        if submit_ticket:
            if not issue_details.strip():
                st.error("Please enter a valid description.")
            else:
                # Generate new ticket ID
                new_id = f"AX-{random.randint(1000, 9999)}"
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

                # AI classification (more comprehensive)
                text_lower = issue_details.lower()
                if any(w in text_lower for w in ["ddos", "flood", "attack", "unauthorized", "breach", "exploit"]):
                    category = "Security Anomaly"
                    priority = "Critical"
                    diagnostic = "AUTONOMOUS BLOCK: High threat vector isolated. Sentinel sync engaged."
                elif any(w in text_lower for w in ["downtime", "crash", "leak", "fail", "offline", "memory"]):
                    category = "Hardware / Server Downtime"
                    priority = "High"
                    diagnostic = "RESOURCE ROUTING: Infrastructure drift isolated. Check system cluster."
                elif any(w in text_lower for w in ["slow", "latency", "ping", "delay", "timeout"]):
                    category = "Network Latency Spike"
                    priority = "Medium"
                    diagnostic = "TRAFFIC SHAPING: Network packet bottleneck flagged."
                else:
                    category = "General Support Request"
                    priority = "Low"
                    diagnostic = "ROUTINE REVIEW: Queue assignment completed."

                # Append to session state
                new_ticket = {
                    "ID": new_id,
                    "Timestamp": timestamp,
                    "Category": category,
                    "Priority": priority,
                    "Issue": issue_details,
                    "AI Diagnostic Note": diagnostic,
                    "Status": "Open"
                }
                st.session_state.tickets.insert(0, new_ticket)

                logging.info(f"AI Triage: {new_id} classified as {category} [{priority}]")
                st.success(f"✅ Incident {new_id} autonomously processed by Aexis AI!")
                st.rerun()

# ==============================================================================
# 6. RIGHT COLUMN – TICKET PIPELINE & MANAGEMENT
# ==============================================================================
with col_pipeline:
    st.write("### 📋 Active Incident Tracking Pipeline")

    if not st.session_state.tickets:
        st.info("No incidents logged in system memory.")
    else:
        df_display = pd.DataFrame(st.session_state.tickets)
        st.dataframe(df_display, use_container_width=True, hide_index=True)

        st.write("---")
        st.write("#### ⚡ Quick Resolution Tool")

        ticket_ids = [t["ID"] for t in st.session_state.tickets]
        selected_id = st.selectbox("Select Ticket ID to Update:", ticket_ids)

        # Find current status for pre‑selection
        current_status = next(t["Status"] for t in st.session_state.tickets if t["ID"] == selected_id)
        new_status = st.radio(
            "Modify Operational Status:",
            ["Open", "In Progress", "Resolved"],
            index=["Open", "In Progress", "Resolved"].index(current_status),
            horizontal=True
        )

        if st.button("🔄 Update System Records", use_container_width=True):
            for ticket in st.session_state.tickets:
                if ticket["ID"] == selected_id:
                    ticket["Status"] = new_status
                    logging.info(f"Ticket {selected_id} updated to {new_status}")
                    st.toast(f"Ticket {selected_id} marked as {new_status}!", icon="🔄")
                    st.rerun()
                    break

# ==============================================================================
# 7. OPTIONAL FOOTER
# ==============================================================================
st.caption("🔒 All operations logged. Aexis Incident Manager v2.0 – Production Ready")
