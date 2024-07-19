# %% [markdown]
# # Data Exploration Notebook

# %%
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

%matplotlib inline

# %%
# Load professor data
with open('../data/professors/Stanford University.json', 'r') as f:
    professors = json.load(f)

df = pd.DataFrame(professors)

# %%
# Display basic statistics
print(df.describe())
print(df.info())

# %%
# Visualize distribution of interests
interests = [interest for sublist in df['interests'] for interest in sublist]
interest_counts = pd.Series(interests).value_counts()

plt.figure(figsize=(12, 6))
sns.barplot(x=interest_counts.index[:20], y=interest_counts.values[:20])
plt.title('Top 20 Research Interests')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# %%
# Analyze publication counts
df['publication_count'] = df['publications'].apply(len)
plt.figure(figsize=(10, 6))
sns.histplot(df['publication_count'], kde=True)
plt.title('Distribution of Publication Counts')
plt.xlabel('Number of Publications')
plt.show()