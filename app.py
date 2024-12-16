import json
import os
import requests
from requests.auth import HTTPBasicAuth
# from dotenv import load_dotenv
from typing import Dict
from fastapi import FastAPI, Depends, HTTPException, status, Request, Form
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles


print("Listening on PORT:", os.getenv("PORT"))

# load_dotenv()
# web_auth = os.getenv('web_auth')
web_auth = 'user:mypasswd'
web_user, web_passwd = web_auth.split(':')
print(f'{web_user}-{web_passwd}')


    # print(type(data_agent))
url = "http://localhost:11434/api/chat"
DATA_FILE = "agent_user.json"

with open(DATA_FILE,"r") as file:
    data_agent = json.load(file)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
security = HTTPBasic()
fake_db: Dict[str, str] = {
    web_user: web_passwd
}

@app.get("/", response_class=HTMLResponse)
async def read_root_credential(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = fake_db.get(credentials.username)
    if correct_username is None or correct_username != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return templates.TemplateResponse("home.html", {"request": request})

#response user input a prompt to ai agent
@app.get("/ask/{user_input}")
def get_response_json(user_input: str):
    # with open(DATA_FILE,"r") as f2:
    #     data_agent = json.load(f2)
    payload = {
        "model": "llama3.2",
        "messages": [
            {"role": "user", "content": user_input}
        ]
    }
    print(url)
    print(payload)
    try:
        response = requests.post(url, json=payload)
        print(response)
        response.raise_for_status()  # Check for HTTP errors
        raw_response = response.text.strip()
        json_parts = raw_response.split('\n')  # Assuming each line is a separate JSON object
        output=[]
        for part in json_parts:
            try:
                json_data = json.loads(part)
                output.append(json_data["message"]["content"])
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {e}")
        result = ''.join(output)
        data_agent.append({"user_input":user_input,"ai_output":result})
        # print(data_agent)
        return result
    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
    except ValueError as e:
        print(f"Error parsing JSON response: {e}")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail=repr(e))

@app.post("/submit")
def submit_data(request: Request, user_input: str = Form(...)):

    payload = {
        "model": "llama3.2",
        "messages": [
            {"role": "user", "content": user_input}
        ]
    }
    print(url)
    print(payload)
    try:
        response = requests.post(url, json=payload)
        print(response)
        response.raise_for_status()  # Check for HTTP errors
        raw_response = response.text.strip()
        json_parts = raw_response.split('\n')  # Assuming each line is a separate JSON object
        output=[]
        for part in json_parts:
            try:
                json_data = json.loads(part)
                output.append(json_data["message"]["content"])
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {e}")
        result = ''.join(output)
        print({"user_input":user_input,"ai_output":result})
        data_agent.append({"user_input":user_input,"ai_output":result})
    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
    except ValueError as e:
        print(f"Error parsing JSON response: {e}")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail=repr(e))
    # Save updated data
    with open(DATA_FILE, "w") as f:
        json.dump(data_agent, f)
        print("Dump agent_user.json after submit")
    return RedirectResponse(url="/history", status_code=303)
    
#response dump snapshot of current json data base
@app.get("/dump_data")
def get_dumpdata():
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data_agent, file)
    print("Dump agent_user.json")
    return {"message": "Dump agent_user.json !!! "}

@app.get("/history")
def read_history(request: Request):
    return templates.TemplateResponse("history.html", {"request": request, "data": data_agent})

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))  # Use the PORT env variable
    uvicorn.run(app, host="0.0.0.0", port=port)
    
