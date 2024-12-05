# BOX PLOT--NIMITTAS AND SESSION DURATION

import matplotlib.pyplot as plt    #
import numpy as np              
from utils import load_meditation_data  

df = load_meditation_data()

plt.figure(figsize=(10, 6))
plt.boxplot([
   df[df['nimittas'] == False]['duration_minutes'],
   df[df['nimittas'] == True]['duration_minutes']
], labels=['No Nimittas', 'With Nimittas'])
plt.ylabel('Duration (minutes)')
plt.title('Meditation Duration by Presence of Nimittas')
plt.show()

 
