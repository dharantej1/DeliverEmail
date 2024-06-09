import streamlit as st
from deliverMail import read_email_details, write_email_details, send_email

# Read initial email details
to_emails, cc_emails, bcc_emails, subject, body = read_email_details()

# Streamlit UI
st.title("Email Editor and Sender")

# To email input
to_emails_input = st.text_input("To:", ', '.join(to_emails))

# Cc email input
cc_emails_input = st.text_input("Cc:", ', '.join(cc_emails))

# Bcc email input
bcc_emails_input = st.text_input("Bcc:", ', '.join(bcc_emails))

subject = st.text_input("Subject:", subject)
body = st.text_area("Body:", body)

uploaded_files = st.file_uploader("Choose files to attach", accept_multiple_files=True)

if st.button("Save and Send Email"):
    # Update the email details file
    write_email_details(to_emails_input.split(', '), cc_emails_input.split(', '), bcc_emails_input.split(', '), subject,
                        body)

    # Send email
    result = send_email(uploaded_files)

    if "successfully" in result:
        st.success(result)
    else:
        st.error(result)