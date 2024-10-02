import sys
import os
import tempfile
import pdfplumber
import shutil
import streamlit as st
from langchain.retrievers import ParentDocumentRetriever
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader,UnstructuredExcelLoader,UnstructuredWordDocumentLoader
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_chroma.vectorstores import Chroma
from langchain.storage import InMemoryStore
from langchain.schema import Document

# py_file_location = "/content"
sys.path.append(os.path.abspath('/content/htmlTemplates.py'))

from htmlTemplates import page_style, title_html, sidebar_style, logo_html

# Set the API key
os.environ["OPENAI_API_KEY"] = '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'

# Directory to load the documents from
docs_directory = "./docs"
chroma_db_path = "chroma_db"

def is_dual_page_layout(page):
    """
    Check if a PDF page has a dual-page layout based on the width-to-height ratio.
    Returns True if the page is likely dual-page, False otherwise.
    """
    width = page.width
    height = page.height
    # If the width is roughly twice the height, we assume it's a dual-page layout
    return width / height > 1.5

def split_dual_page_layout(pdf_path):
    """
    Split the pages of a PDF file into left and right parts if it has a dual-page layout.
    Returns a list of Document objects.
    """
    docs = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            if is_dual_page_layout(page):
                width = page.width
                height = page.height

                # Split the page into left and right halves
                left_page = page.within_bbox((0, 0, width / 2, height))
                right_page = page.within_bbox((width / 2, 0, width, height))

                # Extract text from each half
                left_text = left_page.extract_text()
                right_text = right_page.extract_text()

                # Wrap the text into Document objects with metadata
                if left_text:
                    docs.append(Document(page_content=left_text, metadata={'page_number': f'{page_num}-left'}))
                if right_text:
                    docs.append(Document(page_content=right_text, metadata={'page_number': f'{page_num}-right'}))
            else:
                # If not a dual-page layout, extract the entire page
                full_text = page.extract_text()
                if full_text:
                    docs.append(Document(page_content=full_text, metadata={'page_number': page_num}))
    return docs

def load_documents_from_directory(directory):
    if directory.endswith('.pdf'):
        loader = PyPDFLoader(directory)
        docs = loader.load()
    else:
        docs = []
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if filename.endswith('.pdf'):
                loader = PyPDFLoader(file_path)
            elif filename.endswith('.xlsx'):
                loader = UnstructuredExcelLoader(file_path)
            elif filename.endswith('.docx'):
                loader = UnstructuredWordDocumentLoader(file_path)
            else:
                continue
            docs.extend(loader.load())
    return docs


def load_pdf(pdf_docs):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(pdf_docs.read())
        temp_file_path = temp_file.name

    docs = split_dual_page_layout(temp_file_path)

    os.remove(temp_file_path)
    return docs


def get_vectorstore(_docs, _collection_name, _persist_directory):
    parent_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    child_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")

    child_vectorstore = Chroma(
        collection_name=_collection_name,
        embedding_function=embedding_model,
        persist_directory=_persist_directory
    )

    parent_docstore = InMemoryStore()

    retriever_parent = ParentDocumentRetriever(
        vectorstore=child_vectorstore,
        docstore=parent_docstore,
        child_splitter=child_splitter,
        parent_splitter=parent_splitter
    )
    retriever_parent.add_documents(_docs)

    return retriever_parent

def get_conversation_chain(vectorstore):
#     human_message_template = PromptTemplate.from_template(
#     """
#      You are an experienced and knowledgeable insurance assistant, highly skilled in providing \\
#        accurate and concise answers based on the given context.
#     Your goal is to deliver clear, concise, and brief responses that include only the most\\
#          essential details from the context.
#     Focus on relevance and prioritize the most critical information to directly address the\\
#         question in a short and precise manner.

#     Structure your answer logically, maintaining a professional and courteous tone throughout.
#     If the context is extensive, summarize key points and ensure your answers are simple, easy to understand.

