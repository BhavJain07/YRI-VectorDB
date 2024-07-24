The Cold Emailer tool is designed to generate personalized cold emails for students to send to professors based on their research interests. Here's a breakdown of its functionality and components:
AI Components:
OpenAI API: Used for generating professor suggestions based on user interests.
Groq API: Used for generating the actual cold email content.
Vector Database (VectorDB):
Purpose: To store and efficiently search for professors based on their research interests.
Implementation: Uses the FAISS library for similarity search.
Functionality:
Stores professor information along with embeddings of their research interests.
Allows for quick similarity searches to find professors with matching interests.
Main Workflow:
a. Scrape professor data (if not already in the VectorDB).
b. Get user input (name, interests, achievements).
c. Use the VectorDB to find similar professors based on the user's interests.
d. Generate a cold email for the top matching professor.
Key Components:
ProfessorScraper: Scrapes professor information from universities.
InterestEmbedder: Converts text interests into numerical embeddings.
ColdEmailer: Handles the generation of cold emails using AI.
VectorDB: Stores and searches professor data efficiently.
