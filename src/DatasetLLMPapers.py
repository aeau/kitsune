import pandas as pd
import re
import math

from src.Experimenter import *
#from src.Experimenter import DatasetInputType


class DatasetLLMPapers:

    def __init__(self):

        self.papers_data = {}
        self.papers_data.update({'text': []})

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

            if input_type.name == "REFERENCES" or input_type.name == "REFERENCES_SECTION_PARTS":
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

    def add_input(self, input_type, paper_section_title, paper_session, current_text, section_counter, break_by_chunk):

        chunk_input_text = ""
        if break_by_chunk:
            chunk_input_text = " part " + str(section_counter)

        paper_section_title = re.sub(r'\d+', '', paper_section_title)
        paper_section_title = paper_section_title.strip()

        if input_type.name == "NO_REFERENCES":
            return (current_text + "Write the " +
                    str(paper_section_title) +
                    " of an ACM CHI paper on " +
                    str(paper_session))
        elif input_type.name == "NO_REFERENCES_SECTION_PARTS": # No references
            return (current_text + "Write the " +
                    str(paper_section_title) + chunk_input_text +
                    " of an ACM CHI paper on " +
                    str(paper_session))
        elif input_type.name == "REFERENCES_SECTION_PARTS": # With references
            return (current_text + "Write the " +
                    str(paper_section_title) + chunk_input_text +
                    " of an ACM CHI paper on " +
                    str(paper_session) +
                    " together with its references"
                    )
        elif input_type.name == "REFERENCES":
            return (current_text + "Write the " +
                    str(paper_section_title) +
                    " of an ACM CHI paper on " +
                    str(paper_session) +
                    " together with its references"
                    )

    def get_data(self):
        return self.papers_data