from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_astradb import AstraDBVectorStore
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor  # Corrected typo and syntax
from langchain.tools.retriever import create_retriever_tool  # Assuming corrected names
from github import fetch_issues
from note import note_tool

load_dotenv()

def connect_to_vstore():
    embeddings = OpenAIEmbeddings()
    # vstore = AstraDBVectorStore(embeddings)
    ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
    ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
    desired_namespace = os.getenv("ASTRA_DB_KEYSPACE")
    if desired_namespace:
        ASTRA_DB_KEYSPACE = desired_namespace
    else:
        ASTRA_DB_KEYSPACE = None

    vstore = AstraDBVectorStore(embedding = embeddings, collection_name = "github", api_endpoint = ASTRA_DB_API_ENDPOINT, token = ASTRA_DB_APPLICATION_TOKEN, namespace = ASTRA_DB_KEYSPACE)
    return vstore


vstore = connect_to_vstore()
add_to_vstore = input("Would you like to add to the vector store? (y/n): ")
if(add_to_vstore == "y"):
    owner = input("Owner: ")
    repo = input("Repo: ")
    issues = fetch_issues(owner, repo)
    
    try:
        vstore.delete_collection()
    except exceptions as e:
        print(e)
        pass

    vstore = connect_to_vstore()
    vstore.add_documents(issues)

    # results = vstore.similarity_search("flash_messages", k = 3)
    # for res in results:
    #     print(f"* {res.page_content} {res.metadata}")


retriever = vstore.as_retriever(search_kwags = {"k": 3})
retriever_tool = create_retriever_tool(
    retriever,
    "github_search",
    "Search for information about github issues, for any question about github issues, you must use this tool!",
    )

prompt = hub.pull("hwchase17/openai-functions-agent")
llm = ChatOpenAI(prompt = prompt)

tools = [retriever_tool, note_tool]
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executer = AgentExecutor(agent=agent, tools = tools, verbore = True)

while(question = := input("Ask a question about github issues: ")):
    response = agent_executer.invoke({"input" : question})
    print(response["output"])






