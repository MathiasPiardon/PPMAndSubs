import os
from ExtractTextFromContracts import extract_text_from_pdf
import spacy
from IdentifyClausesInEachContract import extract_clauses

# Extract text from all pdf files in the specified directory
contracts_dir = r"G:\My Drive\PPMAndSubs\PPMs"
contract_texts = {}
for filename in os.listdir(contracts_dir):
    if filename.endswith(".pdf"):
        path = os.path.join(contracts_dir, filename)
        contract_texts[filename] = extract_text_from_pdf(path)

# VERIF: show in terminal first 200 charachters of each contract. To verify that the text was extracted correctly
"""
for filename, text in contract_texts.items():
    print(f"\n--- First 200 characters of {filename} ---")
    print(text[:200])  # Print the first 200 characters
"""

# VERIF: Print the full text of the first contract (for example)
"""sample_filename = list(contract_texts.keys())[0]
print(f"--- Full text of {sample_filename} ---")
print(contract_texts[sample_filename][:2000])  # Print the first 2000 characters
"""

# load spaCy model to identify sentences or paragraphs that likely contain clauses
nlp = spacy.load("en_core_web_lg")

# Common clause headers
clause_headers = [
    "fund","management", "risk factors","valuation", "brokerage practices", "conflicts of interest", "tax considerations",
    "prime broker", "custodian", "auditor", "legal counsel", "investment strategy", "investment restrictions",
    "confidentiality", "termination", "representations and warranties",
    "covenants", "events of default", "governing law", "fees",
    "lock-up period", "indemnification", "use of proceeds",
]

# Extract clauses from the extracted text
contract_clauses = {}
for filename, text in contract_texts.items():
    contract_clauses[filename] = extract_clauses(text,clause_headers)

#VERIF: Print clauses for the first contract
sample_filename = list(contract_clauses.keys())[0]
print(f"\n--- Clauses extracted from {sample_filename} ---")
for header, clause_text in contract_clauses[sample_filename].items():
    print(f"\n**{header}**")
    print(clause_text[:200] + "...")  # Print the first 200 characters of each clause
