## local_ai_agent
personal ai agent by local LLM (llama...)


## pre-requirements
install ollama in your local host


https://github.com/ollama/ollama

### validation PASS 
macOS 15.2 24C101 \
MACBOOK PRO M1 Pro 16GB \
ollama 0.5.1
- llama3.2
- llama3
python3 3.12/3.13


## local python script mode
python3 local_aiagent.py

according prompt to input to local ai agent

## web application mode
'''uvicorn app:app --host 0.0.0.0 --port 8080'''

then open web browser to access from localhost or ip address port 8080

such as home page in
### http://localhost:8080

### http://localhost:8080/docs 
show all available API

### edit .env file to update web access credential for your own

## web REST API
### http://localhost:8080/ask/string_to_ai_agent
send questions to AI Agent

### http://localhost:8080/dump_data
save current ai conversation history to agent_user.json

### http://localhost:8080/history
show all ai agent conversation 
