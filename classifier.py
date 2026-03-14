from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np

# Training data — zyada examples = better accuracy
training_data = [
    # Invoice / Finance
    ("invoice total amount payment due bill receipt", "finance"),
    ("total bill payment receipt amount due date tax", "finance"),
    ("invoice number date amount payable gst tax", "finance"),
    ("salary payslip deduction gross net amount", "finance"),
    ("bank statement transaction credit debit balance", "finance"),

    # Legal
    ("agreement contract terms conditions party signed", "legal"),
    ("hereby agreement signed parties contract law legal", "legal"),
    ("legal document terms obligations rights clause", "legal"),
    ("affidavit notary sworn statement legal court", "legal"),
    ("patent trademark copyright intellectual property", "legal"),

    # Medical
    ("patient diagnosis treatment prescription doctor", "medical"),
    ("medical report blood pressure symptoms medicine", "medical"),
    ("doctor prescription dosage patient health clinic", "medical"),
    ("hospital discharge summary diagnosis treatment", "medical"),
    ("lab report test results glucose hemoglobin", "medical"),

    # Technology
    ("technology network system software hardware", "technology"),
    ("internet protocol wireless network generation", "technology"),
    ("5g 4g lte network technology wireless spectrum", "technology"),
    ("computer algorithm data processing software", "technology"),
    ("server database api request response system", "technology"),
    ("mobile network bandwidth frequency modulation", "technology"),
    ("access scheme architecture evolution generation", "technology"),

    # Education
    ("student exam marks grade university college", "education"),
    ("syllabus course lecture assignment semester", "education"),
    ("result marksheet certificate degree diploma", "education"),

    # Image
    ("image width height mode pixels RGB JPEG PNG", "image"),
    ("image width height mode RGB resolution", "image"),
    ("image width height mode JPEG bitmap", "image"),

    # General
    ("document file general information data report", "general"),
    ("report summary information general document", "general"),
]

# Data alag karo
texts = [item[0] for item in training_data]
labels = [item[1] for item in training_data]

# Model banao aur train karo
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

model = MultinomialNB()
model.fit(X, labels)

def classify_document(text):
    """Document ka text lo aur category batao"""
    if not text or len(text.strip()) == 0:
        return "general"
    
    # Pehle 500 characters use karo
    text_sample = text[:500].lower()
    
    X_new = vectorizer.transform([text_sample])
    prediction = model.predict(X_new)
    confidence = model.predict_proba(X_new).max()
    
    print(f" Confidence: {confidence:.2%}")
    
    return prediction[0]