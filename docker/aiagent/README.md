# **AI Agent Container Documentation (Simple Prototype)**

## **1. Introduction**

This **aiagent** container is a **simple base prototype** in the context of the AI Agent Lab. It demonstrates a minimal working version of an AI agent that:

1. Accepts a user’s natural language query (e.g., “How many records are in the binance_trades table?”).  
2. Generates a corresponding SQL query using **LangChain/LangGraph**.  
3. Executes the query against **QuestDB**.  
4. Returns the results to the user in a simple, readable format.

This prototype focuses on **core functionality** with minimal complexity. Advanced features (like multi-step reasoning, complex graphs, or integrations with multiple tools) are intentionally out of scope and can be added in future improvements.

---

## **2. Project Structure**

Below is the project file structure of the `aiagent/` directory:

```
aiagent/
├── app/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   ├── tool.py
│   │   ├── memory.py
│   ├── interface/
│   │   ├── __init__.py
│   │   ├── agent_interface.py
│   │   ├── tool_interface.py
│   │   ├── memory_interface.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── chat_routes.py
│   │   ├── health_routes.py
├── run.py
├── config.py
├── Dockerfile
├── requirements.txt
```

---

## **3. Interface-First Design Philosophy**

This project employs an **Interface-First Design** to ensure modularity and flexibility:

- **`AgentInterface`** defines the expected methods and behavior of an AI agent:
  - Must provide `invoke(user_message: str) -> str` to process user input and return a text response.

- **`ToolInterface`** defines a contract for any external tool (e.g., a database or another service):
  - Must provide `execute_query(query: str) -> str` (or similarly named methods) to interact with external systems.

### **Why Interface-First?**
1. **Loose Coupling**: The application’s AI logic only depends on abstract interfaces—making each concrete implementation easily swappable or upgradable.  
2. **Easy Testing**: Each component can be tested against its interface without requiring the entire environment (e.g., QuestDB, actual LLM keys).  
3. **Extendibility**: New tools (e.g., a different database, an analytics service) can be added as long as they conform to the interfaces.

---

## **4. Core Components**

Below is an overview of the files that implement the agent’s functionality and illustrate the Interface-First approach.

### **4.1. `app/__init__.py`**
- **Purpose**: Initializes and configures the Flask application via a `create_app()` factory function.
- **Key Steps**:
  1. Creates a Flask app instance.
  2. Registers route blueprints:
     - **Chat** routes (`chat_routes.py`)
     - **Health** routes (`health_routes.py`)

### **4.2. `app/core/agent.py`**
- **Class**: `MainAgent`
- **Implements**: `AgentInterface`
- **Highlights**:
  - **LangChain/LangGraph** Integration: Constructs a “ReAct” agent with the specified large language model (LLM) and tools.
  - **System Prompt**: Injects a short description of the database schema so the agent can generate accurate SQL queries.
  - **Method**: `invoke(user_message: str) -> str`
    - Receives the user query.
    - Feeds it to the underlying LLM-based agent.
    - Returns the final response text.

### **4.3. `app/core/tool.py`**
- **Classes:**
  - **`QueryQuestDBTool`**: Executes SQL queries against QuestDB.
  - **`GrafanaDashboardTool`**: Manages Grafana dashboards via its HTTP API.
  - **`VSCodeIntegrationTool`**: Communicates with a VS Code extension via a WebSocket interface to create or delete files.
- **Highlights:**
  - **QueryQuestDBTool:** Uses `psycopg2` to connect to QuestDB.
  - **GrafanaDashboardTool:** Handles creating, deleting, and searching dashboards.
  - **VSCodeIntegrationTool:** Uses Python’s `websocket-client` library to send JSON commands over WebSocket to the VS Code extension.

### **4.4. `app/core/memory.py`**
- **Class**: `WindowMemoryManager`
- **Implements**: `MemoryInterface`
- **Highlights**:
  - Provides memory management for conversation context.
  - Uses a window-based approach to retain only the most recent messages (e.g., 10 messages) for context.
  - Enables multi-turn conversational capability.

### **4.5. `app/interface/` (Interfaces)
- **`agent_interface.py`**: Defines `AgentInterface` with the core method signature `invoke(user_message: str) -> str`.
- **`tool_interface.py`**: Defines `ToolInterface` with the core method signature `execute_tool(query: str) -> str`.
- **`memory_interface.py`**: Defines `MemoryInterface` with the necessary methods to manage conversation memory.
- **`__init__.py`**: Makes these interfaces easily importable from a single place.

This directory is pivotal in the **Interface-First** approach. By referencing the interfaces rather than concrete classes, the rest of the code remains flexible and unit-testable.

### **4.6. `app/routes/chat_routes.py`**
- **Blueprint**: `chat_bp`
- **Endpoint**: `POST /chat`
- **Flow**:
  1. Receives a JSON payload with a user `message`.
  2. Passes that message to `MainAgent().invoke(user_message)`.
  3. Returns the AI agent’s response in JSON form.

This route demonstrates how the system ties together: a user message flows from the Flask endpoint → `MainAgent` → `Tool` → returns final output as text.

### **4.6. `app/routes/health_routes.py`**
- **Blueprint**: `health_bp`
- **Endpoint**: `GET /health`
- **Flow**:
  1. Performs a trivial test query (`SELECT 1`) to QuestDB.
  2. Returns JSON “healthy” if successful or “unhealthy” if there is a connection issue.

---

## 5. VSCode Integration

The AI agent integrates with a VS Code extension that exposes a WebSocket interface for file management.

### Key Points:
- **WebSocket Endpoint:** The extension listens on the URL defined by `VSCODE_WS_URL` (e.g., `ws://vscode:8765`).
- **Command Format:**  
  When issuing VS Code file management commands, output a valid JSON object with the following keys:
  - **operation:** "create" or "delete"
  - **filepath:** Absolute file path (e.g., `/home/coder/new_file.txt`)
  - **content:** (Only for "create") the content to write in the file

### Example Commands:
- **Create a File:**

'''
{ "operation": "create", "filepath": "/home/coder/new_file.txt", "content": "Hello, there. How are you? Hope you're doing well." }
'''

- **Delete a File:**

'''
{ "operation": "delete", "filepath": "/home/coder/new_file.txt" }
'''

The AI agent uses the `VSCodeIntegrationTool` to send these JSON commands over WebSocket to the VS Code extension, which then performs the file operations.

---

## **Conclusion**

This simple prototype demonstrates an **Interface-First Design** that results in a modular, testable AI agent. It integrates natural language processing, SQL query generation, database querying (QuestDB), dashboard management (Grafana), and file management through a custom VS Code extension.

With this foundation in place, additional features and integrations can be layered on as the project evolves, maintaining clear separations of concern thanks to the use of well-defined interfaces.
