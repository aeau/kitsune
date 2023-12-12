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

print(date(2022, 9, 4))

print("\'176\'")
print("asdas")

a = "asdasd"
b = "asd ejrj"
c = "06:35"
d = "09:44"
e = "-1"
f = "2"
g = "12"

print(a, a.split(":"), len(a.split(":")))
print(b, b.split(":"), len(b.split(":")))
print(c, c.split(":"), len(c.split(":")))
print(d, d.split(":"), len(d.split(":")))
print(e, e.split(":"), len(e.split(":")))
print(f, f.split(":"), len(f.split(":")))
print(g, g.split(":"), len(g.split(":")))

marked = [(12, 13), (14, 15), (16, 17), (18, 19)]

print(len(marked))

import pandas as pd

technologies = {
    'days':["Monday","Monday","Monday","Tuesday","Monday","Tuesday","Wednesday","Wednesday"],
    'week' :[37, 38, 37, 38, 39, 40, 37, 38],
    'sub_time':[4, 5, 4, 4, 4, 8, 12, 15],
    'real_time':["04:00","05:12","04:23","04:36","04:09","08:14","12:32","15:15"],
    'Duration':['30day','40days','40days', '35days','40days','60days','60days','70days'],
    'Discount':[1000,2300, 15, 1200,2500,2000,2000,3000],
              }
df = pd.DataFrame(technologies)
print(df)

# Groupby multiple columns
# result = df.groupby(['days','week','sub_time'], as_index=False).apply(lambda x : x.sum())
result = df.groupby(['days','week','sub_time'], as_index=False).sum()
print(result)

result = result.sort_values(by=["Discount"], ascending=False)
print(result)



#### MORE TESTING

def search_for_references_in_text(section_part):
    # Use regular expression to find all numbers within square brackets and at the beginning or end
    numbers = re.findall(r'\b(\d+)\b|\[(\d+)\]', section_part)

    # Flatten the list and convert the extracted numbers from strings to integers
    numbers = [int(number) for group in numbers for number in group if number]

    return numbers

# Example usage
input_string = "33] I know that you are [23, 24, 25] but you should never [1], however; [3, 15] are not happy about that! [2"
result = search_for_references_in_text(input_string)
print(result)

def extract_and_count_sentences(texts):
    all_sentence_counts = Counter()

    for text in texts:
        # Preprocess the text (remove non-alphanumeric characters, numbers, and convert to lowercase)
        # text = re.sub(r'[^a-zA-Z.,;\s\n-]', '', text)
        # text = re.sub(r'[^a-zA-Z.,;\s\n\[\]\d-]', '', text)
        text = re.sub(r'[^a-zA-Z.,;?!:\s\n\[\]\d-]', '', text)

        # Remove everything inside square brackets
        text = re.sub(r'\[.*?\]', '', text)

        text = re.sub(r'\[\s*\d+\s*(?:,\s*\d+\s*)*\]', '', text)

        # Remove punctuation even if there is a space in between, excluding "-"
        text = re.sub(r'([.,;])\s*', r'\1', text)

        # Replace consecutive spaces with a single space
        text = re.sub(r'\s+', ' ', text)

        # Remove spaces before punctuation, excluding "-"
        # text = re.sub(r'\s*([.,;?!:])\s*', r'\1', text)
        text = re.sub(r'\s*([.,;?!:])', r'\1', text)

        text = text.lower()

        # Extract sentences based on ".", ",", ";", and "\n"
        # sentences = re.split(r'[.,;\n]', text)

        # Extract sentences based on ".", ",", ";", ":", "!", "?", and "\n"
        sentences = re.split(r'[.,;?!:\n]', text)


        # Remove leading and trailing whitespaces from each sentence
        sentences = [sentence.strip() for sentence in sentences]

        # Filter out sentences that are either one word or empty space
        sentences = [sentence for sentence in sentences if len(sentence.split()) > 1]

        # Count each unique sentence
        sentence_counts = Counter(sentences)

        # Update the overall counts
        all_sentence_counts.update(sentence_counts)

    return all_sentence_counts

# Example usage:
input_texts = [
    "I was hanging-out [23, 21, 89], but [00, 21, p.35]? then I! got 9*, for instance; sandwiches.",
    "Another example text with more sentences.\nLet's see how the function handles multiple texts.",
    "The third text for testing. It contains some repetitive sentences to check if the function counts them correctly.",
    "Our knowledge and values play an essential role in human-computer interaction design,; imbued with implicit ethical positionalities,,",
]

result = extract_and_count_sentences(input_texts)

# Display the result sorted by counts in descending order
for sentence, count in sorted(result.items(), key=lambda x: x[1], reverse=True):
    print(f"{sentence}: Occurs in {count} texts")




paper_directory = str(core_path) + "/"
paper_directory = str(core_path) + "/compressed_view/"

testPlot = Experimenter(paper_directory, "testing this s")
# testPlot.load_all_original_papers_data() # load the raw info from the website
testPlot.load_compressed_view() # After we have actually loaded all the raw data from html, it is easy and quick to load comprresed
testPlot.calculate_papers_metrics(column_name="author_names")

testPlot.extract_sentences(column_name="nothing")
testPlot.extract_sentences(column_name="nothing", minimum_length=3)
testPlot.extract_sentences(column_name="nothing", minimum_length=6)

testPlot.extract_sentences_per_paper(column_name="not important")
testPlot.extract_sentences_per_paper(column_name="not important", minimum_length=3)
testPlot.extract_sentences_per_paper(column_name="not important", minimum_length=6)
#testPlot.calculate_ngram_unique(column_name="no_matter", ngram=10, all_ngrams_until=True, top_k=5)
#testPlot.calculate_ngram(column_name="intro", ngram=10, top_k=5)
# testPlot.create_limited_dataset_text_references(DatasetInputType.NO_REFERENCES_SECTION_PARTS) # Create a Dataset

# df = df[:k]