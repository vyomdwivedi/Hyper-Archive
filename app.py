import os
import time
import shutil
import py7zr  #pip install py7zr
import streamlit as st  #pip install streamlit
import auth  #Importing the auth.py file



def compressor(ff_Path, ff_name):
    start_time = time.time()

    new_file_name = f"{ff_name}.rar"

    with py7zr.SevenZipFile(new_file_name, 'w') as archive:
        for root, dirs, files in os.walk(ff_Path):
            for file in files:
                archive.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), ff_Path))


    folder_name = f"{ff_name}(1)"
    file_name = new_file_name

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    src = file_name
    dst = os.path.join(folder_name, file_name)

    os.rename(src, dst)

    file_name = dst

    with py7zr.SevenZipFile(f"{ff_name}1.rar", 'w') as archive:
        archive.writeall(file_name)

    if os.path.exists(folder_name):
        shutil.rmtree(folder_name)

    new_file_name = f"{ff_name}1.rar"

    folder_name = f"{ff_name}(2)"
    file_name = new_file_name

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    src = file_name
    dst = os.path.join(folder_name, file_name)

    os.rename(src, dst)

    file_name = dst

    with py7zr.SevenZipFile(f"{ff_name}.rar", 'w') as archive:
        archive.writeall(file_name)

    if os.path.exists(folder_name):
        shutil.rmtree(folder_name)

    end_time = time.time()
    st.write(f'Time taken: {end_time - start_time} seconds')
    st.write("Compression complete.")



def decompressor(rar_path, extract_name):
    start_time = time.time()
    fn_without_extension = extract_name[:-len(".rar")]

    if rar_path.endswith(extract_name):
        dir = rar_path[:-len(extract_name)]
    else:
        dir = rar_path

    try:
        with py7zr.SevenZipFile(rar_path, 'r') as archive:
            archive.extractall(dir)
    except Exception as e:
        st.error(f"Error extracting RAR file: {e}")
        return

    source_path = os.path.join(dir, f"{fn_without_extension}(2)", f"{fn_without_extension}1.rar")
    destination_path = dir

    try:
        shutil.move(source_path, destination_path)
        #st.write("File moved successfully.")
    except Exception as e:
        st.write("An error occurred:", e)

    foldertodel = os.path.join(dir, f"{fn_without_extension}(2)")

    try:
        shutil.rmtree(foldertodel)
        #st.write("Folder deleted successfully.")
    except Exception as e:
        st.write("An error occurred:", e)

    archivepath2 = os.path.join(dir, f"{fn_without_extension}1.rar")

    try:
        with py7zr.SevenZipFile(archivepath2, 'r') as archive:
            archive.extractall(dir)
    except Exception as e:
        st.write("An error occurred:", e)

    file_path = archivepath2

    try:
        os.remove(file_path)
        #st.write("File deleted successfully.")
    except Exception as e:
        st.write("An error occurred:", e)

    rar_path = os.path.join(dir, f"{fn_without_extension}(1)", extract_name)
    new_rar_name = f"{extract_name}(last)"
    destination_dir = dir

    try:
        new_rar_path = os.path.join(os.path.dirname(rar_path), new_rar_name)
        os.rename(rar_path, new_rar_path)
        #st.write("RAR file renamed successfully.")
        destination_path = os.path.join(destination_dir, new_rar_name)
        os.rename(new_rar_path, destination_path)
        #st.write("RAR file moved successfully.")
    except Exception as e:
        st.write("An error occurred:", e)

    folder_path = os.path.join(dir, fn_without_extension)

    try:
        os.makedirs(folder_path)
        #st.write("Folder created successfully.")
    except Exception as e:
        st.write("An error occurred:", e)

    try:
        with py7zr.SevenZipFile(destination_path, 'r') as archive:
            archive.extractall(folder_path)
    except Exception as e:
        st.write("An error occurred:", e)

    foldertodel = os.path.join(dir, f"{fn_without_extension}(1)")

    try:
        shutil.rmtree(foldertodel)
        #st.write("Folder deleted successfully.")
    except Exception as e:
        st.write("An error occurred:", e)

    file_path = os.path.join(dir, new_rar_name)

    try:
        os.remove(file_path)
        #st.write("File deleted successfully.")
    except Exception as e:
        st.write("An error occurred:", e)

    end_time = time.time()
    st.write(f'Time taken: {end_time - start_time} seconds')
    st.write("Extraction complete.")



def main():
    # st.title("Hyper Archive Tool")  # Already present in main.py

    st.subheader(f"Welcome {st.session_state.email}")

    function = st.selectbox("What do you want to do?", ("Compress", "Decompress"))

    if function == "Compress":
        ff_Path = st.text_input("Enter the folder path:")
        ff_name = st.text_input("Enter the name of the folder you want to convert:")

        if st.button("Compress"):
            if ff_Path and ff_name:
                compressor(ff_Path, ff_name)
                st.success("Compression complete.")
            else:
                st.error("Please enter the folder path and name.")
    elif function == "Decompress":
        rar_path = st.text_input("Enter the RAR path:")
        extract_name = st.text_input("Enter the RAR name:")

        if st.button("Decompress"):
            if rar_path and extract_name:
                decompressor(rar_path, extract_name)
                st.success("Extraction complete.")
            else:
                st.error("Please enter the RAR path and name.")

if __name__ == "__main__":
    main()
