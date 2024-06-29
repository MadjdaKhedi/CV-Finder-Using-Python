# CV-Finder
(Python and Jupyter Notebook versions)

# The solution will consist of :
### Imports and Constants: The necessary modules are imported and the list of keywords to search for in CVs is defined.
### Functions :
- Extract_text_from_pdf: Extracts text from a PDF file.
- Extract_text_from_docx: Extracts text from a DOCX file.
- Process_cvs: Reads all CV files in the specified directory and extracts their text content.
- Create_keyword_index: Creates an index of keywords found in the CVs.
- Search_cvs: Searches for CVs containing a specific keyword using the index.

### Main Execution :
- The directory containing the CVs is specified.
- The CVs are processed and their content is indexed.
- The available keywords are printed for the user.
- A loop allows the user to search for CVs by entering the number corresponding to a keyword. The results are displayed, or the user is informed if no CVs contain the keyword. The loop continues until the user click on 'Exit'.
