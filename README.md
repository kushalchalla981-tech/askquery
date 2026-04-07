---
title: askquery
emoji: 🗄️
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
---

<div align="center">

# 🗄️ AskQuery
### Democratizing Data Access through Natural Language

**National Level Hackathon Project**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-huggingface-blue)](https://huggingface.co/spaces/kushal981/askquery)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

**Transform plain English questions into SQL queries instantly**

👉 [View Presentation](https://prezi.com/view/p7kZWtR0K70SdCzu3kJ8/)

</div>

---

## 🎯 Project Overview

AskQuery is an AI-powered system that converts **natural language questions into SQL queries**, democratizing database access for non-technical users.

### The Problem
> "90% of enterprise data is stored in databases, but only 5% of employees know SQL"

### Our Solution
AskQuery bridges the gap between human language and database queries, enabling anyone to interact with databases without writing SQL.

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🤖 **AI-Powered** | Uses Meta's Llama-3.2 for intelligent query generation |
| 🔒 **Secure** | Multi-layer SQL injection protection |
| 📊 **Accurate** | Execution-based grading with semantic understanding |
| ⚡ **Fast** | Sub-second query generation |
| ☁️ **Deployed** | Live on HuggingFace Spaces |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AskQuery Pipeline                    │
├─────────────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────┐    ┌──────────────┐    ┌─────────┐  │
│  │   User     │    │  Llama     │    │ SQL     │  │
│  │ Question  │───▶│   3.2    │───▶│ Parse   │  │
│  │           │    │  (LLM)    │    │ & Exec │  │
│  └──────────────┘    └──────────────┘    └─────────┘  │
│         │                                      │         │
│         │           ┌──────────────┐          │         │
│         └─────────▶│  SQLite DB   │◀─────────┘         │
│                    │ (Read-Only) │                   │
│                    └──────────────┘                   │
└──────────────────────────────────────────────────────┘
```

### Technology Stack

- **Language Model**: Meta Llama-3.2-1B-Instruct
- **Database**: SQLite with SQLGlot validation
- **Deployment**: HuggingFace Spaces + Docker
- **API**: OpenAI-compatible interface

---

## 💡 Innovation

1. **No-Code Database Access** - Anyone can query databases without SQL knowledge
2. **Secure Sandbox** - Read-only execution prevents data corruption
3. **Execution-Based Grading** - Rewards semantically correct queries
4. **Open Source** - Free to use and modify

---

## 📊 Results

| Metric | Score |
|--------|-------|
| Easy Queries | **80%** |
| Medium Queries | **50%** |
| Hard Queries | **30%** |
| **Average** | **53%** |

---

## 🎓 Learning Outcomes

- ✅ Large Language Model integration
- ✅ SQL security best practices
- ✅ Reinforcement learning environment design
- ✅ Cloud deployment on HuggingFace Spaces

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/kushalchalla981-tech/askquery.git
cd askquery

# Install dependencies
pip install -e .

# Run the application
python inference.py
```

### Environment Variables

| Variable | Description | Default |
|----------|------------|---------|
| `HF_TOKEN` | HuggingFace token | Required |
| `MODEL_NAME` | Model to use | Llama-3.2-1B-Instruct |
| `API_BASE_URL` | Inference endpoint | HuggingFace |

---

## 🔮 Future Scope

- [ ] Support for PostgreSQL & MySQL
- [ ] Fine-tuned SQL generation model
- [ ] Multi-table JOIN understanding
- [ ] Complex subquery support
- [ ] Voice-based query input

---

## 👥 Team

| Role | Name |
|------|------|
| Lead Developer | Kushal Challa |
| Lead Designer | Lingaraj Dyavakkalavar |
| Lead Coder | Manya S |
| GitHub | [@kushalchalla981-tech](https://github.com/kushalchalla981-tech) |

---

## 📚 Documentation

- **Live Demo**: [huggingface.co/spaces/kushal981/askquery](https://huggingface.co/spaces/kushal981/askquery)
- **Presentation**: [View Prezi](https://prezi.com/view/p7kZWtR0K70SdCzu3kJ8/)
- **Source Code**: [github.com/kushalchalla981-tech/askquery](https://github.com/kushalchalla981-tech/askquery)

---

<div align="center">

**🗄️ AskQuery - Making Data Accessible to Everyone**

*Built with ❤️ for the National Level Hackathon*

</div>