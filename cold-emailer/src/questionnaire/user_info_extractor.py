from typing import Dict

class UserInfoExtractor:
    def __init__(self):
        self.questions = [
            ("name", "What is your full name?"),
            ("education", "What is your highest level of education and field of study?"),
            ("interests", "What are your main research interests? (Comma-separated)"),
            ("reason_for_contact", "What is your primary reason for contacting professors?"),
            ("achievements", "List any relevant academic achievements or experiences:"),
            ("target_degree", "What degree program are you interested in pursuing?"),
            ("preferred_start_date", "When do you hope to start your studies?"),
            ("additional_info", "Is there any additional information you'd like to share?")
        ]

    def extract_user_info(self) -> Dict[str, str]:
        user_info = {}
        print("Please answer the following questions:")
        for key, question in self.questions:
            user_info[key] = input(f"{question}\n").strip()
        return user_info

if __name__ == "__main__":
    extractor = UserInfoExtractor()
    user_info = extractor.extract_user_info()
    print("\nCollected User Information:")
    for key, value in user_info.items():
        print(f"{key}: {value}")