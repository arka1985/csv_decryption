import streamlit as st
import pandas as pd
from cryptography.fernet import Fernet

# Streamlit app title and description
st.title("CSV File Decryption App")
st.write("This app allows you to upload an encrypted CSV file and a Fernet key for decryption.")

# Function to decrypt the data using the provided Fernet key
def decrypt_data(encrypted_data, key):
    f = Fernet(key)
    return f.decrypt(encrypted_data.encode()).decode()

# File upload section
st.subheader("Upload the Encrypted CSV File")
encrypted_csv_file = st.file_uploader("Choose an encrypted CSV file", type=["csv"])

st.subheader("Upload the Fernet Key")
fernet_key_file = st.file_uploader("Choose the Fernet key file", type=["key"])

if encrypted_csv_file and fernet_key_file:
    # Read the Fernet key
    key = fernet_key_file.read()

    # Create a Fernet cipher with the key
    cipher = Fernet(key)

    # Read the encrypted CSV file
    df = pd.read_csv(encrypted_csv_file)

    # Define the columns to decrypt
    columns_to_decrypt = ["age", "weight", "height"]

    # Decrypt the specified columns
    st.subheader("Decrypted Data")
    decrypted_df = df.copy()  # Create a copy of the DataFrame for decryption
    for col in columns_to_decrypt:
        decrypted_df[col] = decrypted_df[col].apply(lambda x: decrypt_data(x, key))

# Decrypt the specified columns
    #for col in columns_to_decrypt:
        #df[col] = df[col].apply(lambda x: cipher.decrypt(x.encode()).decode())

    # Display the decrypted data
    st.write(decrypted_df)
    if st.button("Save Decrypted Data"):
        with open("decrypted_patient_data.csv", "w") as file:
            decrypted_df.to_csv(file, index=False)
            st.success("Decrypted data has been saved as decrypted_patient_data.csv")

    #if st.button("Save Decrypted Data to CSV"):
        #decrypted_df.to_csv("decrypted_patient_data.csv", index=False)
        #st.success("Decrypted data has been saved to 'decrypted_patient_data.csv'.")
else:
    st.warning("Please upload the encrypted CSV file and the Fernet key.")

# Footer text
st.text("Developed by Dr. Arkaprabha Sau")

