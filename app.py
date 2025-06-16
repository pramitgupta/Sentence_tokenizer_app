import streamlit as st
import pandas as pd
import nltk
import io

from nltk.tokenize import sent_tokenize

# Download necessary NLTK data
nltk.download('punkt')

st.title("Sentence Filter App")

# Upload text document
text_file = st.file_uploader("Upload a text document", type=["txt"])
wordlist_file = st.file_uploader("Upload a wordlist (one word per line)", type=["txt"])

if text_file and wordlist_file:
    # Read and decode text file
    text = text_file.read().decode('utf-8')
    sentences = sent_tokenize(text)

    # Read wordlist and clean it
    wordlist = wordlist_file.read().decode('utf-8').splitlines()
    wordlist = [word.strip().lower() for word in wordlist if word.strip()]

    # Filter sentences
    matched_sentences = []
    for i, sent in enumerate(sentences):
        sent_lower = sent.lower()
        if any(word in sent_lower for word in wordlist):
            matched_sentences.append((i + 1, sent))

    # Create DataFrame
    df = pd.DataFrame(matched_sentences, columns=["Index", "Sentence"])

    # Show results
    st.subheader("Filtered Sentences")
    st.dataframe(df)

    # Option to download results
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name='filtered_sentences.csv',
        mime='text/csv',
    )
