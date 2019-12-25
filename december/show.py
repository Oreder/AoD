import pandas as pd
import plotly.graph_objects as go
import numpy as np

fileName = './io/io-2.csv'

df = pd.read_csv(fileName)
iters = np.array(range(0, len(df.values)))

# fileName = './io/io-1.csv'
# df1 = pd.read_csv(fileName)

# fileName = './io/io-2.csv'
# df2 = pd.read_csv(fileName)

# fileName = './io/io-3.csv'
# df3 = pd.read_csv(fileName)

# iters = np.array(range(0, len(df1.values)))

fig = go.Figure()

fig.add_trace(go.Scatter(x=iters, y=df['Approximate'], name='Приближенное'))
fig.add_trace(go.Scatter(x=iters, y=df['Exact'], name='Точное'))

# fig.add_trace(go.Scatter(x=iters, y=df1['RelError'], name='divF'))
# fig.add_trace(go.Scatter(x=iters, y=df2['RelError'], name='U'))
# fig.add_trace(go.Scatter(x=iters, y=df3['RelError'], name='dU'))


fig.update_layout(title='Расчёт приближенного и точного решения',
                   plot_bgcolor='rgb(230, 230,230)',
                   showlegend=True)

fig.show()