import re


def extract_clauses(text, clause_headers):
    
    # Split text into sections using headers
    sections = re.split(r'(?i)(' + "|".join(clause_headers) + r')', text)
    sections = [s.strip() for s in sections if s.strip()]

    # Group headers with their content
    clauses = {}
    current_header = None
    for section in sections:
        if section.lower() in [h.lower() for h in clause_headers]:
            current_header = section
            clauses[current_header] = ""
        elif current_header:
            clauses[current_header] += section + "\n"

    # Clean up: Remove empty clauses
    clauses = {k: v for k, v in clauses.items() if v.strip()}
    return clauses
