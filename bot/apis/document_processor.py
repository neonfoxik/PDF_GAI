import os
from pathlib import Path
import PyPDF2
from striprtf.striprtf import rtf_to_text

class DocumentProcessor:
    def __init__(self):
        self.laws_dir = Path(__file__).parent.parent / 'documents' / 'LAWS'
        self.documents = {
            'koap': 'КоАП РФ (в ред. от 24.06.2024).pdf',
            'police_order': 'Приказ_МВД_РФ_от_02_05_2023_N_264_Об_утверждении_Порядка_осуществления.rtf',
            'police_law': 'фз №3, о Полиции.pdf',
            'doc1': 'doc1'
        }

    def read_pdf(self, file_path):
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text

    def read_rtf(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            rtf_content = file.read()
            return rtf_to_text(rtf_content)

    def read_doc1(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def process_documents(self):
        documents_content = {}
        for doc_name, filename in self.documents.items():
            file_path = self.laws_dir / filename
            if not file_path.exists():
                continue

            if filename.endswith('.pdf'):
                content = self.read_pdf(file_path)
            elif filename.endswith('.rtf'):
                content = self.read_rtf(file_path)
            else:
                content = self.read_doc1(file_path)

            documents_content[doc_name] = content

        return documents_content 