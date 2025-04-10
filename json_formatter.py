import streamlit as st
import json

# Define a function to format JSON nicely
def format_json(raw_json):
    try:
        parsed_json = json.loads(raw_json)
        formatted_json = json.dumps(parsed_json, indent=4)
        return formatted_json, parsed_json
    except json.JSONDecodeError:
        return "Invalid JSON provided.", {}

# Define a function to generate SQL extraction query for each array item with value example
def generate_sql_extract_example(json_data):
    sql_queries = []
    
    def generate_sql_for_dict(path, data):
        if isinstance(data, dict):
            for key, value in data.items():
                new_path = f"{path}.{key}" if path else key
                generate_sql_for_dict(new_path, value)
        elif isinstance(data, list):
            for i, item in enumerate(data):
                new_path = f"{path}[{i}]"
                generate_sql_for_dict(new_path, item)
        else:
            value_example = f"{data}"  # Example value extracted
            sql_queries.append(f"'$.{path}'  --  Value: {value_example}")
    
    generate_sql_for_dict("", json_data)
    
    return "\n".join(sql_queries)

# Set up the Streamlit app layout
st.set_page_config(page_title="JSON Formatter and SQL Extractor", layout="wide")

# Title of the app
st.title("JSON Formatter with SQL Extraction")

# Create a left-right column layout
col1, col2 = st.columns(2)

# Left Column: Input JSON box
with col1:
    st.markdown("<h3 style='text-align: center;'>Input JSON</h3>", unsafe_allow_html=True)
    input_json = st.text_area("", height=900, max_chars=5000, key="input_json")

# Automatically format the JSON as the user types or pastes
if input_json:
    formatted_json, parsed_json = format_json(input_json)
else:
    formatted_json = ""
    parsed_json = {}

# Right Column: Formatted JSON with syntax highlighting
with col2:
    st.markdown("<h3 style='text-align: center;'>Formatted JSON</h3>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)  # Add line break between header and box
    st.code(formatted_json, language="json", height=900)

# Add a copy to clipboard button for formatted JSON
if st.button('Copy to Clipboard'):
    st.text(formatted_json)  # Automatically copies last value in output area

# SQL Extraction: Example SQL for each array element with output value examples
if parsed_json:
    st.subheader("SQL Extraction Example")
    sql_example = generate_sql_extract_example(parsed_json)
    st.text_area("SQL Query to Extract Data:", sql_example, height=600, max_chars=5000, disabled=True)


