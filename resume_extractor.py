import os
import pdfplumber
import re
import logging
import spacy
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# spaCy NLP model for English
nlp = spacy.load("en_core_web_sm")

# to extract text from a single PDF file
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        logging.error(f"Error extracting text from {pdf_path}: {e}")
    return text.strip()

# to extract specific sections based on keywords
def extract_section(text, keywords):
    """Returns the first line that contains one of the keywords."""
    for keyword in keywords:
        pattern = re.compile(rf"{keyword}[:\s]*(.*)", re.IGNORECASE)
        match = pattern.search(text)
        if match:
            return match.group(1).strip()
    return None

# to extract Full Name from text

def extract_name(text):
    """
    Extracts a person's name from text.

    1. If a line starts with "Name:" (case-insensitive), it extracts the text following it.
    2. Otherwise, it checks the first non-empty line. If it is short (<=3 words) and appears to be a name, it returns that.
    3. As a fallback, it returns the first occurrence of one or more capitalized words.
    """
    # Case 1: Look for a line starting with "Name:" 
    match = re.search(r"(?im)^name\s*:\s*(.+)$", text)
    if match:
        name = match.group(1).strip()
        name = re.sub(r"[^\w\s]", "", name)  # remove any punctuation
        return name

    # Case 2: Check the first non-empty line
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    if lines:
        first_line = lines[0]
        # Heuristic: if the line is short (<= 5 words) and contains capitalized words, consider it the name.
        words = first_line.split()
        if len(words) <= 3 and any(word[0].isupper() for word in words):
            return first_line

    # Case 3: Fallback to regex that finds one or more capitalized words
    fallback = re.search(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b", text)
    if fallback:
        return fallback.group(1)
    
    return None

# Function to extract email
def extract_email(text):
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group(0) if match else None

# Function to extract phone number
def extract_phone(text):
    match = re.search(r"\+?\d[\d\s\-\(\)]{8,}\d", text)
    return match.group(0) if match else None

# Function to extract LinkedIn URL
def extract_linkedin(text):
    match = re.search(r"(https?://)?(www\.)?linkedin\.com/in/[a-zA-Z0-9-_/]+", text)
    return match.group(0) if match else None

# Function to extract education, experience, skills, and project details
def extract_fields_from_text(text, file_name):
    return {
        "File Name": file_name,
        "Full Name": extract_name(text),
        "Email": extract_email(text),
        "Phone": extract_phone(text),
        "LinkedIn": extract_linkedin(text),
        "Education": extract_section(text, ["Education", "Qualification", "Degree", "B.Sc", "M.Sc", "B.Tech", "M.Tech", "PhD", "Diploma"]),
        "Experience": extract_section(text, ["Experience", "Work History", "Employment", "Internship"]),
        "Skills": extract_section(text, ["Skills", "Technical Skills", "Programming Languages", "Tools"]),
        "Project": extract_section(text, ["Projects", "Portfolio", "Work Done"])
    }

# Main function to process a resume
def process_resume(file_path):
    text = extract_text_from_pdf(file_path)
    if not text:
        logging.error("No text extracted from file.")
        return None
    extracted_data = extract_fields_from_text(text, os.path.basename(file_path))
    logging.info(f"Extracted data: {extracted_data}")
    return extracted_data

# Function to save extracted data to an Excel file
def save_to_excel(data):
    EXCEL_FILE = "resume_data.xlsx"
    df = pd.DataFrame([data])  # Convert dictionary to DataFrame

    try:
        if os.path.exists(EXCEL_FILE):
            existing_df = pd.read_excel(EXCEL_FILE)
            df = pd.concat([existing_df, df], ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)
        logging.info(f"Saved extracted data to {EXCEL_FILE}")
    except Exception as e:
        logging.error(f"Error writing to {EXCEL_FILE}: {e}")

if __name__ == "__main__":
    test_file = os.path.join("uploads", "sample_resume.pdf")
    if os.path.exists(test_file):
        data = process_resume(test_file)
        if data:
            save_to_excel(data)
            print("Extraction & Saving Complete!")
    else:
        print("Test PDF not found in 'uploads/' folder.")
