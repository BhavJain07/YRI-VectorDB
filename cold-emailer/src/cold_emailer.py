from openai import OpenAI
import sys

class ColdEmailer:
    def __init__(self, api_keys):
        try:
            print("Initializing OpenAI client...")
            self.client = OpenAI(api_key=api_keys['openai'])
            print("OpenAI client initialized successfully.")
        except Exception as e:
            print(f"Error initializing API client: {str(e)}")
            raise

    def generate_cold_email(self, name, prof_name, interest, achievements, publications):
        try:
            message = f"""
            Generate a cold email for a student named {name} to send to Professor {prof_name}.
            The student is interested in {interest} and has achieved {achievements}.
            The professor has published: {', '.join(publications[:3])}.
            """

            print("Generating email using OpenAI API...")
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates cold emails for students."},
                    {"role": "user", "content": message}
                ],
                max_tokens=300,
                n=1,
                temperature=0.7,
            )
            print("Email generated successfully.")
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating email: {str(e)}")
            raise

if __name__ == "__main__":
    from config import OPENAI_API_KEY
    
    api_keys = {
        'openai': OPENAI_API_KEY
    }
    
    try:
        emailer = ColdEmailer(api_keys)
        email = emailer.generate_cold_email(
            name="John Doe",
            prof_name="Dr. Smith",
            interest="Machine Learning",
            achievements="Published a paper on NLP",
            publications=["Title: AI Advances"]
        )
        print("Generated email:")
        print(email)
    except Exception as e:
        print(f"Error in main: {str(e)}")
        import traceback
        traceback.print_exc()