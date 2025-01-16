import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from openai import OpenAI
import json

from langgraph.graph import StateGraph, END 

import streamlit as st

def main():
    st.title("Financial Performance Reporting Agent")

    task = st.text_input(
        "Enter the task:",
        "Analyze the financial performance of our company (MyAICo.AI) compared to competitors")
    
    competitors = st.text_area("Enter competitor names (one per line):").split("\n")

    max_revisions = st.number_input("Max Revisions", min_value=1, value=2)

    uploaded_file = st.file_uploader(
        "Upload a CSV file with the company's financial data",
        type=["csv"]
    )

    if st.button("Start Analysis") and uploaded_file is not None:
        # Read the uploaded CSV file
        csv_data = uploaded_file.getvalue().decode("utf-8")

        initial_state = {
            "task": task,
            "competitors" : [comp.strip() for comp in competitors if comp.strip()],
            "csv_file": csv_data,
            "max_revisions": max_revisions,
            "revision_number": 1,
        }
        thread = {"configurable": {"thread_id":"1"}}

        final_state = None
        for s in graph.stream(initial_state, thread):
            st.write(s)
            final_state = s 

        if final_state and "report" in final_state:
            st.subheader("Final Report")
            st.write(final_state["report"])


if __name__ == "__main__":
    main()