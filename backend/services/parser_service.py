import fitz
import re



def extract_text_from_pdf(file):
    """
    Extracts text from every page of an uploaded PDF.
    """

    document = fitz.open(
        stream=file.read(),
        filetype="pdf"
    )

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text




SECTION_HEADERS = {
    "SUMMARY": "summary",
    "TECHNICAL SKILLS": "technical_skills",
    "SKILLS": "technical_skills",
    "EXPERIENCE": "experience",
    "WORK EXPERIENCE": "experience",
    "PROJECTS": "projects",
    "OPEN SOURCE": "open_source",
    "EDUCATION": "education",
    "CERTIFICATIONS": "certifications",
}




def extract_sections(text):
    """
    Separates raw resume text into sections such as
    skills, experience, projects, and education.
    """

    sections = {}

    current_section = None
    current_content = []

    for line in text.splitlines():

        # Remove unnecessary spaces
        line = line.strip()

        # Ignore empty lines
        if not line:
            continue

        upper_line = line.upper()

        
        if upper_line in SECTION_HEADERS:

            
            if current_section:
                sections[current_section] = "\n".join(
                    current_content
                ).strip()

            
            current_section = SECTION_HEADERS[upper_line]
            current_content = []

        
        elif current_section:
            current_content.append(line)

    
    if current_section:
        sections[current_section] = "\n".join(
            current_content
        ).strip()

    return sections


#calc

def calculate_word_count(text):
    """
    Calculates the total number of words in the resume.
    """

    words = text.split()

    return len(words)
def extract_contact_info(text):
    """
    Extracts basic contact information from resume text.
    """

    email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
    phone_pattern = r'(?:\+91[\s-]?)?[6-9]\d{9}'

    email_match = re.search(email_pattern, text)
    phone_match = re.search(phone_pattern, text)

    contact_info = {
        "email": email_match.group() if email_match else None,
        "phone": phone_match.group() if phone_match else None,
    }

    return contact_info
def parse_resume(file):
    """
    Parse a resume PDF and return all extracted information
    in one structured dictionary.
    """

    # Extract complete resume text
    raw_text = extract_text_from_pdf(file)

    # Extract resume sections
    sections = extract_sections(raw_text)

    # Calculate word count
    word_count = calculate_word_count(raw_text)

    # Extract email and phone
    contact_info = extract_contact_info(raw_text)

    return {
        "raw_text": raw_text,
        "sections": sections,
        "word_count": word_count,
        "contact_info": contact_info,
    }

#testing

if __name__ == "__main__":

    pdf_path = "data/test_resume.pdf"

    with open(pdf_path, "rb") as file:
        resume = parse_resume(file)

    print("\n" + "=" * 50)
    print("RESUME PARSER RESULT")
    print("=" * 50)

    print("\nWORD COUNT:")
    print(resume["word_count"])

    print("\nCONTACT INFO:")
    print(resume["contact_info"])

    print("\nSECTIONS FOUND:")
    print(list(resume["sections"].keys()))

    print("\n" + "=" * 50)
    print("SECTIONS")
    print("=" * 50)

    for section_name, content in resume["sections"].items():
        print(f"\n--- {section_name.upper()} ---")
        print(content)