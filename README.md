# 🤖 Advanced QA RAG System

> **A sophisticated multi-agent AI assistant showcasing advanced RAG systems, SQL agents, and intelligent tool orchestration using LangGraph.**

---

## 🌟 Overview

**Advanced QA RAG System** is a comprehensive AI assistant that demonstrates enterprise-level architecture for building intelligent, multi-modal chatbots. This project combines **Retrieval-Augmented Generation (RAG)**, **SQL agents**, **web search**, and **conversation memory** into a unified system powered by **LangGraph's agent orchestration**.

Perfect for showcasing advanced AI engineering skills, system architecture design, and production-ready development practices.

---

## 🏗️ System Architecture

![alt text](<Screenshot 2025-08-17 024017.png>)

---

## ✨ Key Features

### 🤖 **Multi-Agent Orchestration**
- **LangGraph-powered** agent system with intelligent tool routing
- Dynamic decision-making for optimal tool selection
- State management across multi-step conversations

### 🔍 **Hybrid RAG Pipelines**
- **📋 Swiss Airline Policy RAG** → Company policy Q&A using PDF embeddings
- **📚 Stories RAG** → Contextual story retrieval from vector database
- **Semantic search** with ChromaDB vector store

### 🗄️ **Intelligent SQL Agents**
- **🎵 Chinook SQL Agent** → Music store analytics and business intelligence
- **✈️ Travel SQL Agent** → Flight booking queries and travel data analysis
- **Natural language** to SQL query translation

### 🌐 **Live Web Search**
- **DuckDuckGo** integration (default)
- **Tavily API** support for enhanced search capabilities
- Real-time information retrieval

### 🧠 **Advanced Memory Management**
- **Persistent conversation history** with CSV storage
- **Session-aware responses** with context retention
- Timestamp-based chat organization

### 🎨 **Professional UI Experience**
- **Clean Gradio interface** with custom avatars
- **Like/Dislike feedback** collection system
- **Real-time streaming** responses

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+**
- **Git**
- **API Keys**: Groq, Tavily (optional), HuggingFace

### 1️⃣ **Clone Repository**
```bash
git clone https://github.com/your-username/advanced-qa-rag-system.git
cd advanced-qa-rag-system
```

### 2️⃣ **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 3️⃣ **Environment Configuration**
Create `.env` file:
```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_key_optional
HF_TOKEN=your_huggingface_token
```

### 4️⃣ **Initialize Vector Databases**
```bash
python prepare_vector_db.py
```

### 5️⃣ **Launch Application**
```bash
python app.py
```

🎉 **Your AI assistant is now live at:** [http://localhost:7860](http://localhost:7860)

---

## 📁 Project Structure

```
advanced-qa-rag-system/
│
├── 🚀 app.py                     # Main Gradio application entry point
├── 📊 prepare_vector_db.py       # Vector database initialization
├── 📝 requirements.txt           # Python dependencies
│
├── 🤖 chatbot/
│   ├── chatbot_backend.py        # Core chatbot logic and orchestration
│   ├── memory.py                 # Conversation memory management
│   └── load_config.py            # Configuration loading utilities
│
├── 🧠 agent_graph/
│   ├── build_full_graph.py       # LangGraph agent construction
│   ├── tool_policy_rag.py        # Swiss Airline policy RAG tool
│   ├── tool_stories_rag.py       # Stories retrieval RAG tool
│   ├── tool_chinook_sql.py       # Chinook database SQL agent
│   ├── tool_travel_sql.py        # Travel database SQL agent
│   └── tool_web_search.py        # Web search integration
│
├── ⚙️ utils/
│   ├── ui_components.py          # Custom Gradio components
│   └── directory_utils.py        # File system utilities
│
├── 📋 configs/
│   ├── project_config.yaml       # Main project configuration
│   └── tools_config.yaml         # Tool-specific settings (LLMs, embeddings, DBs, APIs)
│
└── 💾 data/
    ├── unstructured_docs/        # Raw input documents for RAG
    │   ├── stories/              # Stories dataset (stories.pdf)
    │   └── swiss_airline_policy/ # Swiss airline FAQs & policy docs (swiss_faq.pdf)
    ├── airline_policy_vectordb/  # VectorDB for Swiss airline policy
    ├── stories_vectordb/         # VectorDB for stories dataset
    ├── Chinook.db                # Sample music store DB          
    └── travel.sqlite             # Travel booking database
```

---

## 🛠️ Technology Stack

### **Core AI Framework**
- **🧠 LangGraph** - Advanced agent orchestration and workflow management
- **🔗 LangChain** - LLM application framework and tool integration
- **🤖 Groq API** - High-performance LLM inference

### **Data & Storage**
- **🗄️ ChromaDB** - Vector database for semantic search and embeddings
- **💾 SQLite** - Relational database for structured data queries
- **📊 Pandas** - Data manipulation and analysis

### **Search & Retrieval**
- **🔍 Tavily API** - Premium web search capabilities
- **🦆 DuckDuckGo** - Privacy-focused web search fallback
- **🤗 HuggingFace** - Embedding models and transformers

### **User Interface**
- **🎨 Gradio** - Interactive web-based chat interface
- **💬 Custom Components** - Enhanced UX with avatars and feedback

---

## 🎯 Why This Project Matters

### **🚀 Technical Demonstration**
- **Advanced AI Architecture** - Showcases enterprise-level multi-agent system design
- **Production-Ready Code** - Modular, configurable, and maintainable codebase
- **Full-Stack Implementation** - From data processing to user interface

### **💼 Professional Value**
- **Portfolio Showcase** - Demonstrates practical AI engineering expertise
- **Interview Ready** - Complete project with documentation and testing
- **Industry Relevant** - Uses current best practices and modern frameworks

### **🔬 Learning Outcomes**
- **Multi-Agent Systems** - Understanding of agent orchestration and tool routing
- **RAG Implementation** - Hands-on experience with vector databases and semantic search
- **System Integration** - Combining multiple AI capabilities into unified experience

---

## 🤝 Contributing

This is a **personal portfolio project** designed to showcase AI engineering capabilities. While not accepting external contributions, the codebase serves as a reference implementation for building similar systems.

### **For Learning & Inspiration**
- ⭐ **Star this repository** if you find it helpful
- 🍴 **Fork it** to create your own version
- 📧 **Reach out** for questions or discussions about the implementation

---

## 🔗 Connect & Learn More

- **🎯 Portfolio**: [GitHub Profile](https://github.com/rbbishtji236)
- **💼 LinkedIn**: [LinkedIn Profile](https://www.linkedin.com/in/rohitbisht2360)



---

<div align="center">

**🌟 Crafted with passion for AI engineering and system architecture 🌟**

*This project represents my journey in building sophisticated AI systems and demonstrates practical expertise in modern AI frameworks and engineering practices.*

</div>

---

## 🚀 What's Next?

### **Planned Enhancements**
- **🔧 Advanced Tool Integration** - Adding more specialized agents
- **📈 Performance Optimization** - Query response time improvements
- **🌐 Multi-language Support** - Expanding language capabilities
- **📊 Analytics Dashboard** - Usage metrics and system monitoring