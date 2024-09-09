#!/bin/bash

# Get the latest .whl file
latest_whl=$(ls dist/yt_summaries-*-py3-none-any.whl | sort -V | tail -n 1)

# Extract the version from the .whl file name (assumes version follows the pattern yt_summaries-X.Y.Z)
whl_version=$(echo $latest_whl | sed -n 's/.*yt_summaries-\([0-9.]*\)-py3-none-any.whl/\1/p')

# Check if the package is already installed and get the installed version
installed_version=$(pip show yt_summaries | grep Version | awk '{print $2}')

# Compare the installed version with the .whl version
if [ "$installed_version" == "$whl_version" ]; then
    echo "🟢 The latest version ($installed_version) is already installed. Skipping installation."
else
    echo "🔴 Installing latest dist... ($whl_version)"
    pip install "$latest_whl"
    echo "🟢 Done!"
fi

# building the ES index from the default YT channel
python3 app/yt_rag/build_index.py

echo "Initilizing Grafana Dashboard"
python3 app/grafana/init.py

echo "Running Streamlit App"
streamlit run app/yt_rag/streamlit_app.py --server.port=8501 --server.address=0.0.0.0
