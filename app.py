import time
import shutil
import py7zr
import streamlit as st
from io import BytesIO

def compressor(uploaded_file, ff_name):
    start_time = time.time()
    new_file_name = f"{ff_name}.rar"
    with py7zr.SevenZipFile(new_file_name, 'w') as archive:
        archive.write(uploaded_file, ff_name)
    end_time = time.time()
    st.write(f'Time taken: {end_time - start_time} seconds')
    st.write("Compression complete.")
    return new_file_name

def decompressor(uploaded_file, extract_name):
    start_time = time.time()
    fn_without_extension = extract_name[:-len(".rar")]
    dir = "/tmp"  # Temporary directory for extraction
    try:
        with py7zr.SevenZipFile(uploaded_file, 'r') as archive:
            archive.extractall(dir)
    except Exception as e:
        st.error(f"Error extracting RAR file: {e}")
        return None
    end_time = time.time()
    st.write(f'Time taken: {end_time - start_time} seconds')
    st.write("Extraction complete.")
    return dir

def main():
    # st.subheader(f"Welcome {st.session_state.email}")

    function = st.selectbox("What do you want to do?", ("Compress", "Decompress"))

    if function == "Compress":
        uploaded_file = st.file_uploader("Upload a file to compress", type=["txt", "csv", "json", "xlsx", "pdf", "png", "jpg", "jpeg"])
        ff_name = st.text_input("Enter the name of the file you want to convert:")

        if st.button("Compress"):
            if uploaded_file and ff_name:
                compressed_file_name = compressor(uploaded_file, ff_name)
                with open(compressed_file_name, "rb") as file:
                    st.download_button(label="Download Compressed File", data=file, file_name=compressed_file_name)
            else:
                st.error("Please upload a file and enter the file name.")
    elif function == "Decompress":
        uploaded_file = st.file_uploader("Upload a RAR file to decompress", type=["rar"])
        extract_name = st.text_input("Enter the RAR name:")

        if st.button("Decompress"):
            if uploaded_file and extract_name:
                extracted_dir = decompressor(uploaded_file, extract_name)
                if extracted_dir:
                    shutil.make_archive(extracted_dir, 'zip', extracted_dir)
                    with open(f"{extracted_dir}.zip", "rb") as file:
                        st.download_button(label="Download Extracted Files", data=file, file_name=f"{extract_name}.zip")
            else:
                st.error("Please upload a RAR file and enter the RAR name.")
if __name__ == "__main__":
    main()
