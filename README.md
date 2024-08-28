# Cold Emailer

Cold Emailer is a web application that generates personalized cold emails for students to send to professors based on their research interests.

## Features

- Scrapes professor data from universities
- Stores professor information in a vector database for efficient searching
- Generates personalized cold emails using AI
- Web interface for user input and email generation

## Installation

1. Clone the repository:
   ```
   git clone 
   cd cold-emailer
   ```

2. Create a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory and add the following:
   ```
   OPENAI_API_KEY=your_openai_api_key
   GROQ_API_KEY=your_groq_api_key
   ```

## Usage

1. Start the FastAPI server:
   ```
   uvicorn src.app:app --reload
   ```
2. CD into the cold-emailer directory

3. Open a web browser and navigate to `http://localhost:8000`

4. Fill out the form with your name, research interests, and achievements

5. Click "Generate Email" to receive a personalized cold email

## Project Structure
