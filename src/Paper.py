import pandas as pd
import re

class Paper:

    def __init__(self, paper_name, paper_session):
        self.paper_name = paper_name
        self.paper_session = paper_session
        self.paper_authors = []
        self.papers_authors_institutions = []
        self.abstract = ""
        self.section_titles = []
        self.sections = []
        self.references = []

        self.delimiter = " ___ "
        self.current_reference = 0

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

        value = str(value)
        value = value.replace('\u00A0', '')

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
                self.paper_authors.append(split_t)
        elif variable == "paper_authors_institution":
            split_text = value.split(self.delimiter)
            for split_t in split_text:
                self.papers_authors_institutions.append(split_t)
        elif variable == "section_titles":
            split_text = value.split(self.delimiter)
            for split_t in split_text:
                self.section_titles.append(split_t)

    def add_references(self, references_text):
        split_references = references_text.split(self.delimiter)
        split_references_aux = references_text.split(self.delimiter)

        for split_reference in split_references:
            self.current_reference = self.current_reference + 1
            self.references.append("[" + str(self.current_reference) + "] " + split_reference)

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

    def get_paper_authors_no_delimiter(self):
        return self.paper_authors

    def get_paper_full_authors(self):
        return self.delimiter.join(self.papers_authors_institutions)

    def get_paper_full_authors_no_delimiter(self):
        return self.papers_authors_institutions

    def get_paper_section_titles(self):
        return self.delimiter.join(self.section_titles)

    def get_paper_section_titles_no_delimiter(self):
        return self.section_titles

    def get_paper_sections(self):
        return self.delimiter.join(self.sections)

    def get_paper_sections_no_delimiter(self):
        return self.sections

    def get_paper_references_no_delimiter(self):
        return self.references

    def get_paper_sections_raw(self):
        return self.sections

    def get_paper_references(self):
        return self.delimiter.join(self.references)

    def add_datapoint(self, paper_name, session_name, abstract):
        self.papers_data['paper_name'].append(paper_name)
        self.papers_data['paper_session'].append(session_name)
        self.papers_data['abstract'].append(abstract)
        self.papers_data['paper_authors'].append([])
        self.papers_data['paper_authors_institution'].append([])
        self.papers_data['section_titles'].append([])
        self.papers_data['sections'].append([])
        self.papers_data['references'].append([])

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
