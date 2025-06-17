import streamlit as st
import pandas as pd
import nltk

from nltk.tokenize import sent_tokenize

# Download necessary tokenizer
nltk.download('punkt')

st.title("CSV Column Sentence Filter App")

# Upload files
csv_file = st.file_uploader("Upload a CSV file", type=["csv"])
wordlist_file = st.file_uploader("Upload a wordlist (one word per line)", type=["txt"])

if csv_file and wordlist_file:
    df = pd.read_csv(csv_file)
    st.subheader("Select the column to process")

    selected_col = st.selectbox("Choose a column containing text", df.columns)

    if selected_col:
        # Clean wordlist
        wordlist = wordlist_file.read().decode('utf-8').splitlines()
        wordlist = [word.strip().lower() for word in wordlist if word.strip()]

        matched_rows = []
        total_sentences = 0
        filtered_sentences = 0

        # Iterate using correct row index
        for true_idx, row in df.iterrows():
            text = row[selected_col]
            if pd.notna(text):
                sentences = sent_tokenize(str(text))
                total_sentences += len(sentences)

                for sent in sentences:
                    if any(word in sent.lower() for word in wordlist):
                        matched_rows.append((true_idx, sent))
                        filtered_sentences += 1

        # Show counts
        st.markdown(f"**Total sentences in column:** {total_sentences}")
        st.markdown(f"**Filtered sentences matched:** {filtered_sentences}")

        # Output
        result_df = pd.DataFrame(matched_rows, columns=["Row Index", "Matched Sentence"])
        st.subheader("Filtered Sentences")
        st.dataframe(result_df)

        # Download
        csv_output = result_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Filtered Sentences as CSV",
            data=csv_output,
            file_name='filtered_sentences_from_csv.csv',
            mime='text/csv',
        )
