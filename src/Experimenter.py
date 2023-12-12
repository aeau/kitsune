from collections import Counter
from datetime import date
from locale import atoi

import re
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os as os
import os.path
from os import path
from numpy import genfromtxt
from os import listdir
import copy
import enum
import math
from enum import Enum
import matplotlib as mpl
import re
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.animation import FuncAnimation, PillowWriter
import matplotlib.animation as animation

from matplotlib.colors import from_levels_and_colors
from matplotlib.collections import LineCollection

from src.CollectedPapersGeneral import CollectedPapersGeneral
from src.Paper import Paper
from src.DatasetLLMPapers import *
import string


class DatasetInputType(Enum):
    NO_REFERENCES = 1
    NO_REFERENCES_SECTION_PARTS = 2
    REFERENCES = 3
    REFERENCES_SECTION_PARTS = 4

class Experimenter:

    def __init__(self, papers_directory, experiment_name="itiswhatitis"):
        print("experimentor")
        self.experiment_name = experiment_name
        self.papers_directory = papers_directory
        self.papers = {}
        self.compressed_papers = {}

        self.column_names = ["article-authors", "article-fullauthors", "article-headers", "article-sections", "article-ind-bib"]
        self.variable_names = ["author", "author_institution", "section_title", "section", "reference"]
        self.max_sections = 0
        self.max_sections_paper_name = ""

        self.collected_papers_general = CollectedPapersGeneral("chi23", self.max_sections)

    def get_csv_files(self, directory):
        filenames = listdir(directory)
        csv_files = [filename for filename in filenames if filename.endswith(".csv")]

        return csv_files

    def get_files(self, directory, extension : str):
        filenames = listdir(directory)
        files = [filename for filename in filenames if filename.endswith(extension) and not filename.startswith("~")]

        return files

    def extract_sessions(self, df):
        """Extract session name for the papers and their name
        Creates the Paper object with the correct session and the paper name
        Pre-process the session names to only keep the session name rather than including keywork: "SESSION:"
        """
        df_2 = df.replace(np.nan, "")
        session_data = df_2.index[[df_2["sessions-and-papers"].str.contains("SESSION:")]].values  # get all sessions
        session_data = list(session_data)
        current_index = 0

        while session_data:  # Iterate sessions to create papers within the session in order

            # Get index of session and session name
            current_index = session_data.pop(0)
            session_name = df_2.iloc[current_index]["sessions-and-papers"]
            session_name = session_name.split("SESSION: ")[1]

            # Get paper names
            paper_name = "lets get started"
            while "SESSION:" not in paper_name and paper_name != "":
                current_index = current_index + 1
                paper_name = df_2.iloc[current_index]["sessions-and-papers"]
                # print(paper_name)
                # print(type(paper_name))

                if paper_name not in self.papers:  # add the paper if it doesn't exist!
                    self.papers.update({paper_name: Paper(paper_name, session_name)})

                paper_name = df_2.iloc[current_index + 1]["sessions-and-papers"]

        print("DONE ITERATING FOR SESSIONS AND PAPER NAMES")
        return current_index + 1

    def extract_abstract(self, paper_name, data, data_index):
        """Check the pandas dataset for the abstract"""
        print(paper_name)
        abstract = data.iloc[data_index]["article-abstract"]
        self.papers.get(paper_name).add_abstract(abstract)

    def extract_value(self, paper_name, data, data_index, column_name, variable_name):
        """Depending on column name and variable name:
         We get data (value_name) from 'column_name' from the pandas dataset, and
         add the value to the particular key ('variable_name') within the paper's dictionary.

         Keyword arguments:
         paper_name -- key for the papers dictionary
         data -- particular pandas dataset
         data_index -- given the peculiarity of the webscraper, each row contain a different datapoint for the paper
         column_name -- What column should we take from the pandas dataset ('data')
         variable_name -- key in the dictionary within particular Paper object where we will add a new value!
         """
        df_2 = data.replace(np.nan, "")  # Replace all NaN values with empty strings (for easier iteration)
        value_name = "lets get started"
        current_sections = 0
        while value_name != "":  # we iterate the
            data_index = data_index + 1
            value_name = df_2.iloc[data_index][column_name]
            # print(paper_name)
            # print(type(paper_name))

            if value_name == "":
                break

            if paper_name in self.papers:
                self.papers[paper_name].add_value(value_name, variable_name)

            if variable_name == "section":
                current_sections = current_sections + 1

        if current_sections > self.max_sections:
            self.max_sections = current_sections
            self.max_sections_paper_name = paper_name

        return data_index - 1

    def load_all_original_papers_data(self):
        xlsx_files = self.get_files(self.papers_directory, ".xlsx")  # Get all excel files (for now CHI23)
        current_index = 0
        current_paper_number = 0
        max_papers_assessed = 20

        for file in xlsx_files:
            print(file)

            current_data = pd.read_excel(self.papers_directory + file)  # Get the pandas object

            current_index = 1 # We start from 1 because 0 is always -1 for the validation data we use
            current_index = self.extract_sessions(current_data)  # Extract the session data and pre-process
            print(current_index)
            print(current_data.iloc[[current_index]])
            print(current_data.iloc[[0]])
            print(len(current_data))

            while current_index + 1 < len(current_data):
                # current_paper_number = current_paper_number + 1
                # if current_paper_number > max_papers_assessed:
                #     break

                current_paper_name = current_data.iloc[current_index]["article-open"]
                # current_paper_name = current_paper_name.replace(" :", ":")
                self.extract_abstract(current_paper_name, current_data, current_index)

                variable_index = 0
                current_index = current_index - 1 # little hack for sergberto
                for column_name in self.column_names:
                    current_index = self.extract_value(current_paper_name, current_data, current_index, column_name, self.variable_names[variable_index])
                    variable_index = variable_index + 1

                next_paper_name = current_paper_name
                while current_paper_name == next_paper_name and current_index + 1 < len(current_data):
                    current_index = current_index + 1
                    next_paper_name = current_data.iloc[current_index]["article-open"]
                    # next_paper_name = current_data.iloc[current_index]["article-titles"]

            print("are we done?")  # Well not really, now I need to make it into an excel.
            print(self.max_sections)
            self.papers_to_compressed_view()

    def load_compressed_view(self):
        xlsx_files = self.get_files(self.papers_directory, ".xlsx")  # Get the compressed view
        self.papers = {}

        for file in xlsx_files:
            print(file)

            current_data = pd.read_excel(self.papers_directory + file)  # Get the pandas object
            current_data = current_data.replace(np.nan, "")
            current_data = current_data.replace("&nbsp", "")
            current_data = current_data.replace('\u00A0', '')

            for index, row in current_data.iterrows():

                paper_name = row["paper_name"]
                paper_session = row["paper_session"]
                paper = Paper(paper_name, paper_session)

                print(paper_name)

                if paper_name not in self.papers:  # add the paper if it doesn't exist!
                    self.papers.update({paper_name: paper})

                for (columnName, columnData) in current_data.iteritems():

                    if columnName == 'paper_name' or columnName == 'paper_session':
                        continue
                    else:
                        paper.add_value_compressed(row[columnName], columnName)

        print("done!")

    def calculate_papers_metrics(self, column_name: str, avg = True, sd = True, file_name="paper_metrics.csv", save=True, append=True):

        total_count = 0
        paper_count = 0
        counter = []
        avg_count = 0
        sd_count = 0

        for paper_name, paper in self.papers.items():
            paper_count += 1
            total_count += len(paper.get_paper_full_authors_no_delimiter())
            counter.append(len(paper.get_paper_full_authors_no_delimiter()))

        counter = np.array(counter)
        avg_count = float(total_count)/float(paper_count)

        print(avg_count)
        print("\n \n")

        print(len(counter))
        print(np.average(counter))
        print(np.std(counter))
        print(np.percentile(counter, 2.5))
        print(np.percentile(counter, 97.5))

    def calculate_ngram_per_paper(self, column_name: str, all_ngrams_until=True, ngram=3, top_k=5, avg=True, sd=True, file_name="paper_metrics.csv", save=True, append=True):

        if all_ngrams_until:
            grams = [Counter() for i in range(ngram)]
        else:
            grams = [Counter()]

        for paper_name, paper in self.papers.items():
            paper_sections = paper.get_paper_sections_no_delimiter()
            paper_sections_no_punctuation = [self.remove_punctuation(x) for x in paper_sections]

            seen_ngrams = set()

            for section in paper_sections_no_punctuation:
                words = section.split()

                if all_ngrams_until:
                    for gram_step in range(ngram):
                        ngrams = [tuple(words[i:i + gram_step + 1]) for i in range(len(words) - gram_step)]
                        ngram_counts = Counter(ngrams)

                        # for ngram, count in sorted(ngram_counts.items(), key=lambda x: x[1], reverse=True)[:top_k]:
                        #   print(f"{ngram}: {count} occurrences of total)")

                        for ngram_collected in ngrams:
                            # Count only if the n-gram hasn't been seen in this text before
                            if ngram_collected not in seen_ngrams:
                                grams[gram_step][ngram_collected] += 1
                                # all_ngram_counts[ngram] += 1
                                seen_ngrams.add(ngram_collected)

                        # grams[gram_step].update(ngram_counts)

                        # Update the overall counts
                        #all_ngram_counts.update(ngram_counts)
                else:
                    # Generate and count 3-grams
                    ngrams = [tuple(words[i:i + ngram]) for i in range(len(words) - ngram - 1)]
                    ngram_counts = Counter(ngrams)

                    for ngram_collected in ngrams:
                        # Count only if the n-gram hasn't been seen in this text before
                        if ngram_collected not in seen_ngrams:
                            grams[0][ngram_collected] += 1
                            # all_ngram_counts[ngram] += 1
                            seen_ngrams.add(ngram_collected)

                    # Update the overall counts
                    # grams[0].update(ngram_counts)


        # Display the top 5 n-grams by counts sorted!
        print("Here we present all the specified ngram ocurrances per paper!")
        for all_ngram_counts in grams:
            total_ngrams = len(self.papers)
            for ngram, count in sorted(all_ngram_counts.items(), key=lambda x: x[1], reverse=True)[:top_k]:
                percentage = (count / total_ngrams) * 100
                print(f"{ngram}: {count} occurrences ({percentage:.2f}% of total)")
            print("\n")

    def calculate_ngram(self, column_name: str, all_ngrams_until=True, ngram=3, top_k=5, avg=True, sd=True, file_name="paper_metrics.csv", save=True, append=True):

        if all_ngrams_until:
            grams = [Counter() for i in range(ngram)]
        else:
            grams = [Counter()]

        for paper_name, paper in self.papers.items():
            paper_sections = paper.get_paper_sections_no_delimiter()
            paper_sections_no_punctuation = [self.remove_punctuation(x) for x in paper_sections]

            for section in paper_sections_no_punctuation:
                words = section.split()

                if all_ngrams_until:
                    for gram_step in range(ngram):
                        ngrams = [tuple(words[i:i + gram_step + 1]) for i in range(len(words) - gram_step)]
                        ngram_counts = Counter(ngrams)
                        grams[gram_step].update(ngram_counts)

                        # Update the overall counts
                        #all_ngram_counts.update(ngram_counts)
                else:
                    # Generate and count 3-grams
                    ngrams = [tuple(words[i:i + ngram]) for i in range(len(words) - ngram - 1)]
                    ngram_counts = Counter(ngrams)

                    # Update the overall counts
                    grams[0].update(ngram_counts)


        # Display the top 5 n-grams by counts sorted!
        print("Here we present all the specified ngram ocurrances in general in all papers and sections")
        for all_ngram_counts in grams:
            total_ngrams = sum(all_ngram_counts.values())
            for ngram, count in sorted(all_ngram_counts.items(), key=lambda x: x[1], reverse=True)[:top_k]:
                percentage = (count / total_ngrams) * 100
                print(f"{ngram}: {count} occurrences ({percentage:.2f}% of total)")
            print("\n")

    def extract_sentences(self, column_name: str, all_ngrams_until=True, minimum_length=1, top_k=5, avg=True, sd=True, file_name="paper_metrics.csv", save=True, append=True):

        all_sentence_counts = Counter()

        for paper_name, paper in self.papers.items():
            paper_sections = paper.get_paper_sections_no_delimiter()
            paper_sections_no_punctuation = [self.remove_punctuation(x) for x in paper_sections]

            for section in paper_sections:

                # text = re.sub(r'[^a-zA-Z0-9.,;\s]', '', section)
                # text = re.sub(r'[^a-zA-Z.,;\s]', '', section)
                # text = re.sub(r'[^a-zA-Z.,;\s-]', '', section)

                # Preprocess the text (remove non-alphanumeric characters, convert to lowercase)
                text = re.sub(r'[^a-zA-Z.,;\s\n\[\]-]', '', section)

                # Remove numbers within square brackets
                text = re.sub(r'\[.*?\]', '', text)

                # Remove punctuation followed by other punctuation without spaces
                text = re.sub(r'([.,;])\s*', r'\1', text)

                # Remove punctuation followed by other punctuation without spaces
                text = re.sub(r'[.,;]+(?=[.,;])', '', text)

                text = text.lower()

                # Extract sentences based on ".", ",", ";"
                # sentences = re.split(r'[.,;]', text)
                sentences = re.split(r'[.,;\n]', text)

                # Remove leading and trailing whitespaces from each sentence
                sentences = [sentence.strip() for sentence in sentences]

                # Filter out sentences that are either one word or empty space
                sentences = [sentence for sentence in sentences if len(sentence.split()) > minimum_length]

                # Count each unique sentence
                sentence_counts = Counter(sentences)

                # Update the overall counts
                all_sentence_counts.update(sentence_counts)


        # Display the top 5 n-grams by counts sorted!
        print("Here we present all the sentences ocurrances in general in all papers and sections")
        total_sentences = sum(all_sentence_counts.values())
        for sentence, count in sorted(all_sentence_counts.items(), key=lambda x: x[1], reverse=True)[:top_k]:
            percentage = (count / total_sentences) * 100
            print(f"{sentence}: {count} occurrences ({percentage:.2f}% of total)")

        print("\n")

    def extract_sentences_per_paper(self, column_name: str, all_ngrams_until=True, minimum_length=1, top_k=5, avg=True, sd=True, file_name="paper_metrics.csv", save=True, append=True):

        all_sentence_counts = Counter()

        for paper_name, paper in self.papers.items():
            paper_sections = paper.get_paper_sections_no_delimiter()
            seen_sentence = set()

            for section in paper_sections:

                # text = re.sub(r'[^a-zA-Z0-9.,;\s]', '', section)
                # text = re.sub(r'[^a-zA-Z.,;\s]', '', section)
                text = re.sub(r'[^a-zA-Z.,;\s-]', '', section)

                # Remove punctuation followed by other punctuation without spaces
                text = re.sub(r'([.,;])\s*', r'\1', text)

                # Remove punctuation followed by other punctuation without spaces
                text = re.sub(r'[.,;]+(?=[.,;])', '', text)

                text = text.lower()

                # Extract sentences based on ".", ",", ";"
                # sentences = re.split(r'[.,;]', text)
                sentences = re.split(r'[.,;\n]', text)

                # Remove leading and trailing whitespaces from each sentence
                sentences = [sentence.strip() for sentence in sentences]

                # Filter out sentences that are either one word or empty space
                sentences = [sentence for sentence in sentences if len(sentence.split()) > minimum_length]

                # Count each unique sentence
                sentence_counts = Counter(sentences)

                for sentence_count in sentence_counts:
                    # Count only if the n-gram hasn't been seen in this text before
                    if sentence_count not in seen_sentence:
                        all_sentence_counts[sentence_count] += 1
                        # all_ngram_counts[ngram] += 1
                        seen_sentence.add(sentence_count)


        # Display the top 5 n-grams by counts sorted!
        print("Here we present all sentences ocurrances in papers")
        total_sentences = len(self.papers)
        for sentence, count in sorted(all_sentence_counts.items(), key=lambda x: x[1], reverse=True)[:top_k]:
            percentage = (count / total_sentences) * 100
            print(f"{sentence}: {count} occurrences ({percentage:.2f}% of total)")

        print("\n")

    def remove_punctuation(self, input_string):
        # Make a regular expression that matches all punctuation
        regex = re.compile('[%s]' % re.escape(string.punctuation))
        text = regex.sub('', input_string)
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        text = text.lower()
        # Use the regex
        return text

    def count_occurrences_of_string(self, target_string):
        total_occurrences = 0

        for paper_name, paper in self.papers.items():
            paper_sections = paper.get_paper_sections_no_delimiter()
            paper_sections_no_punctuation = [self.remove_punctuation(x) for x in paper_sections]

            for section in paper_sections_no_punctuation:

                occurrences = section.count(target_string.lower())
                total_occurrences += occurrences


        for text in texts:
            # Case-insensitive search
            occurrences = text.lower().count(target_string.lower())
            total_occurrences += occurrences

        return total_occurrences

    def create_limited_dataset_text_references(self, input_type: DatasetInputType, token_limit=512, section_token_limit=400):
        dataset_llm = DatasetLLMPapers()

        for paper_name, paper in self.papers.items():
            paper_sections = paper.get_paper_sections_no_delimiter()
            paper_section_titles = paper.get_paper_section_titles_no_delimiter()
            paper_references = paper.get_paper_references_no_delimiter()

            for i in range(0, len(paper_sections)):

                dataset_llm.format_data_section_paragraphs(input_type, paper_section_titles[i], paper_sections[i],
                                                       paper_references, paper.get_paper_session(), section_token_limit,
                                                       token_limit, True)


            print(paper.get_paper_name())

        df = pd.DataFrame(dataset_llm.get_data(),
                          columns=dataset_llm.get_data().keys())
        # df.to_excel("output.xlsx")
        df.to_excel(self.papers_directory + "/chi-2023-data-no-references.xlsx")


    def papers_to_compressed_view(self):

        # Get the paper with the most sections!
        self.collected_papers_general = CollectedPapersGeneral("chi23", self.max_sections)

        for paper_name, paper_object in self.papers.items():
            print(paper_name)

            self.collected_papers_general.add_sections(paper_object.get_paper_sections_raw())

            self.collected_papers_general.add_full_datapoint(
                paper_object.get_paper_name(),
                paper_object.get_paper_session(),
                paper_object.get_paper_abstract(),
                paper_object.get_paper_authors(),
                paper_object.get_paper_full_authors(),
                paper_object.get_paper_section_titles(),
                # paper_object.get_paper_sections(),
                paper_object.get_paper_references()
            )

        df = pd.DataFrame(self.collected_papers_general.get_data(), columns=self.collected_papers_general.get_data().keys())
        #df.to_excel("output.xlsx")
        df.to_excel(self.papers_directory + "/compressed_view.xlsx")
