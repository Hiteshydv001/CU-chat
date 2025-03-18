import fitz  # PyMuPDF
import logging
import os
from nltk.tokenize import sent_tokenize

# Configure logging
logging.basicConfig(
    filename="chatbot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def extract_text_from_pdf(pdf_path):
    try:
        logging.info(f"Attempting to open PDF: {pdf_path}")
        doc = fitz.open(pdf_path)
        logging.info(f"PDF opened successfully with {doc.page_count} pages")
        text = ""
        for page_num, page in enumerate(doc):
            page_text = page.get_text("text").strip()
            if page_text:
                text += page_text + "\n"
                logging.info(f"Page {page_num + 1} text (first 200 chars): {page_text[:200]}...")
            else:
                logging.warning(f"Page {page_num + 1} contains no extractable text")
        doc.close()
        logging.info(f"Total extracted text length: {len(text)} characters")
        if not text:
            logging.error("No text extracted from the PDF")
        return text
    except Exception as e:
        logging.error(f"PDF extraction error: {str(e)}")
        return ""

def extract_faqs(pdf_text):
    try:
        import nltk
        nltk.download('punkt', quiet=True)  # Download sentence tokenizer data
        sentences = sent_tokenize(pdf_text)
        faqs = {}
        for i, sentence in enumerate(sentences):
            if "?" in sentence:
                question = sentence.strip()
                # Look for the next sentence as a potential answer
                if i + 1 < len(sentences):
                    next_sentence = sentences[i + 1].strip()
                    if next_sentence and not "?" in next_sentence:
                        faqs[question] = next_sentence
        logging.info(f"Extracted {len(faqs)} FAQ pairs: {faqs}")
        return faqs
    except Exception as e:
        logging.error(f"FAQ extraction error: {str(e)}")
        return {}

if __name__ == "__main__":
    text = extract_text_from_pdf("data/university_faqs.pdf")
    faqs = extract_faqs(text)
    print(faqs)