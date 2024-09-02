# faq-bot

Sample repo for an NLP chatbot to answer questions given a knowledgebase using RAG and OpenAI function calling.

## Setup

1. Setup OpenAI project and project key and `model_name` in `.env`
2. Setup `.env-qdrant-compose` and `env-postgres-compose`
3. Build docker image for the repository
4. Run `docker compose up`