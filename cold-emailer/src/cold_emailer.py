from groq import Groq
from openai import OpenAI

class ColdEmailer:
    def __init__(self, api_keys):
        self.groq_client = Groq(api_key=api_keys.get('groq'))
        self.openai_client = OpenAI(api_key=api_keys.get('openai'))

    def generate_professor_suggestions(self, interests, vector_db, interest_embedder, k=5):
        interest_embedding = interest_embedder.embed(interests)
        similar_professors = vector_db.search(interest_embedding, k=k)
        return similar_professors

    def generate_cold_email(self, name, prof_name, interest, achievements, publications):
        message = f"""
        You will be given a person's full name delimited by triple backticks (```), the desired professor's name delimited by triple hashtags (###), the person's interest statement delimited \
        by triple ampersands (&&&), the person's achievements, delimited by triple carets (^^^), and list of overview of publications delimited by triple asterisks (***).

        Using the given information, write a persuasive and powerful cold email using the following template/outlines below, synthesizing them for a powerful cold email. \
         Phrases within square brackets [] or {{curly braces}} are meant to explain each part.

          Make sure the email follows roughly similar appeals to ethos, pathos, (and if applicable, logos). It should be sure to include the student's achivement along with some info that ties the professor's \
        work to the opportunity. If there is no achievments for the student, reword appropriately.

        The cold email should be persuasive, so remember not to \
        add any informationt hat could adversely affect the student's chances (such as begging for an opportunity, or suggesting \
        this is more about prestige and fame than actual research, even if it's the student's desire). For example, don't mention a student wants to research at an ivy-league university \
        or that a student wants to do research for their resume.

        Make sure to be concise in intentions, and be very specific about the \
        professor's work (like talk about more in technical and focusing on this a sizable amount of attention.)

        Output JUST the new cold email.

        Full Name: ```
        {name}
        ```

        Professor Name: ###
        {prof_name}
        ###

        Interest Statement: &&&
        {interest}
        &&&

        Achievements: ^^^
        {achievements}
        ^^^

        Publication Info: ***
        {publications}
        ***
        """

        completion = self.groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": message}],
            temperature=0.3,
            max_tokens=800
        )
        return completion.choices[0].message.content