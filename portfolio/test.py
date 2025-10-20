import pandas as pd

df = pd.DataFrame({
    'country': ['Italy', 'Italy', 'France', 'France', 'Spain', 'Spain'],
    'points': [90, 88, 85, 87, 92, 91]
})

print(df.groupby('country').head(1))