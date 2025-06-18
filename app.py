import streamlit as st
import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize

nltk.download('punkt')

st.title("CSV Sentence Filter by Wordlist")

# Upload CSV and Wordlist
csv_file = st.file_uploader("Upload a CSV file", type=["csv"])
wordlist_file = st.file_uploader("Upload a wordlist (one word per line)", type=["txt"])

if csv_file and wordlist_file:
    df = pd.read_csv(csv_file)

    # Filter named columns only
    named_columns = [col for col in df.columns if not col.lower().startswith("unnamed")]

    # Dropdown for target column
    st.subheader("Select the column to process")
    selected_col = st.selectbox("Text column to process", [col for col in named_columns if col != "prim_key"])

    if selected_col and "prim_key" in df.columns:
        # Read wordlist
        wordlist = wordlist_file.read().decode('utf-8').splitlines()
        wordlist = [word.strip().lower() for word in wordlist if word.strip()]

        total_sentences = 0
        matched_sentences = 0
        results = []

        for _, row in df.iterrows():
            text = row[selected_col]
            prim_key = row["prim_key"]

            if pd.notna(text):
                sentences = sent_tokenize(str(text))
                total_sentences += len(sentences)

                for sent in sentences:
                    if any(word in sent.lower() for word in wordlist):
                        results.append((prim_key, sent))
                        matched_sentences += 1

        # Display stats
        st.markdown(f"**Total sentences processed:** {total_sentences}")
        st.markdown(f"**Matched sentences:** {matched_sentences}")

        # Display result table
        result_df = pd.DataFrame(results, columns=["prim_key", "Matched Sentence"])
        st.subheader("Filtered Sentences")
        st.dataframe(result_df)

        # Download option
        csv_output = result_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Filtered Sentences as CSV",
            data=csv_output,
            file_name="filtered_sentences.csv",
            mime="text/csv"
        )
