## VitaAI: Medical Assistant 

**VitaAI** is an AI-powered medical assistant designed to provide accurate health-related information using **Retrieval-Augmented Generation (RAG)**. It leverages **LLMs (Groq)**, **LangChain**, and **Pinecone Vector Database** to ensure contextual and medically relevant responses.

---

# Key Features
- **Contextual Awareness:** Uses RAG to fetch data from trusted medical PDFs/documents.
- **High Speed:** Powered by Groq/GPT for lightning-fast responses.
- **Persistent Memory:** Vector indexing with Pinecone for efficient data retrieval.
- **Production Ready:** Scalable deployment using Docker on AWS.
- **CI/CD Pipeline:** Fully automated deployment using GitHub Actions.

---

# Project Architecture
```text
User Query ➔ Flask App ➔ LangChain (RAG) ➔ Pinecone (Vector Search)
                                 ⬇
                          Groq/OpenAI (LLM)
                                 ⬇
                          Structured Response
```

```bash
# Clone the Repository
git clone https://github.com/harshcseai/VitaAI-medical-assistant.git
cd VitaAI-medical-assistant
```

```bash
# Virtual Environment Using Conda
conda create -n vitaai python=3.10 -y
conda activate vitaai
```

```bash
# Install the requirements
pip install -r requirements.txt
```

```ini
# Create a Virtual Environment
PINECONE_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
GROQ_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

```bash
# Run this to store embeddings to Pinecone
python store_index.py
```

```bash
# Finally run the application
python app.py
```

# TechStack
- Python
- LangChain
- Flask
- Groq
- Pinecone



# AWS-CICD-Deployment-with-Github-Actions

## 1. Login to AWS console.

## 2. Create IAM user for deployment

	#with specific access

	1. EC2 access : virtual machine

	2. ECR: Elastic Container registry to save your docker image in aws


	# Description: 

	1. Build docker image of the source code

	2. Push your docker image to ECR

	3. Launch Your EC2 

	4. Pull Your image from ECR in EC2

	5. Lauch your docker image in EC2


	
## 3. Create ECR repo to store/save docker image
    - URL: 704593925871.dkr.ecr.ap-south-1.amazonaws.com/vitaai
	
## 4. Create EC2 machine (Ubuntu) 

## 5. Open EC2 and Install docker in EC2 Machine:
	
	
# 6. Configure EC2 as self-hosted runner:
    Go to Settings > Actions > Runners > New self-hosted runner, select Linux, and run the provided commands on your EC2 instance.


# 7. GitHub Secrets Configuration
    Add the following secrets in Settings > Secrets and variables > Actions:

   - AWS_ACCESS_KEY_ID
   - AWS_SECRET_ACCESS_KEY
   - AWS_DEFAULT_REGION
   - ECR_REPO
   - PINECONE_API_KEY
   - GROQ_API_KEY
