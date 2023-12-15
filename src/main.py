# This is a sample Python script.
# from datetime import datetime
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from collections import Counter
from datetime import date
from pathlib import Path

from Experimenter import Experimenter, DatasetInputType
import re


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

core_path = Path(__file__).parent.resolve() / "../data/"
print(core_path)

validation_path = Path(__file__).parent.resolve() / "../data/validation-data/"
print(validation_path)

paper_directory = str(core_path) + "/"
paper_directory = str(core_path) + "/compressed_view/"

testPlot = Experimenter(paper_directory, "CHI 2023 papers")

# First run the code with this uncommented. Then comment the code, and run testPlot.load_compressed_view()
# testPlot.load_all_original_papers_data() # load the raw info from the website
testPlot.load_compressed_view() # After we have actually loaded all the raw data from html, it is easy and quick to load comprresed
testPlot.calculate_papers_metrics(column_name="author_names")
testPlot.calculate_metrics_for_sessions(column_name="sessions")
testPlot.calculate_metrics_sections(column_name="sections")
testPlot.calculate_metrics_references(column_name="references")

# Extract most used sentences in all papers and all sections (you can set the minimum length)
# testPlot.extract_sentences(column_name="nothing")
# testPlot.extract_sentences(column_name="nothing", minimum_length=3)
# testPlot.extract_sentences(column_name="nothing", minimum_length=6)

# testPlot.extract_sentences_per_paper(column_name="not important")
# testPlot.extract_sentences_per_paper(column_name="not important", minimum_length=3)
# testPlot.extract_sentences_per_paper(column_name="not important", minimum_length=6)

# testPlot.search_sentences_per_paper(sentences_to_search=["contribution", "three research questions",
# "research question", "our knowledge"], minimum_length=3, top_k=10)
# testPlot.search_sentences_per_paper(sentences_to_search=["contribution", "three research questions",
# "research question", "our knowledge"], minimum_length=6, top_k=10)
# testPlot.search_sentences_per_paper(sentences_to_search=["contribution", "three research questions",
# "research question", "our knowledge"], minimum_length=9, top_k=10)

# testPlot.calculate_ngram_unique(column_name="no_matter", ngram=10, all_ngrams_until=True, top_k=5)
# testPlot.calculate_ngram(column_name="intro", ngram=10, top_k=5)

# Uncomment to create the expected dataset used in the paper for alt.chi
testPlot.create_limited_dataset_text_references(DatasetInputType.NO_REFERENCES_SECTION_PARTS, token_limit=2048,
                                                section_token_limit=2048) # Create a Dataset

# df = df[:k]