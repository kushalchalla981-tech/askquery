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
### Natural Language to SQL - AI-Powered Database Query Generator

**Hackathon Project | National Level**

![QR Code](./presentation_qr.png)

**Scan to Try the App →**

</div>

---

## 🎯 What is AskQuery?

AskQuery is an AI-powered system that converts **natural language questions into SQL queries** automatically. Users can ask questions in plain English, and the system generates and executes the corresponding SQL query against a database.

### Example:
| Natural Language | Generated SQL |
|----------------|---------------|
| "Find all customers from California" | `SELECT * FROM customers WHERE state = 'California'` |
| "Show total revenue per product" | `SELECT p.name, SUM(o.total_amount) FROM products p JOIN orders o...` |

---

## 🚀 Features

- **🤖 LLM-Powered**: Uses Meta's Llama-3.2 for intelligent SQL generation
- **🔒 Secure Sandbox**: Read-only SQL execution with multiple security layers
- **📊 Execution-Based Grading**: Tiered rewards (0.0-1.0) based on query accuracy
- **📈 18 Benchmark Tasks**: Easy, Medium, and Hard difficulty levels
- **☁️ HuggingFace Spaces**: Live demo deployed at huggingface.co/spaces/kushal981/askquery

---

## 🏗️ Technical Architecture

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────────┐
│   User Query    │────▶│   Llama-3.2  │────▶│   SQL Parser    │
│ "Find orders..." │     │  (LLM)      │     │ (SQLGlot)       │
└─────────────────┘     └──────────────┘     └────────┬────────┘
                                                  │
                                                  ▼
                                          ┌─────────────────┐
                                          │   SQLite DB      │
                                          │ (Read-Only)     │
                                          └─────────────────┘
```

### Tech Stack:
- **Language Model**: Meta Llama-3.2-1B-Instruct
- **Framework**: OpenAI-compatible API via HuggingFace Inference
- **Database**: SQLite with SQLGlot validation
- **Deployment**: HuggingFace Spaces + Docker

---

## 💻 Implementation

### Action Space
```python
SQLAction(sql_query: str)  # Agent provides SQL query
```

### Observation Space
```python
SQLObservation(
    question: str,        # Natural language question
    schema_info: str,     # Database schema
    feedback: str,        # Execution result
    reward: float         # Score (0.0-1.0)
)
```

---

## 📊 Performance

| Difficulty | Score |
|------------|-------|
| Easy | ~0.80 |
| Medium | ~0.50 |
| Hard | ~0.30 |
| **Overall** | **~0.53** |

---

## 🔧 Setup

### Quick Start
```bash
# Clone the repo
git clone https://github.com/kushalchalla981-tech/askquery.git
cd askquery

# Install dependencies
pip install -e .

# Run inference
python inference.py
```

### Docker
```bash
docker build -t askquery .
docker run -p 7860:7860 askquery
```

---

## 🎓 Learning Outcomes

1. **LLM Integration**: Learned to integrate open-source LLMs with custom APIs
2. **SQL Security**: Implemented multi-layer SQL injection protection
3. **RL Environment**: Built OpenEnv-compatible reinforcement learning environment
4. **Cloud Deployment**: Deployed on HuggingFace Spaces

---

## 🔮 Future Improvements

- [ ] Use larger model (Llama-3.2-3B) for better accuracy
- [ ] Add support for JOINs and subqueries
- [ ] Implement prompt engineering for complex queries
- [ ] Add multi-database support (PostgreSQL, MySQL)
- [ ] Fine-tune model on SQL dataset

---

## 👥 Team

- **Kushal Challa** - @kushalchalla981-tech

---

## � links

- **Live Demo**: [huggingface.co/spaces/kushal981/askquery](https://huggingface.co/spaces/kushal981/askquery)
- **GitHub**: [github.com/kushalchalla981-tech/askquery](https://github.com/kushalchalla981-tech/askquery)

---

<div align="center">

**Made with ❤️ for the Hackathon**

</div>