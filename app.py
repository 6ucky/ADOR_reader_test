from fastapi import FastAPI
from data_pipeline import DocxReader, XlsxReader, PptxReader, PdfReader

from llama_index.core import SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
from llama_index.core.ingestion import IngestionPipeline
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.extractors.entity import EntityExtractor
from llama_index.core import VectorStoreIndex

import re
import spacy

os.environ["OPENAI_API_KEY"] = ""

Settings.embed_model = OpenAIEmbedding(embed_batch_size=10)

nlp = spacy.load("en_core_web_sm")

app = FastAPI()

file_extractor = {
    ".docx": DocxReader(),
    ".xlsx": XlsxReader(),
    ".pptx": PptxReader(),
    ".pdf": PdfReader()
}

def extract_entities_rule_based(text):
    entities = {
        "Company": re.findall(r"Company:\s*([\w\s]+)", text),
        "Sponsor": re.findall(r"Sponsor:\s*([\w\s]+)", text),
        "Investor": re.findall(r"Investor:\s*([\w\s]+)", text),
        "Pre-money Valuation": re.findall(r"Pre-money Valuation:\s*([\w\s\d]+)", text),
        "Amount of Financing": re.findall(r"Amount of Financing:\s*([\w\s\d,]+)", text),
        "Security Type": re.findall(r"Type of Security:\s*([\w\s]+)", text),
        "Dividends": re.findall(r"Dividends:\s*([\w\s\d%,]+)", text),
        "Liquidation Preference": re.findall(r"Liquidation Preference:\s*([\w\s\d%,]+)", text),
        "Exit Period": re.findall(r"Exit Period:\s*([\d]+ months)", text),
        "Voting Rights": re.findall(r"Voting Rights:\s*([\w\s\d]+)", text),
    }

    return {key: value[0] if value else None for key, value in entities.items()}

def extract_entities_spacy(text):
    doc = nlp(text)
    extracted_entities = {ent.label_: ent.text for ent in doc.ents}
    return extracted_entities

def build_pipeline():

    openai_llm = OpenAI(model="gpt-3.5-turbo-1106", temperature=0.1)
    transformations = [
        EntityExtractor(prediction_threshold=0.5),
        Settings.embed_model,
    ]

    return IngestionPipeline(transformations=transformations)




@app.get("/rule")
async def ner_rule(file_folder_path: str = './example'):
    try:
        documents = SimpleDirectoryReader(file_folder, file_folder_path=file_extractor).load_data()
        print("Documents are charged successfully.")
    except Exception as e:
        print(f"Errors: {e}")
        return f"Errors: {e}"
    
    response = []
    for document in documents:
        response.append(extract_entities_rule_based(document.to_embedchain_format()['data']['content']))
    return str(response)

@app.post("/spacy")
async def ner_spacy(file_folder_path: str = './example'):
    try:
        documents = SimpleDirectoryReader(file_folder, file_folder_path=file_extractor).load_data()
        print("Documents are charged successfully.")
    except Exception as e:
        print(f"Errors: {e}")
        return f"Errors: {e}"

    response = []
    for document in documents:
        response.append(extract_entities_spacy(document.to_embedchain_format()['data']['content']))
    return str(response)

@app.get("/llm")
async def ner_llm(file_folder_path: str = './example', query: str = "What is Infuse Capital?"):
    try:
        documents = SimpleDirectoryReader(file_folder, file_folder_path=file_extractor).load_data()
        print("Documents are charged successfully.")
    except Exception as e:
        print(f"Errors: {e}")
        return f"Errors: {e}"
    
    pipline = build_pipeline()
    nodes = await pipline.arun(documents=documents,show_progress=True)
    index = VectorStoreIndex(nodes=nodes)
    query_engine = index.as_query_engine()
    response = query_engine.query(query)
    return response