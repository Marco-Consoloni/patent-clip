import dash
from dash.exceptions import PreventUpdate
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
from sklearn.manifold import TSNE
import pickle
import os
from PIL import Image

'''
References
> https://stackoverflow.com/questions/30445198/displaying-image-on-point-hover-in-plotly
> https://www.tutorialspoint.com/how-to-display-an-image-on-hovering-over-a-point-in-python-plotly
'''

# Create dash app
app = dash.Dash(__name__)

def load_vectors(pickle_path):
   with open(pickle_path, "rb") as pkl_file:
      data = pickle.load(pkl_file)
      return data.get("vectors"), data.get("payloads")

def move_images(payloads, output_dir):
   for payload in payloads:
      source_path = payload[3]
      output_path = os.path.join(output_dir, os.path.basename(source_path))
      img = Image.open(source_path)
      # Reduce image size for better vizualization
      img.thumbnail((550, 550), Image.LANCZOS)  # use LANCZOS for high-quality downsampling
      img.save(output_path, quality=95, optimize=True)  # save image and adjust compression without losing quality
   print(f'All images have been successfully moved to: {output_dir}')

# Define database
db = "all"
#db = "A42B3-H02K19"

# 1. Use text and image embeddings separately
#pickle_img = "/home/fantoni/marco/patent-clip/docker/vectors/all-custom/all-images.pkl"
#pickle_text = "/home/fantoni/marco/patent-clip/docker/vectors/all-custom/all-text.pkl"
#pickle_text = "/home/fantoni/marco/patent-clip/docker/vectors/A42B3-H02K19-custom/A42B3-H02K19-text.pkl"
#pickle_img = "/home/fantoni/marco/patent-clip/docker/vectors/A42B3-H02K19-custom/A42B3-H02K19-images.pkl"
# Merging vectors and payloads
#vec_text, pld_text = load_vectors(pickle_text)
#vec_img, pld_img = load_vectors(pickle_img)
#vectors = np.concatenate((vec_text, vec_img), axis=0) 
#payloads = pld_text + pld_img 

# 2. Use joint embeddings
pickle_joint = "/home/fantoni/marco/patent-clip/docker/vectors/all-custom/all-joint.pkl"
vectors, payloads = load_vectors(pickle_joint)

# Move images in assets folder
output_dir = os.path.join("/home/fantoni/marco/patent-clip/tsne-vizualization/assets", db)
os.makedirs(output_dir, exist_ok=True)
move_images(payloads, output_dir) 

# Create metadata
metadata = {
    "doc_id":[payload[0] for payload in payloads],
    "cls": [payload[1] for payload in payloads],
    "text": [payload[2] for payload in payloads],
    "img_src": [f"/assets/{db}/{os.path.basename(payload[3])}" for payload in payloads],
    "collection_name": [payload[4] for payload in payloads]
}

# Apply t-SNE to reduce to 2D
X = np.vstack(vectors) # convert list of arrays to a numpy matrix
tsne = TSNE(n_components=2, random_state=1999)
X_embedded = tsne.fit_transform(X)

# Convert the result into a DataFrame for easier plotting
df = pd.DataFrame(X_embedded, columns=['x', 'y'])
df['cls'] = metadata["cls"]
df['doc_id'] = metadata["doc_id"]
df['text'] = metadata["text"]
df['img_src'] = metadata["img_src"]
df['collection_name'] = metadata["collection_name"]

# Plot using Plotly, with color by label or group
fig = px.scatter(df, x='x', y='y',
                 color='cls', 
                 symbol='collection_name',
                 title="t-SNE visualization",
                 custom_data=['doc_id', 'cls', 'text', 'img_src', 'collection_name'])

# Update layout and update traces
fig.update_layout(clickmode='event+select')
fig.update_traces(marker=dict(
                     size=15, # Set point size
                     line=dict(width=1), # Set point border width
                     opacity=0.7 # Set point transparency
                  ),
                  hovertemplate="<b>Class:</b> %{customdata[1]}<br>" +
                  "<b>Document ID:</b> %{customdata[0]}<br>" +
                  "<extra></extra>"  # This removes the secondary box
                  )

# Create app layout to show dash graph and metadata
app.layout = html.Div([
    html.Div([
        dcc.Graph(
            id="graph_interaction",
            figure=fig
        )
    ], style={'width': '100%', 'margin-bottom': '5px'}),
    html.Div([
        html.Div([
            html.Div(id='metadata', style={'marginTop': '20px', 'font-size': '22px'})
        ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}), 
        html.Div([
            html.Div([
                html.Img(id='image', src='', style={'max-width': '100%', 'height': 'auto'})
            ], style={'text-align': 'center'})
        ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'})
    ], style={'width': '100%'})
])

# Callback function to handle hover data and display image and metadata
@app.callback(
   [Output('image', 'src'),
    Output('metadata', 'children')],
   Input('graph_interaction', 'hoverData')
)

def display_metadata(hoverData):
   if hoverData:
      # Extract custom data from hoverData
      doc_id, cls, claim, image_src, collection_name = hoverData["points"][0]["customdata"]
      # Create a formatted string for metadata display
      metadata_text = f"**class**: {cls}\n\n**doc_id**: {doc_id}\n\n**claim**: {claim}\n\n**collection_name**: {collection_name}"
      return image_src, dcc.Markdown(metadata_text)
   else:
      raise PreventUpdate

if __name__ == '__main__':
   app.run_server(debug=True)