#     Check these conditions before answering:
#     1. Extract the coverage details from the coverage summary section which is a tabular data. \\
#     Ensure that null values are clearly indicated as "N/A" or left blank if appropriate.Typically, after a home address, \\
#     the dwelling coverage information is presented first, followed by content coverage. Please identify and \\
#     return the details accordingly.
#     2. Homeowners insurance policies cover damage caused by fires, including wildfires.
#     When a property is covered with a home insurance, the wildfire loses are covered.
#     3. Losses by fire are covered by the home insurance policies.
#     4. If the question is about the policy's active period, calculate the remaining months by comparing today's date to the policy expiration date.
#     5. If you are unsure of the answer, then ask them to contact insurance agent or customer care.
#     6. Whenever the prompt is about personal belongings include the contents coverage summary with cost details.
#     7. If someone wants to contact the customer care, then first offer to help before providing the customer care information.
#     8. If the prompt is about motor vechicle accident and policy includes auto insurance, \\
#         then provide the dedicated hotline number along with your assistance.
#     9. If the query is asking about the property/properties please provide details of house/home properties only.

#     Question: {question}
#     Context: {context}
#     Answer:
#     """
# )

    human_message_template = PromptTemplate.from_template('''

     You are an experienced and knowledgeable insurance assistant, highly skilled in providing \\
       accurate and concise answers based on the given context.
    Your goal is to deliver clear, concise, and brief responses that include only the most\\
         essential details from the context.
    Focus on relevance and prioritize the most critical information to directly address the\\
        question in a short and precise manner.

    Question: {question}
    Context: {context}
    Answer:

    '''
    )


    human_message_prompt_template = HumanMessagePromptTemplate(prompt=human_message_template)
    chat_prompt_template = ChatPromptTemplate(input_variables=['context', 'question'], messages=[human_message_prompt_template])
    gpt4o = ChatOpenAI(temperature=0, model_name="gpt-4o")
    rag_chain = chat_prompt_template | gpt4o | StrOutputParser()
    return rag_chain

def get_parent_content(child_docs, retriever_parent):
    parent_content = []
    for child in child_docs:
        doc_id = child.metadata['doc_id']
        parent_doc = retriever_parent.docstore.store.get(doc_id)
        if parent_doc not in parent_content:
            parent_content.append(parent_doc)
    return parent_content

def handle_userinput(user_question, retriever_parent):
    if retriever_parent is None:
        return "Error: No document loaded. Please upload a document first."

    child_docs = retriever_parent.vectorstore.similarity_search(user_question, k=15)
    parent_content = get_parent_content(child_docs, retriever_parent)
    response = st.session_state.conversation.invoke({"context": parent_content, "question": user_question})
    return response

def delete_previous_policy_vectorstore():
    if "vectorstore" in st.session_state and st.session_state.vectorstore is not None:
        if 'user_policy' in st.session_state.vectorstore.vectorstore._client.list_collections():
            st.session_state.vectorstore.vectorstore._client.delete_collection('user_policy')
            st.session_state.vectorstore = None
            st.session_state.conversation = None

# Initialization on app start
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
    st.session_state.conversation = None

st.markdown(logo_html, unsafe_allow_html=True)
st.markdown(page_style, unsafe_allow_html=True)
st.markdown(title_html, unsafe_allow_html=True)
st.markdown(sidebar_style, unsafe_allow_html=True)

# Load documents from directory and create Chroma DB if not already created
if st.session_state.vectorstore is None and not os.path.exists(chroma_db_path):
    with st.spinner("Initiating the chat conversation..."):
        docs = load_documents_from_directory(docs_directory)
        st.session_state.vectorstore = get_vectorstore(docs, "docs_collection", chroma_db_path)
        st.session_state.conversation = get_conversation_chain(st.session_state.vectorstore)
        st.success("Start your conversation now or upload your policy!")

# Display chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("How can I help you?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if st.session_state.vectorstore:
            result = handle_userinput(prompt, st.session_state.vectorstore)
            #result = result.replace('$','USD ')
        else:
            result = "Error: No document loaded. Please upload a document first."
        st.markdown(result)
    st.session_state.messages.append({"role": "assistant", "content": result})

with st.sidebar:
    st.subheader("Your documents")
    pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", type=["pdf"])

    if pdf_docs is not None and st.button("Process"):
        delete_previous_policy_vectorstore()  # Delete the previous collection before processing a new one
        with st.spinner("Processing"):
            raw_text = load_pdf(pdf_docs)
            st.session_state.vectorstore = get_vectorstore(raw_text, "user_policy", chroma_db_path)
            st.session_state.conversation = get_conversation_chain(st.session_state.vectorstore)
            st.success("Processing complete! You can now start querying your document.")

