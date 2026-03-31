
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import numpy as np

training_data = [
    # Finance
    ("invoice total amount payment due bill receipt gst tax", "finance"),
    ("total bill payment receipt amount due date tax", "finance"),
    ("invoice number date amount payable gst tax", "finance"),
    ("salary payslip deduction gross net amount ctc", "finance"),
    ("bank statement transaction credit debit balance account", "finance"),
    ("profit loss revenue expense budget quarterly annual", "finance"),
    ("tax return filing income deduction refund assessment", "finance"),
    ("loan emi interest rate principal repayment bank", "finance"),
    ("balance sheet assets liabilities equity shareholder", "finance"),
    ("purchase order vendor payment terms discount", "finance"),

    # Legal
    ("agreement contract terms conditions party signed", "legal"),
    ("hereby agreement signed parties contract law legal", "legal"),
    ("legal document terms obligations rights clause", "legal"),
    ("affidavit notary sworn statement legal court", "legal"),
    ("patent trademark copyright intellectual property", "legal"),
    ("memorandum understanding mou parties binding", "legal"),
    ("nda non disclosure confidential agreement", "legal"),
    ("court order judgment plaintiff defendant case", "legal"),
    ("power attorney authorize legal representative", "legal"),
    ("terms conditions privacy policy user agreement", "legal"),

    # Medical
    ("patient diagnosis treatment prescription doctor", "medical"),
    ("medical report blood pressure symptoms medicine", "medical"),
    ("doctor prescription dosage patient health clinic", "medical"),
    ("hospital discharge summary diagnosis treatment", "medical"),
    ("lab report test results glucose hemoglobin", "medical"),
    ("xray mri scan radiology report findings", "medical"),
    ("surgery operation procedure anesthesia recovery", "medical"),
    ("vaccine immunization dose schedule health", "medical"),
    ("clinical trial study participants drug efficacy", "medical"),
    ("ecg heart rate pulse oxygen saturation vitals", "medical"),

    # Technology
    ("technology network system software hardware", "technology"),
    ("internet protocol wireless network generation", "technology"),
    ("5g 4g lte network technology wireless spectrum", "technology"),
    ("computer algorithm data processing software", "technology"),
    ("server database api request response system", "technology"),
    ("mobile network bandwidth frequency modulation", "technology"),
    ("access scheme architecture evolution generation", "technology"),
    ("power amplifier signal transistor circuit electronic", "technology"),
    ("amplifier gain frequency voltage current waveform", "technology"),
    ("electronic circuit resistor capacitor inductor", "technology"),
    ("digital signal processing filter bandwidth", "technology"),
    ("microprocessor embedded system hardware controller", "technology"),
    ("semiconductor diode transistor electronic component", "technology"),
    ("machine learning model training dataset neural", "technology"),
    ("cloud computing aws azure deployment container", "technology"),
    ("operating system kernel process thread memory", "technology"),
    ("cybersecurity encryption firewall vulnerability", "technology"),
    ("web development html css javascript frontend", "technology"),
    ("python java programming code function class", "technology"),
    ("router switch packet tcp ip networking", "technology"),

    # Education
    ("student exam marks grade university college", "education"),
    ("syllabus course lecture assignment semester", "education"),
    ("result marksheet certificate degree diploma", "education"),
    ("thesis research paper abstract methodology", "education"),
    ("curriculum lesson plan teaching learning", "education"),
    ("scholarship admission application form", "education"),
    ("tutorial exercise problem solution practice", "education"),
    ("notes unit chapter topic subject study", "education"),
    ("quiz test assessment evaluation rubric", "education"),
    ("project report submission deadline marks", "education"),

    # Research
    ("abstract introduction methodology conclusion research", "research"),
    ("literature review findings analysis discussion", "research"),
    ("hypothesis experiment data collection results", "research"),
    ("journal paper publication citation reference", "research"),
    ("survey questionnaire respondents sample study", "research"),
    ("statistical analysis regression correlation", "research"),

    # Business
    ("company profile mission vision strategy", "business"),
    ("marketing campaign brand product launch", "business"),
    ("meeting minutes agenda action items", "business"),
    ("project proposal scope deliverables timeline", "business"),
    ("annual report quarterly performance review", "business"),
    ("employee performance appraisal kpi target", "business"),
    ("business plan startup revenue model investor", "business"),

    # Image
    ("image width height mode pixels RGB JPEG PNG", "image"),
    ("image width height mode RGB resolution bitmap", "image"),
    ("image width height mode JPEG screenshot", "image"),
    ("image width height mode PNG transparency", "image"),

    # General
    ("document file general information data report", "general"),
    ("report summary information general document", "general"),
    ("letter correspondence address dear sincerely", "general"),
]

texts = [item[0] for item in training_data]
labels = [item[1] for item in training_data]

# Pipeline use karo — better accuracy
classifier = Pipeline([
    ('tfidf', TfidfVectorizer(
        ngram_range=(1, 2),      # single words + word pairs
        max_features=5000,        # top 5000 features
        sublinear_tf=True,        # better scaling
        min_df=1,
    )),
    ('model', MultinomialNB(alpha=0.1))  # lower alpha = more precise
])

classifier.fit(texts, labels)

def classify_document(text):
    """Document ka text lo aur category batao"""
    if not text or len(text.strip()) == 0:
        return "general"

    # Zyada text use karo — 1000 characters
    text_sample = text[:1000].lower()

    prediction = classifier.predict([text_sample])
    confidence = classifier.predict_proba([text_sample]).max()

    print(f" Confidence: {confidence:.2%}")

    return prediction[0]