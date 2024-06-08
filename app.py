import streamlit as st
from deliverMail import read_email_details, write_email_details, send_email

# Read initial email details
to_emails, bcc_emails, subject, body = read_email_details()

# Streamlit UI
st.title("Email Editor and Sender")

to_emails = st.text_input("To:", ', '.join(to_emails))
bcc_emails = st.text_input("Bcc:", ', '.join(bcc_emails))
subject = st.text_input("Subject:", subject)
body = st.text_area("Body:", body)

uploaded_files = st.file_uploader("Choose files to attach", accept_multiple_files=True)

if st.button("Save and Send Email"):
    # Update the email details file
    write_email_details(to_emails.split(', '), bcc_emails.split(', '), subject, body)

    # Send email
    result = send_email(uploaded_files)

    if "successfully" in result:
        st.success(result)
    else:
        st.error(result)