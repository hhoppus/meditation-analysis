# SCATTERPLOT--MEDITATION SESSION VS QUALITY, INCLUDING CORRELATION COEFFICIENT 

import matplotlib.pyplot as plt   
import numpy as np                
from utils import load_meditation_data  

# Get the data
df = load_meditation_data()

# Calculate correlation coefficient
correlation = df['duration_minutes'].corr(df['quality_rating'])
     
# Create scatter plot with correlation info in title
plt.figure(figsize=(10, 6))
plt.scatter(df['duration_minutes'], df['quality_rating'])
plt.xlabel('Duration (minutes)')  
plt.ylabel('Quality Rating')      
plt.title(f'Meditation Duration vs Quality (r = {correlation:.3f})')    
    
# Add trend line
z = np.polyfit(df['duration_minutes'], df['quality_rating'], 1)   
p = np.poly1d(z)    
plt.plot(df['duration_minutes'], p(df['duration_minutes']), "r--")   
plt.show()



# DATASET STATS:

# Average session length
avg_duration = df['duration_minutes'].mean()
print(f"Average session length: {avg_duration:.1f} minutes")

# Distribution of quality ratings
quality_dist = df['quality_rating'].value_counts().sort_index()
print("\nQuality rating distribution:")
for rating, count in quality_dist.items():
    print(f"Rating {rating}: {count} sessions ({count/len(df)*100:.1f}%)")

# Percentage with nimittas
nimitta_pct = (df['nimittas'].sum() / len(df)) * 100
print(f"\nSessions with nimittas: {nimitta_pct:.1f}%")

