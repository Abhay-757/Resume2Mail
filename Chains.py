import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()
API_Key = os.getenv('API_Key')

class Email:
    def __init__(self):
        self.llm = ChatGroq(
    temperature=0.7,
    api_key = API_Key,
    model='llama-3.1-8b-instant',
)
    def Resume_Input(self,Page_data):
        Text = "\n".join([doc.page_content for doc in Page_data])
        Splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        Chunks = Splitter.split_text(Text)
        All_Result = []
        parser = JsonOutputParser()

        Prompt_Extract =  PromptTemplate.from_template(
            """
                ###SCRAPED TEXT FROM WEBSITE:
                {page_data}
                ###INSTRUCTION:
                The scrap text is a resume.
                Your job is to extarct the following keys
                followings keys: 'education, 'experience', 'skills' and 'description', achievment.
                Only return the valid JSON.
                ### VALID JSON (NO PREAMBLE)
                """
        )

        Chain = Prompt_Extract | self.llm

        for Chunk in Chunks[:-1]:
            try:
                Result = Chain.invoke({'page_data': Chunk})
                Parsed = parser(Result.content)
                All_Result.append(Parsed)
            except Exception:
                continue
        return All_Result

    def Write_Email(self,resume,company,role):
        
        Email_Prompt = PromptTemplate.from_template("""
        ###CANDIDATE PROFILE:
        {profile}

        TARGET COMPANY: {company}
        TARGET ROLE: {role}
                            
        ###INSTRUCTION:
        - Write a concise, professional email (120–150 words)
        - Start with a polite greeting
        - Clearly mention the role being applied for
        - Highlight 2–3 relevant skills from the profile
        - Mention at least one project or experience aligned with the role
        - Show genuine interest in the company
        - Maintain a confident but respectful tone
        - Avoid generic phrases like "I am passionate" unless supported by experience
        - Do NOT repeat the entire resume
        - Keep it human, natural, and not robotic
        - End with a polite closing and call to action

        Output Format:
        - Only return the email text
        - Do not include explanations or extra comments
                                                
    """)
        Email_Chain = Email_Prompt | self.llm

        Response =  Email_Chain.invoke({
            'profile':str(resume),
            'company': company,
            'role':role
        })

        return Response.content
 