# ReflectCT

ReflectCT is an LLM-powered system designed to help students reflect on their computational thinking (CT) errors through step-by-step guidance, error tagging, and collaborative analysis.

---

## Quick Start

To get started, first clone the repository and set up the environment:

```bash
git clone https://github.com/YimeiZhang18/ReflectCT.git
cd ReflectCT
python -m venv .venv
source .venv/bin/activate 
pip install -r requirements.txt
```


## Configuration

Before running, please add your personal OpenAI API key.

1. Create a `.env` file in your project:

 ```bash
 touch .env
 ```

2. Add your key inside  `.env` file:
   
  
```markdown

OPENAI_API_KEY=YOUR_API_KEY
