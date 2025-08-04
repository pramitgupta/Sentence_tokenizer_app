import streamlit as st
import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize

nltk.download('punkt')

st.title("Tokenize and Filter 'extr_sents_pr' by prim_key (≥ 8 words)")

# Upload CSV
csv_file = st.file_uploader("Upload a CSV file", type=["csv"])

if csv_file:
    df = pd.read_csv(csv_file)

    if "prim_key" in df.columns and "extr_sents_pr" in df.columns:
        results = []

        for _, row in df.iterrows():
            prim_key = row["prim_key"]
            text = row["extr_sents_pr"]

            if pd.notna(text):
                sentences = sent_tokenize(str(text))
                for sent in sentences:
                    word_count = len(sent.split())
                    if word_count >= 8:
                        results.append((prim_key, sent))

        # Display result
        result_df = pd.DataFrame(results, columns=["prim_key", "Tokenized Sentence"])
        st.subheader("Tokenized Sentences (≥ 5 words)")
        st.dataframe(result_df)

        # Download option
        csv_output = result_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Filtered Sentences as CSV",
            data=csv_output,
            file_name="filtered_tokenized_extr_sents_pr.csv",
            mime="text/csv"
        )
    else:
        st.error("The CSV must contain both 'prim_key' and 'extr_sents_pr' columns.")

