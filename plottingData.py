import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_excel (r'D:\Faculty\GP\Graduation-Project-V2V\car2.xlsx')
locationx = pd.DataFrame(data, columns= ['locationx2'])
locationy = pd.DataFrame(data, columns= ['locationy2'])
data.plot(x ='locationx2',y=['locationy2'] ,kind='line')
plt.show()

