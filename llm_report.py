from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import fitz
import tiktoken
import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from fpdf import FPDF

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

enc = tiktoken.encoding_for_model("gpt-4")
llm = ChatOpenAI(
    model_name="gpt-4",
    temperature=0,
    api_key=os.getenv(
        "OPENAI_API_KEY"
    ),  ## it seems we need to make this in env?? weird
)
embedding_model = OpenAIEmbeddings()

MAX_TOKENS = 4000 ## random number


@app.post("/process")
async def process_pdf(file: UploadFile = File(...)):
    print("is the file here?????")
    pdf_bytes = await file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = "\n".join([page.get_text() for page in doc])

    token_count = len(enc.encode(text))

    if token_count <= MAX_TOKENS:
        prompt = f"Extract applicant info from this text:\n\n{text}"
        response = llm.predict(prompt)
        print("GOOD")
        print(response)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        lines = response.split("\n")
        for line in lines:
            if len(line) > 80:
                words = line.split()
                current_line = ""
                for word in words:
                    if len(current_line + " " + word) < 80:
                        current_line += " " + word
                    else:
                        pdf.cell(0, 10, txt=current_line.strip(), ln=True, align="L")
                        current_line = word
                if current_line:
                    pdf.cell(0, 10, txt=current_line.strip(), ln=True, align="L")
            else:
                pdf.cell(0, 10, txt=line, ln=True, align="L")

        pdf.output("output.pdf", "F")
        return {"tokens": token_count, "mode": "direct", "response": response}

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_text(text)
    vectordb = FAISS.from_texts(chunks, embedding_model)
    retriever = vectordb.as_retriever()

    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    response = qa.run("Extract applicant GPA, intended major, and test scores.")
    print("GOOD")
    print(response)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    lines = response.split("\n")
    for line in lines:

        if len(line) > 80:
            words = line.split()
            current_line = ""
            for word in words:
                if len(current_line + " " + word) < 80:
                    current_line += " " + word
                else:
                    pdf.cell(0, 10, txt=current_line.strip(), ln=True, align="L")
                    current_line = word
            if current_line:
                pdf.cell(0, 10, txt=current_line.strip(), ln=True, align="L")
        else:
            pdf.cell(0, 10, txt=line, ln=True, align="L")

    pdf.output("output.pdf", "F")
    return {"tokens": token_count, "mode": "RAG", "response": response}

