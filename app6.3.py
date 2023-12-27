import streamlit as st
import nltk
from nltk import CFG, ChartParser
from nltk.tree import Tree
from nltk.treeprettyprinter import TreePrettyPrinter

# Modify the cyk_parse function to return the complete chart
def cyk_parse(sentence, grammar):
    words = sentence.split()
    n = len(words)
    
    # Initialize the chart with empty sets
    chart = [[set() for _ in range(n - i)] for i in range(n)]

    # Fill in the diagonal of the chart with the possible non-terminals for each word
    for i in range(n):
        word = words[i]
        chart[0][i] = set(rule.lhs() for rule in grammar.productions(rhs=word))

    # CYK algorithm
    for length in range(2, n + 1):
        for start in range(n - length + 1):
            end = start + length
            for mid in range(start + 1, end):
                # Check all possible combinations of non-terminals
                for rule in grammar.productions():
                    if len(rule.rhs()) == 2:
                        left, right = rule.rhs()
                        if left in chart[mid - start - 1][start] and right in chart[end - mid - 1][mid]:
                            chart[length - 1][start].add(rule.lhs())

    # Return the complete chart
    return chart


# Modify the display_result function to visualize the parse tree
def display_result(chart):
    if chart[-1][0]:
        # Display the parse tree as a string
        parse_tree_string = '\n'.join([' '.join([str(nt) for nt in cell]) for cell in chart])
        st.success(f"Parse successful. Parse tree:\n{parse_tree_string}")
    else:
        # Display a message when parsing is not successful
        st.error("Parsing failed. Unable to generate a valid parse tree.")


# Main Streamlit App
def main():
    st.title("Aplikasi Syntactic Parsing dengan CYK dan Parse Tree")

    # Input kalimat dari pengguna
    sentence = st.text_input("Masukkan kalimat untuk diparse:")

    # Definisikan grammar (sesuaikan dengan kebutuhan Anda)
    cfg_grammar = """
    S -> NP VP
    NP -> Det N | 'I'
    VP -> V NP | 'am'
    Det -> 'an' | 'the'
    N -> 'elephant' | 'pajamas'
    V -> 'saw'
    """
    grammar = CFG.fromstring(cfg_grammar)

    # Parsing dan menampilkan parse tree
    if st.button("Parse"):
        chart = cyk_parse(sentence, grammar)
        display_result(chart)

if __name__ == "__main__":
    main()
