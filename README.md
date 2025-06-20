# Aplikasi Parsing Kalimat Baku Berbahasa Indonesia

This repository contains an application designed for parsing standard Indonesian sentences. It leverages **Context-Free Grammar (CFG)**, **Chomsky Normal Form (CNF)**, and the **Cocke-Younger-Kasami (CYK) algorithm** to analyze sentence structure according to the General Guidelines for Indonesian Spelling (PUEBI) and the Fourth Edition of the Standard Indonesian Grammar.

The application aims to provide a deeper understanding of Indonesian grammatical structure and enhance the effectiveness and accuracy of Natural Language Processing (NLP) tasks for the Indonesian language.

## Features

* **Syntactic Parsing**: Analyzes input sentences to determine their grammatical structure.
* **Validity Check**: Determines if a sentence adheres to the defined grammatical rules, indicating whether it is "VALID" or "TIDAK VALID" (not valid).
* **Triangular Table Display**: Visualizes the parsing process through a triangular table, showing the non-terminal symbols generated at each step of the CYK algorithm.
* **Parse Tree Generation**: Generates a parse tree to visually represent the hierarchical structure of a valid sentence.

## Technologies Used

* **Python**: The core programming language.
* **Streamlit**: Used for building the interactive web user interface.
* **Graphviz**: Utilized for rendering the parse trees.

## Prerequisites

Before running the application, ensure you have the following installed:

* Python 3.x
* pip (Python package installer)

## Installation

1.  **Clone the repository or download the files**:
    Ensure `app.py` and `set_of_production.txt` are in the same directory.

2.  **Install dependencies**:
    Open your terminal or command prompt and navigate to the project directory. Then, run the following command:

    ```bash
    pip install streamlit graphviz
    ```

## How to Run

1.  **Navigate to the project directory** in your terminal or command prompt.
2.  **Run the Streamlit application**:

    ```bash
    streamlit run app.py
    ```

3.  The application will open in your default web browser (usually at `http://localhost:8501`).
4.  **Enter a sentence** in the provided input field and click the "Parse" button to see the results.

## Project Structure

* `app.py`: The main Python script that implements the CYK algorithm and the Streamlit web interface.
* `set_of_production.txt`: Contains the Context-Free Grammar (CFG) production rules (vocabulary and grammar definitions) used by the parsing application.
* `D1_RevisiFinalPrject_TBO_Parsing Kalimat Baku Kalimat Bahasa Indonesia.pdf`: The project report detailing the theoretical background, design, implementation, and experimental results of the application.
