import streamlit as st
import pandas as pd
import nltk

from nltk.tokenize import sent_tokenize

# Ensure NLTK data is available
nltk.download('punkt')

st.title("CSV Column Sentence Filter App")

# Upload CSV and wordlist
csv_file = st.file_uploader("Upload a CSV file", type=["csv"])
wordlist_file = st.file_uploader("Upload a wordlist (one word per line)", type=["txt"])

if csv_file and wordlist_file:
    # Read CSV
    df = pd.read_csv(csv_file)
    st.subheader("Select the column to process")

    # Selectbox for column
    selected_col = st.selectbox("Choose a column containing text", df.columns)

    if selected_col:
        # Read and clean wordlist
        wordlist = wordlist_file.read().decode('utf-8').splitlines()
        wordlist = [word.strip().lower() for word in wordlist if word.strip()]

        matched_rows = []
        total_sentences = 0
        filtered_sentences = 0

        # Process each row
        for idx, cell in df[selected_col].dropna().items():
            sentences = sent_tokenize(str(cell))
            total_sentences += len(sentences)

            for sent in sentences:
                sent_lower = sent.lower()
                if any(word in sent_lower for word in wordlist):
                    matched_rows.append((idx, sent))
                    filtered_sentences += 1

        # Display counts
        st.markdown(f"**Total sentences in column:** {total_sentences}")
        st.markdown(f"**Filtered sentences matched:** {filtered_sentences}")

        # Create output DataFrame
        result_df = pd.DataFrame(matched_rows, columns=["Row Index", "Matched Sentence"])

        st.subheader("Filtered Sentences")
        st.dataframe(result_df)

        # Download button
        csv_output = result_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Filtered Sentences as CSV",
            data=csv_output,
            file_name='filtered_sentences_from_csv.csv',
            mime='text/csv',
        )
