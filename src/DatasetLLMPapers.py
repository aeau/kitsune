import pandas as pd
import re
import math

from src.Experimenter import *


class DatasetLLMPapers:

    def __init__(self):

        self.papers_data = {}
        self.papers_data.update({'text': []})  # Week number!
       #  self.papers_data.update({'meta': []})  # Week number!

    def add_text(self, text):
        print(text)

    def format_data_section_paragraphs(self, input_type : DatasetInputType, paper_section_title, paper_section, paper_references, paper_session,
                    section_token_limit, max_token_limit, input_break_in_parts=True):
        text_data = "User: User: "
        another = "Assistant: Chip: "
        text_data = self.add_input(input_type, paper_section_title, paper_session, text_data, 0, False)
        section_chunks = self.get_section_chunks(paper_section, section_token_limit)
        section_counter = 1

        for section_chunk in section_chunks:

            if input_break_in_parts and len(section_chunks) > 1:
                text_data = "User: User: "
                text_data = self.add_input(input_type, paper_section_title, paper_session, text_data, section_counter, input_break_in_parts)
                section_counter = section_counter + 1

            input_data = text_data
            input_data = text_data + " Assistant: Chip: "
            input_data = input_data + section_chunk

            if input_type == DatasetInputType.REFERENCES or input_type == DatasetInputType.REFERENCES_SECTION_PARTS:
                references_to_add = self.search_for_references_in_text(section_chunk)
                references_to_add = [int(x) for x in references_to_add]
                references_to_add = list(set(references_to_add))
                references_to_add = sorted(references_to_add, reverse=False)

                if len(references_to_add) == 0:
                    self.papers_data["text"].append(input_data)
                else:
                    input_data = input_data + "\n \n References: "
                    for reference_to_add in references_to_add:
                        if int(reference_to_add) < len(paper_references):
                            input_data = input_data + "\n " + paper_references[int(reference_to_add) - 1]
                        # print(paper_references[int(reference_to_add)])
                    self.papers_data["text"].append(input_data)
            else:
                self.papers_data["text"].append(input_data)

            print(len(input_data.split()))
            # self.papers_data["text"].append(input_data)
            # self.papers_data["meta"].append()

    def format_data(self, input_number, paper_section_title, paper_section, paper_references, paper_session, section_token_limit, max_token_limit):
        text_data = "User: User: "
        another = "Assistant: Chip: "
        text_data = self.add_input(input_number, paper_section_title, paper_session, text_data)

        section_count = len(paper_section.split())
        text_number = float(section_count) / float(section_token_limit)
        text_number = int(math.ceil(text_number))

        for i in range(0, text_number): # we will create as many as necessary
            input_data = text_data
            input_data = text_data + " Assistant: Chip: "
            section_part = paper_section.split()
            section_part = section_part[i*section_token_limit:(i+1)*section_token_limit]
            section_part = " ".join(section_part)
            input_data = input_data + section_part

            if input_number == 2:
                references_to_add = self.search_for_references_in_text(section_part)
                if len(references_to_add) == 0:
                    self.papers_data["text"].append(input_data)
                else:
                    input_data = input_data + "\n \n References: "
                    for reference_to_add in references_to_add:
                        input_data = input_data + "\n " + paper_references[int(reference_to_add) - 1]
                        # print(paper_references[int(reference_to_add)])

            print(len(input_data.split()))
            self.papers_data["text"].append(input_data)

    def get_section_chunks(self, paper_section, section_token_limit):
        section_count = len(paper_section.split())
        return_chunks = []

        if section_count < section_token_limit:
            return_chunks.append(paper_section)
            return return_chunks

        section_chunks = paper_section.split("\n")  # Divide by paragraphs
        return_chunks = []
        current_chunk = ""
        accumulated_count = 0
        current_accumulated_count = 0
        i = 0

        while i < len(section_chunks):
            chunk_count = len(section_chunks[i].split())

            if chunk_count >= section_token_limit: # Special case if we find a chunk that by itself is bigger than the limit then we break it!
                special_chunks = self.split_fot_special_chunk(chunk_count, section_chunks[i], section_token_limit)
                i = i + 1
                return_chunks.extend(special_chunks)
                current_chunk = ""
                current_accumulated_count = 0
            else:

                current_accumulated_count = current_accumulated_count + chunk_count

                if current_accumulated_count < section_token_limit:  # we have space
                    current_chunk = current_chunk + section_chunks[i]
                    accumulated_count = accumulated_count + chunk_count
                    i = i + 1
                else:  # we actually need to restart
                    current_accumulated_count = 0
                    return_chunks.append(current_chunk)
                    current_chunk = ""

        if current_chunk != "":
            return_chunks.append(current_chunk)

        return return_chunks

    def split_fot_special_chunk(self, oversize_chunk_size, oversize_chunk, section_token_limit):

        text_number = float(oversize_chunk_size) / float(section_token_limit)
        text_number = int(math.ceil(text_number))
        if text_number == 1:  # super hack!
            text_number = 2
            section_token_limit = section_token_limit - 100
        special_chunks =[]

        for i in range(0, text_number): # we will create as many as necessary
            section_part = oversize_chunk.split()
            if i + 1 == text_number:
                section_part = section_part[i * section_token_limit:]
            else:
                section_part = section_part[i*section_token_limit:(i+1)*section_token_limit]

            section_part = " ".join(section_part)
            special_chunks.append(section_part)

        return special_chunks

    def search_for_references_in_text(self, section_part):

        # Use regular expression to find all integer or decimal numbers within square brackets
        # numbers = re.findall(r'\[(\d+(?:\.\d+)?)\s*(?:,\s*p\.?\s*\d+)?\]', section_part)

        # Convert the extracted numbers from strings to integers (ignoring decimal parts)
        # numbers = [int(float(number)) if '.' in number else int(number) for number in numbers]

        # return numbers

        # Use regular expression to find all integer or decimal numbers within square brackets
        #numbers = re.findall(r'\[(\d+(?:\.\d+)?)\s*(?:,\s*p\.?\s*\d+)?\]', section_part)

        # Convert the extracted numbers from strings to integers (ignoring decimal parts)
        #numbers = [int(float(number)) if '.' in number else int(number) for number in numbers]

        #return numbers

        # Use regular expression to find all numbers within square brackets and at the beginning or end
        result = re.sub(r'\[\d*p\d*\.\d+]', '', section_part)
        result = re.sub(r'\[\d*p\d*]', '', result)
        result = self.remove_p_numbers_in_square_brackets(result)
        # print(result)
        numbers = re.findall(r'\b(\d+)\b|\[(\d+)\]', result) # Maybe this is still the best!
        # numbers = re.findall(r'\[(\d+)]|\b(\d+)(?=\])\b', result)

        # print(numbers)


        # Flatten the list and convert the extracted numbers from strings to integers
        numbers = [int(number) for group in numbers for number in group if number]

        #numbers = re.findall(r'\[(\d+)\s*(?:,\s*p\.?\s*\d+)?\]', section_part)


        # Convert the extracted numbers from strings to integers
        #numbers = [int(number) for number in numbers]

        return numbers

    def remove_p_numbers_in_square_brackets(self, s):
        result = []
        inside_brackets = False
        current_number = ""
        next_number = False
        got_weird = False
        numbers = []

        for char in s:

            if inside_brackets == False and char.isdigit():
                char = ""
            elif char == '[':
                inside_brackets = True
                current_number = ""
            elif char == ']':
                inside_brackets = False
                got_weird = False
                result.append(f"[{current_number}]")
            elif inside_brackets:

                if got_weird:
                    if char == ",":
                        got_weird = False
                    else:
                        char = ""

                if char == "p" or char == ".":
                    got_weird = True
                    char = ""

                current_number += char
            else:
                result.append(char)

        return ''.join(result)

    def add_input(self, input_type : DatasetInputType, paper_section_title, paper_session, current_text, section_counter, break_by_chunk):

        chunk_input_text = ""
        if break_by_chunk:
            chunk_input_text = " part " + str(section_counter)

        paper_section_title = re.sub(r'\d+', '', paper_section_title)
        paper_section_title = paper_section_title.strip()

        if input_type == DatasetInputType.NO_REFERENCES:
            return (current_text + "Write the " +
                    str(paper_section_title) +
                    " of an ACM CHI paper on " +
                    str(paper_session))
        elif input_type == DatasetInputType.NO_REFERENCES_SECTION_PARTS: # No references
            return (current_text + "Write the " +
                    str(paper_section_title) + chunk_input_text +
                    " of an ACM CHI paper on " +
                    str(paper_session))
        elif input_type == DatasetInputType.REFERENCES_SECTION_PARTS: # With references
            return (current_text + "Write the " +
                    str(paper_section_title) + chunk_input_text +
                    " of an ACM CHI paper on " +
                    str(paper_session) +
                    " together with its references"
                    )
        elif input_type == DatasetInputType.REFERENCES:
            return (current_text + "Write the " +
                    str(paper_section_title) +
                    " of an ACM CHI paper on " +
                    str(paper_session) +
                    " together with its references"
                    )

    def add_abstract(self, abstract):
        self.abstract = abstract

    def add_value(self, value, variable):
        if variable == "author":
            self.paper_authors.append(value)
        elif variable == "author_institution":
            self.papers_authors_institutions.append(value)
        elif variable == "section_title":
            self.section_titles.append(value)
        elif variable == "section":
            self.sections.append(value)
        elif variable == "reference":
            self.references.append(value)

    def add_value_compressed(self, value, variable):

        if variable == 'references':
            self.add_references(value)
        elif variable == 'abstract':
            self.abstract = value
        elif re.match(r"section[0-9]+", variable) and value != "":
            # split_text = value.split(self.delimiter)
            self.sections.append(value)
            # for split_t in split_text:
            #     self.sections.append(split_text)
        elif variable == "paper_authors":
            split_text = value.split(self.delimiter)
            for split_t in split_text:
                self.paper_authors.append(split_text)
        elif variable == "paper_authors_institution":
            split_text = value.split(self.delimiter)
            for split_t in split_text:
                self.papers_authors_institutions.append(split_text)
        elif variable == "section_titles":
            split_text = value.split(self.delimiter)
            for split_t in split_text:
                self.section_titles.append(split_text)

    def add_references(self, references_text):
        split_references = references_text.split(self.delimiter)
        split_references_aux = references_text.split(self.delimiter)

        for split_reference in split_references:
            self.current_reference = self.current_reference + 1
            self.references.append("[" + str(self.current_reference) + "] " + split_reference)

    def get_data(self):
        return self.papers_data

    def add_author(self, author):
        self.paper_authors.append(author)

    def add_author_institution(self, author_institution):
        self.papers_authors_institutions.append(author_institution)

    def add_section_title(self, section_title):
        self.section_titles.append(section_title)

    def add_section(self, section):
        self.sections.append(section)

    def add_reference(self, reference):
        self.references.append(reference)

    def get_paper_name(self):
        return self.paper_name

    def get_paper_session(self):
        return self.paper_session

    def get_paper_abstract(self):
        return self.abstract

    def get_paper_authors(self):
        return self.delimiter.join(self.paper_authors)

    def get_paper_full_authors(self):
        return self.delimiter.join(self.papers_authors_institutions)

    def get_paper_section_titles(self):
        return self.delimiter.join(self.section_titles)

    def get_paper_sections(self):
        return self.delimiter.join(self.sections)

    def get_paper_sections_raw(self):
        return self.sections

    def get_paper_references(self):
        return self.delimiter.join(self.references)

    def add_datapoint(self, paper_name, session_name, abstract):
        self.papers_data['paper_name'].append(paper_name)  # Week number!
        self.papers_data['paper_session'].append(session_name)  # Week number!
        self.papers_data['abstract'].append(abstract)  # If supervision in person! (yes. no, canceled)
        self.papers_data['paper_authors'].append([])  # If supervision in person! (yes. no, canceled)
        self.papers_data['paper_authors_institution'].append([])  # If supervision in person! (yes. no, canceled)
        self.papers_data['section_titles'].append([])  # If supervision in person! (yes. no, canceled)
        self.papers_data['sections'].append([])  # If supervision in person! (yes. no, canceled)
        self.papers_data['references'].append([])  # If supervision in person! (yes. no, canceled)

        self.current_index = self.current_index + 1

    def update_datapoint(self, data_column, data):
        self.papers_data[data_column][self.current_index].append(data)

    # def update_used(self, index):
    #     # print(self.papers_data['validation_tickets'][index])
    #     # print(self.papers_data['line'][index])
    #     # print(self.papers_data['week'][index])
    #     # print(self.papers_data['sub_time'][index])
    #     # print(self.papers_data['date'][index])
    #     self.papers_data['used'][index] = 1
    #
    # def update_used_last_index(self):
    #     self.papers_data['used'][self.current_index - 1] = 1


    def get_filtered_data(self, sum: bool, data_frame, **kwargs):
        for key, value in kwargs.items():
            print(key, value)

        if data_frame is None:
            df = pd.DataFrame(self.papers_data, columns=self.papers_data.keys())
        else:
            df = data_frame
        #
        # print(df.iloc[(0, 5)])
        # print(type(df.iloc[(0, 5)]))

        if kwargs:
            query = ' and '.join(['{0}=={1}'.format(key, value) for key, value in kwargs.items()])
            print(query)
            # matched = np.all([df[vn] == vv for vn, vv in kwargs.items()], axis=0)
            # filtered_df = df[matched]
            df = df.query(' and '.join(['{0}=={1}'.format(key, value) for key, value in kwargs.items()]))
            print("okay")

        if sum:
            print("sum")

            sum = df.sum()
            df = pd.DataFrame(columns=self.papers_data.keys())
            df = df.append((sum.transpose()), ignore_index=True)
        else:
            print("not sum")

        return df

        # other = []
        # for key, value in kwargs.items()

    def get_data_greater_than(self, sum: bool, data_frame, **kwargs):
        for key, value in kwargs.items():
            print(key, value)

        if data_frame is None:
            df = pd.DataFrame(self.papers_data, columns=self.papers_data.keys())
        else:
            df = data_frame

        query = ' and '.join(['{0}>{1}'.format(key, value) for key, value in kwargs.items()])
        print(query)
        # matched = np.all([df[vn] == vv for vn, vv in kwargs.items()], axis=0)
        # filtered_df = df[matched]
        df = df.query(' and '.join(['{0}>{1}'.format(key, value) for key, value in kwargs.items()]))
        print("okay")

        if sum:
            print("sum")
        else:
            print("not sum")

        df = df.sort_values(by=['date'])
        return df

    def get_data_lesser_than(self, sum: bool, data_frame, **kwargs):
        for key, value in kwargs.items():
            print(key, value)

        if data_frame is None:
            df = pd.DataFrame(self.papers_data, columns=self.papers_data.keys())
        else:
            df = data_frame

        query = ' and '.join(['{0}<{1}'.format(key, value) for key, value in kwargs.items()])
        print(query)
        # matched = np.all([df[vn] == vv for vn, vv in kwargs.items()], axis=0)
        # filtered_df = df[matched]
        df = df.query(' and '.join(['{0}<{1}'.format(key, value) for key, value in kwargs.items()]))
        print("okay")

        if sum:
            print("sum")
        else:
            print("not sum")

        return df

    def get_data_groupby(self, data_frame, groupby: []):

        if data_frame is None:
            df = pd.DataFrame(self.papers_data, columns=self.papers_data.keys())
        else:
            df = data_frame

        df = df.groupby(groupby, as_index=False).sum()

        return df

    def get_data_top_k(self, sum: bool, data_frame, k, column):

        if data_frame is None:
            df = pd.DataFrame(self.papers_data, columns=self.papers_data.keys())
        else:
            df = data_frame

        df = df.sort_values(by=[column], ascending=False)
        df = df[:k]

        return df
