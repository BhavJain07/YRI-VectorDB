# %% [markdown]
# # Model Training Notebook

# %%
import sys
sys.path.append('..')

from src.models.fine_tuned_embedder import FineTunedEmbedder
from src.models.fine_tuned_email_generator import FineTunedEmailGenerator
import json
import pandas as pd
from sklearn.model_selection import train_test_split

# %%
# Load and prepare data for embedder fine-tuning
with open('../data/professors/Stanford University.json', 'r') as f:
    professors = json.load(f)

interests = [(' '.join(p['interests']), p['name']) for p in professors]
train_data, test_data = train_test_split(interests, test_size=0.2, random_state=42)

# %%
# Fine-tune embedder
embedder = FineTunedEmbedder()
embedder.fine_tune(train_data, epochs=5)
embedder.save_model('../models/fine_tuned_embedder')

# %%
# Prepare data for email generator fine-tuning
# This would typically involve curated email examples
# For demonstration, we'll use placeholder data
email_examples = [
    {"input": "Professor: AI expert, User: ML student", "output": "Dear Professor,\n\nI am writing to express my interest..."},
    # Add more examples here
]

# In practice, you would fine-tune the email generator using these examples
# This might involve using OpenAI's fine-tuning API or a custom approach
# generator = FineTunedEmailGenerator()
# generator.fine_tune(email_examples)

# %%
# Test the fine-tuned models
test_embedder = FineTunedEmbedder.load_model('../models/fine_tuned_embedder')
test_embedding = test_embedder.embed("Machine Learning Natural Language Processing")
print(f"Test embedding shape: {test_embedding.shape}")

# Test email generator (using the non-fine-tuned version for demonstration)
generator = FineTunedEmailGenerator()
test_email = generator.generate_email(
    {"name": "Dr. Smith", "interests": ["AI", "ML"]},
    {"name": "John Doe", "interests": "Machine Learning"}
)
print(f"Generated email:\n{test_email}")