import pandas as pd
import matplotlib.pyplot as plt

# Read the Excel files
coordinates_data = pd.read_excel(r'C:\Users\bzwil\OneDrive\Desktop\OBSCURATION ALGORITHM\DataObscuration [XJubier].xlsx')
xjubier_data = pd.read_excel(r'C:\Users\bzwil\OneDrive\Desktop\OBSCURATION ALGORITHM\WebScrapedData [XJubier].xlsx')

# Plotting the obscuration data
plt.figure(figsize=(10, 6))

# Plotting coordinates_data
plt.plot(coordinates_data['MAX_OBSCURATION'], label='Coordinates Data')

# Plotting xjubier_data
plt.plot(xjubier_data['MAX_OBSCURATION'], label='XJubier Data')

# Adding labels and title
plt.xlabel('')
plt.ylabel('Obscuration (%)')
plt.title('Comparison of Obscuration Data')
plt.legend()
plt.grid(True)
plt.xticks([])
plt.show()