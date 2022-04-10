import streamlit as st
from PyPDF2 import PdfFileMerger


def get_ordered_files(files):
    """Orders a list of pdf files by name"""
    sorted_files = sorted(
        list(zip(files, [f.name for f in files])),
        key=lambda x: x[1]
    )
    return [f[0] for f in sorted_files]


def show_files_being_merged(sorted_files):
    """A simp[le function to list the files being merged (in order)"""
    st.write("Files being merged:")
    filenames = [f.name for f in sorted_files]  # List of filenames
    # Print each to the screen
    for f in filenames:
        st.write(f)


def merge_pdfs(all_uploaded_files):
    """Takes many individual pdfs and merges them into one big one"""
    # Add the files into one big pdf, keeping count
    result = PdfFileMerger()
    for f in all_uploaded_files:
        result.append(f)
    return result


def load_pdf_for_download(name):
    """This is the final pdf that will be downloaded"""
    with open(name, "rb") as f:
        return f.read()


st.markdown("# PDF Merger")
files_uploaded = st.file_uploader(
    label='Choose files to merge together',
    type=['pdf'],
    accept_multiple_files=True
)

ordered_files = get_ordered_files(files=files_uploaded)
show_files_being_merged(sorted_files=ordered_files)


final_pdf = merge_pdfs(ordered_files)
if len(files_uploaded) > 0:
    filename = st.text_input(label='Enter the name of your new PDF (please do not add the .pdf part)')
    if filename:
        filename = f'{filename}.pdf'

        # Save file so that we can reload it and access the streamlit download button method
        final_pdf.write(filename)

        # Download the file
        st.download_button(label=f"Download '{filename}'",
                           data=load_pdf_for_download(filename),
                           file_name=f'{filename}',
                           mime='application/octet-stream')
