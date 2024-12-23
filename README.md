# Chatbot Backend

This project implements a chatbot backend using Python with Retrieval-Augmented Generation (RAG). It integrates LangChain and HuggingFace models to generate intelligent responses based on provided data sources.

## Features
- Retrieval of relevant information from a GEM report and World Bank indicators.
- Generation of responses using HuggingFace models.
- REST API for backend integration.
- Streamlit-based UI for user interaction.
- Dockerized setup for easy deployment.

## Setup Instructions

### Prerequisites
1. Install Docker on your system: [Docker Installation Guide](https://docs.docker.com/get-docker/)
2. Clone this repository:
   ```bash
   git clone <repository-url>
   cd chatbot-backend
   ```

### Environment Variables
Ensure you have a `.env` file in the root directory with the following content:(https://huggingface.co/settings/tokens  --> to create access token and replace that with ur token on .env file)
```env
HF_API_TOKEN=your_huggingface_api_token
```

### Running with Docker
1. Build the Docker image:
   ```bash
   docker build -t chatbot-backend .
   ```

2. Run the Docker container:
   ```bash
   docker run -p 5000:5000 -p 8502:8502 chatbot-backend
   ```

### Accessing the Application
- **Streamlit UI**: Access the frontend at `http://0.0.0.0:8501/`




### Running Locally (Without Docker)
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the Flask backend:
   ```bash
   python app.py
   ```

3. Start the Streamlit frontend:
   ```bash
   streamlit run streamlit_app/main.py --server.port 8502
   ```


