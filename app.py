import re
import streamlit as st

st.set_page_config(page_title="ScamSathi AI", page_icon="🛡️", layout="centered")

RISK_TERMS = {
    "Urgency or pressure": ["urgent", "immediately", "within 24 hours", "account blocked", "suspended", "last warning", "act now"],
    "OTP or credentials": ["otp", "one time password", "password", "pin", "upi pin", "cvv", "verify your account"],
    "Banking or money": ["bank account", "kyc", "upi", "refund", "payment", "transfer money", "debit", "credit card"],
    "Prize or reward": ["you won", "winner", "prize", "lottery", "free gift", "claim reward"],
    "Links or contact requests": ["click here", "bit.ly", "tinyurl", "http://", "https://", "call this number"],
}

def check_message(message):
    msg = (message or "").strip().lower()
    if not msg:
        return None, [], "Please paste a message first."
    found_categories = []
    score = 0
    for category, terms in RISK_TERMS.items():
        matches = [term for term in terms if term in msg]
        if matches:
            found_categories.append((category, matches))
            score += min(len(matches), 2)
    if score >= 4:
        risk = "HIGH RISK — several warning signs detected"
    elif score >= 2:
        risk = "MEDIUM RISK — verify independently"
    elif score >= 1:
        risk = "CAUTION — inspect carefully"
    else:
        risk = "NO OBVIOUS KEYWORDS — this does NOT prove safety"
    advice = (
        "Do not click links or call numbers included in a suspicious message. "
        "Open the official app or website yourself, or contact the organisation using a trusted number. "
        "Never share your OTP, UPI PIN, password, or CVV."
    )
    return risk, found_categories, advice

st.title("🛡️ ScamSathi AI")
st.subheader("A simple message safety checker")
st.write("Paste an SMS, WhatsApp message, or payment alert to check for common scam warning signs.")

message = st.text_area("Suspicious message", placeholder="Paste the message here…", height=150)

if st.button("🔍 Check for Scam", type="primary", use_container_width=True):
    risk, categories, advice = check_message(message)
    if risk is None:
        st.warning(advice)
    else:
        if risk.startswith("HIGH"):
            st.error(risk)
        elif risk.startswith("MEDIUM"):
            st.warning(risk)
        else:
            st.info(risk)
        st.markdown("### Warning signs detected")
        if categories:
            for category, matches in categories:
                st.write(f"**{category}:** {', '.join(matches)}")
        else:
            st.write("No listed warning keywords were detected. Scams may use different wording.")
        st.markdown("### Safety advice")
        st.write(advice)

st.divider()
st.markdown(
    "**Important:** This is a keyword-based prototype, not a trained AI model or a guarantee that a message is safe. "
    "It may miss scams or flag legitimate messages. Do not enter real OTPs, passwords, UPI PINs, CVVs, or other private data."
)
st.markdown("**In India:** If you lose money to cyber financial fraud, call **1930** promptly or report at [cybercrime.gov.in](https://cybercrime.gov.in/).")
