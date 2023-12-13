import streamlit as st
import  warnings 
import  os  
from AiMazingLLM import  AiAmaizing_llm
from load_pdf import  preprocess_pdf
from langchain.document_loaders  import  PyPDFLoader
from pdf_reader import  read_pdf
from langchain.embeddings import HuggingFaceHubEmbeddings
from langchain.document_loaders  import  PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma, FAISS
from langchain.embeddings import HuggingFaceHubEmbeddings
from langchain.llms.base import LLM
from langchain.chains import RetrievalQA
from langchain.document_loaders.csv_loader import  CSVLoader
import os
from tempfile import NamedTemporaryFile 
import warnings
import random
from ocr import  ocr_space_file
import string
os.environ["EMAIL"]  
os.environ["PASS"] 
warnings.filterwarnings("ignore")
from streamlit_login_auth_ui.widgets import __login__

__login__obj = __login__(auth_token = "courier_auth_token", 
                    company_name = "Shims",
                    width = 200, height = 250, 
                    logout_button_name = 'Logout', hide_menu_bool = False, 
                    hide_footer_bool = False, 
                    lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

LOGGED_IN = __login__obj.build_login_ui() 
def clear():
        st.cache_resource.clear()
st.write("AiMazing")
with st.sidebar:
    option = st.selectbox('Choose your preferred model:',('Llama-2-70b-chat-hf', 'CodeLlama-34b-Instruct-hf', 'falcon-180B-chat', 'Mistral-7B-Instruct-v0.1'),on_change=clear) 
    chat_option = st.radio(
    "What's your favorite movie genre",
    ["Chat", "Chat with your  docs", "Chat with your printed  text"],
    captions = ["Normal chat", "Chat with your  .pdf files.", "chat with your printed screenshots  (jpg/jpeg)"])
#def  pdfllm():
 #   llm = 
if LOGGED_IN == True:
    if  chat_option == "Chat":
            #from metallma2wambugu.huglogin import login
        #import sys
        from hugchat import hugchat
        from hugchat.login import Login
        import os
        import time
        from functools import lru_cache
        import streamlit as st
        #import logging
        #logging.basicConfig(level=logging.DEBUG)
        @st.cache_resource(show_spinner="Loading the model")#(experimental_allow_widgets=True)
        def chatwithme(model):
            email= os.environ["EMAIL"]
            pass_w = os.environ["PASS"]
                #chatbot = login(email,pass_w).login()
            sign = Login(email,pass_w)
            cookies = sign.login()

            # Save cookies to the local directory
            cookie_path_dir = "./cookies_snapshot"
            sign.saveCookiesToDir(cookie_path_dir)
            chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
        #,temperature= 0.5, max_new_tokens= 4029, web_search=True)#chatbot.chat(prompt)
            chatbot.switch_llm(model)
            chatbot.new_conversation(switch_to =True, system_prompt="Your name is 'AiMazing', If you are greeted with hello, hey, how are you, etc your reply must have  'Hello welcome  to AiMazing assistant, ask anything...'")
            return chatbot
           # if os.environ["EMAIL"] or os.environ["PASS"] ==None:
           #     st.error("Huggingface Login required!")
        #@st.cache_resource
        def login_data():

            return cookies

        st.header("AiMazing")
        
        def web_search(prompt):
            sign = Login(os.environ['EMAIL'], os.environ['PASS'])
            cookies = sign.login()
            cookie_path_dir = "./cookies_snapshot1"
            sign.saveCookiesToDir(cookie_path_dir)
            chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
            res = chatbot.query(prompt, temperature=0.6, web_search=True)
            new = [f" - __Source from the web:__ - `Title`:{source.title} - `source`: {source.hostname}  `Link`: {source.link}" for source in res.web_search_sources]
            full_resp = "{} {}".format(res["text"],' '.join(new))
            return full_resp
        with st.sidebar:
            st.markdown("Access real time response:")
            websearch = st.checkbox("Web search")
            st.markdown("__Developer:__ Wambugu kinyua")
            st.markdown("__Email:__ kenliz1738@gmail.com")
            st.markdown("__Note:__ The app is still in development it might break")
        #option_label=False
        #on = st.toggle("Enable model switching:")
        #if on:
        #    st.cache_data.clear()

        st.markdown(f'- You selected: _{option}_')
        if option == 'Llama-2-70b-chat-hf':

            chatbot = chatwithme(0)
            #chatbot.new_conversation(switch_to =True)
            #chatbot = chatwithme(0)#new_conversation(switch_to =True)
        elif option == "CodeLlama-34b-Instruct-hf":
           # st.cache_data.clear()
            chatbot  = chatwithme(1)
           # chatbot.new_conversation(switch_to =True)#chatbot = chatwithme(1)#chatbot.switch_llm(1)
            #chatbot.new_conversation(switch_to =True)
        elif option == "falcon-180B-chat":
            #st.cache_data.clear()
            chatbot  = chatwithme(2)
           # chatbot.new_conversation(switch_to =True)#chatbot = chatwithme(2)#chatbot.switch_llm(2)
            #chatbot.new_conversation(switch_to =True)
        elif option == "Mistral-7B-Instruct-v0.1":
            #st.cache_data.clear()
            chatbot  = chatwithme(3)
           # chatbot.new_conversation(switch_to =True)#chatbot = chatwithme(3)#chatbot.switch_llm(3)
            #chatbot.new_conversation(switch_to =True)
        else:
            st.markdown("Model not available!")
        try:
        #    websearch=st.checkbox("Web search?")
            #if websearch:
             #   st.markdown("Web search enabled")
            if "messages" not in st.session_state:
                st.session_state.messages = []

            # Display chat messages from history on app rerun
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            # Accept user input
            if prompt := st.chat_input("Ask your question?"):
                # Add user message to chat history
                st.session_state.messages.append({"role": "user", "content": prompt})
                # Display user message in chat message container
                with st.chat_message("user"):
                    st.markdown(prompt)

                # Display assistant response in chat message container
                with st.chat_message("assistant"):
                    with st.spinner("Generating response..."):
                        message_placeholder = st.empty()
                        full_response = ""
                        assistant_response = chatbot.query(prompt,temperature= 0.5, max_new_tokens= 4029)['text']#chatbot.chat(prompt)['text']
                        # Simulate stream of response with milliseconds delay
                        #with st.spinner(text="Generating response..."):
                       #### for chunk in assistant_response.split():
                            ###full_response += chunk + " "
                           ### time.sleep(0.05)
                            # Add a blinking cursor to simulate typing
                        if websearch ==False:
                            message_placeholder.markdown(assistant_response)# + "▌")
                        if websearch== True:
                           # data = chatbot.query(prompt,temperature= 0.5, max_new_tokens= 4029, web_search=True)#chatbot.chat(prompt)['text']
                            assistant_response = web_search(prompt)
                            message_placeholder.markdown(assistant_response)
                       # message_placeholder.markdown(full_response)
                    # Add assistant response to chat history
                    #st.markdown(
                    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                   # st.session_state.messages.append()
                ####
        except:
           # custom_notification_box(icon='info', textDisplay='Server error, try reprompting again', styles=styles, key ="foo")
            st.error("server error handling your result, reprompt again")#(icon='info', textDisplay='Server error, try reprompting again...',
    if  chat_option == "Chat with your  docs":
        with st.sidebar:
            uploaded_file = st.file_uploader('Choose your .pdf file', type="pdf")
            if uploaded_file is not None:
                text = read_pdf().read(uploaded_file)
                repo_id = "sentence-transformers/all-mpnet-base-v2"
                embeddings = HuggingFaceHubEmbeddings(
                repo_id=repo_id,
                task="feature-extraction"
            )
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0, length_function = len,)
                texts = text_splitter.create_documents(text) 
                db  = FAISS.from_documents(texts, embeddings)
                
                
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Accept user input
        if prompt := st.chat_input("Ask your question?"):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                with st.spinner("Generating response..."):
                    message_placeholder = st.empty()
                    full_response = ""
                    llm  =  AiAmaizing_llm(email= os.environ["EMAIL"],psw = os.environ["PASS"])
                    retriever = db.as_retriever()
                    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
                    res = qa({"query": f"{prompt}"})#ask your question from your pdf
                    assistant_response = res["result"]
                    # Simulate stream of response with milliseconds delay
                    #with st.spinner(text="Generating response..."):
                   #### for chunk in assistant_response.split():
                        ###full_response += chunk + " "
                       ### time.sleep(0.05)
                        # Add a blinking cursor to simulate typing
                
                    message_placeholder.markdown(assistant_response)# + "▌")
                   # message_placeholder.markdown(full_response)
                # Add assistant response to chat history
                #st.markdown(
                st.session_state.messages.append({"role": "assistant", "content": assistant_response})
               # st.session_state.messages.append()
            
    if  chat_option  == "Chat with your  data":
        with st.sidebar:
            uploaded = st.file_uploader('Choose your .jpg file')
            if uploaded is not None:
                with open("ken.jpg", "wb") as f:
                    f.write(uploaded.read())
                with st.spinner("Extracting  the  text..."):
                    res = ocr_space_file(filename = "ken.jpg").json()['ParsedResults'][0]['ParsedText']

                    repo_id = "sentence-transformers/all-mpnet-base-v2"
                    embeddings = HuggingFaceHubEmbeddings(
                    repo_id=repo_id,
                    task="feature-extraction"
                    )
                    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0, length_function = len,)
                    texts_ = text_splitter.create_documents([res]) 
                    data_base = FAISS.from_documents(texts_, embeddings)

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Accept user input
        if prompt := st.chat_input("Ask your question?"):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                with st.spinner("Generating response..."):
                    message_placeholder = st.empty()
                    full_response = ""
                    llm  =  AiAmaizing_llm(email= os.environ["EMAIL"],psw = os.environ["PASS"])
                    retriever = data_base.as_retriever()
                    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
                    res_ = qa({"query": f"{prompt}"})#ask your question from your pdf
                    assistant_response = res_["result"]
                    message_placeholder.markdown(assistant_response)# + "▌")
                   # message_placeholder.markdown(full_response)
                # Add assistant response to chat history
                #st.markdown(
                st.session_state.messages.append({"role": "assistant", "content": assistant_response})
               # st.session_state.messages.append()



                
            
        


                
                
                
            
        
        
        
