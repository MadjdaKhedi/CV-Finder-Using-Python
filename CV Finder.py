#!/usr/bin/env python
# coding: utf-8

# # The solution will consist of :
# 
# ### Imports and Constants: The necessary modules are imported and the list of keywords to search for in CVs is defined.
# ### Functions :
# - Extract_text_from_pdf: Extracts text from a PDF file.
# - Extract_text_from_docx: Extracts text from a DOCX file.
# - Process_cvs: Reads all CV files in the specified directory and extracts their text content.
# - Create_keyword_index: Creates an index of keywords found in the CVs.
# - Search_cvs: Searches for CVs containing a specific keyword using the index.
# 
# ### Main Execution :
# - The directory containing the CVs is specified.
# - The CVs are processed and their content is indexed.
# - The available keywords are printed for the user.
# - A loop allows the user to search for CVs by entering the number corresponding to a keyword. The results are displayed, or the user is informed if no CVs contain the keyword. The loop continues until the user click on 'quit'.

# # To run your Python script using the Command Prompt (CMD), follow these steps:
# - pip install notebook (only once)
# - cd (Add your path without using the ())
# - jupyter notebook
# - jupyter nbconvert --to script "CV Finder.ipynb"
# - python "CV Finder.py"

# In[1]:


import os
import re
import PyPDF2
import docx
from collections import defaultdict
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from threading import Thread


# In[2]:


# List of keywords to search for in CVs
KEYWORD_LIST = [
    "python", "java", "javascript", "c++", "sql",
    "machine learning", "data analysis", "web development",
    "project management", "agile", "scrum",
    "marketing", "sales", "customer service",
    "finance", "accounting", "human resources"
]


# In[3]:


# Function to extract text from a PDF file
def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

# Function to extract text from a DOCX file
def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return ' '.join([paragraph.text for paragraph in doc.paragraphs])

# Function to process all CV files in a directory
def process_cvs(directory, progress_callback):
    cv_content = {}
    files = [f for f in os.listdir(directory) if f.endswith('.pdf') or f.endswith('.docx')]
    total_files = len(files)
    
    for i, filename in enumerate(files):
        file_path = os.path.join(directory, filename)
        if filename.endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
        elif filename.endswith('.docx'):
            text = extract_text_from_docx(file_path)
        cv_content[filename] = text.lower()
        progress_callback((i + 1) / total_files * 100)
    return cv_content

# Function to create an index of keywords found in the CVs
def create_keyword_index(cv_content):
    keyword_index = defaultdict(list)
    for filename, content in cv_content.items():
        words = re.findall(r'\w+', content)
        for word in set(words):
            keyword_index[word].append(filename)
    return keyword_index

# Function to search for CVs containing a specific keyword
def search_cvs(keyword, keyword_index):
    return keyword_index.get(keyword.lower(), [])

# Function to handle the search button click
def search_button_click():
    keyword = keyword_var.get()
    if keyword:
        results = search_cvs(keyword, keyword_index)
        if results:
            result_text.set(f"CVs containing '{keyword}':\n" + '\n'.join(results))
        else:
            result_text.set(f"No CVs found containing '{keyword}'")
        result_frame.pack(pady=10, fill='both', expand=True)
    else:
        messagebox.showwarning("Input Error", "Please select a keyword.")

# Function to handle the directory selection
def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        progress_bar.pack(pady=10)
        progress_bar['value'] = 0
        status_label.pack(pady=5)
        status_text.set("Processing CVs...")
        result_frame.pack_forget()
        Thread(target=process_directory, args=(directory,)).start()

def process_directory(directory):
    global keyword_index
    cv_content = process_cvs(directory, update_progress)
    keyword_index = create_keyword_index(cv_content)
    status_text.set("CVs processed and indexed successfully.")
    messagebox.showinfo("Success", "CVs processed and indexed successfully.")

def update_progress(value):
    progress_bar['value'] = value

# Function to handle exit button click
def exit_application():
    root.quit()


# In[9]:


# Create the main window
root = tk.Tk()
root.title("CV Keyword Finder")
root.geometry("600x500")

# Configure style
style = ttk.Style()
style.configure('TLabel', foreground='black', background='#3a7bd5', font=('Helvetica', 12))
style.configure('TButton', foreground='black', background='#3a7bd5', font=('Helvetica', 12))
style.configure('TCombobox', foreground='black', background='white', font=('Helvetica', 12))
style.configure('TProgressbar', foreground='#3a7bd5', background='#3a7bd5')
style.map('TButton', background=[('active', '#2a5da8'), ('!disabled', '#3a7bd5')])

root.configure(background='#3a7bd5')

# Welcome message
welcome_label = ttk.Label(root, text="Welcome, Grace, to CV Keyword Finder", font=("Helvetica", 16))
welcome_label.pack(pady=10)

# Dropdown for keyword selection
keyword_var = tk.StringVar()
keyword_label = ttk.Label(root, text="Select a keyword")
keyword_label.pack(pady=5)
keyword_dropdown = ttk.Combobox(root, textvariable=keyword_var)
keyword_dropdown['values'] = KEYWORD_LIST
keyword_dropdown.pack(pady=5)

# Button to select directory
directory_button = ttk.Button(root, text="Select CV Directory", command=select_directory)
directory_button.pack(pady=10)

# Button to search CVs
search_button = ttk.Button(root, text="Search CVs", command=search_button_click)
search_button.pack(pady=10)

# Progress bar for processing CVs (initially hidden)
progress_bar = ttk.Progressbar(root, orient='horizontal', length=300, mode='determinate')

# Label to display status messages (initially hidden)
status_text = tk.StringVar()
status_label = ttk.Label(root, textvariable=status_text)

# Frame for displaying search results with a scrollbar (initially hidden)
result_frame = tk.Frame(root, background='#3a7bd5')
result_canvas = tk.Canvas(result_frame, background='#3a7bd5')
scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=result_canvas.yview)
scrollable_frame = tk.Frame(result_canvas, background='#3a7bd5')

scrollable_frame.bind(
    "<Configure>",
    lambda e: result_canvas.configure(
        scrollregion=result_canvas.bbox("all")
    )
)

result_canvas.create_window((0, 0), window=scrollable_frame, anchor="n")
result_canvas.configure(yscrollcommand=scrollbar.set)

result_canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Label to display search results
result_text = tk.StringVar()
result_label = tk.Label(scrollable_frame, textvariable=result_text, wraplength=500, justify="center", background='#3a7bd5', fg='black')
result_label.pack(pady=10, padx=680)

# Exit button
exit_button = ttk.Button(root, text="Exit", command=exit_application)
exit_button.pack(pady=10)

# Start the GUI event loop
root.mainloop()

