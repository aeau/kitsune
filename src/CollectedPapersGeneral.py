import pandas as pd


class CollectedPapersGeneral:

    def __init__(self, dataset_name, max_number_sections):
        self.dataset_name = dataset_name
        self.max_number_sections = max_number_sections
        self.papers_data = {}
        self.papers_data.update({'paper_name': []})
        self.papers_data.update({'paper_session': []})
        self.papers_data.update({'paper_authors': []})
        self.papers_data.update({'paper_authors_institution': []})
        self.papers_data.update({'abstract': []})
        self.papers_data.update({'section_titles': []})

        for i in range(0, max_number_sections):
            self.papers_data.update({"section" + str(i): []})

        self.papers_data.update({'references': []})

        self.current_index = -1

    def create_as_many_columns_as_sections(self, max_number_sections):

        for i in range(0, max_number_sections):
            self.papers_data.update({"section" + str(self.internal_index): []})

    def add_sections(self, section_list: []):

        for i in range(0, self.max_number_sections):
            if i > len(section_list) - 1:
                self.papers_data["section" + str(i)].append("")
            else:
                self.papers_data["section" + str(i)].append(str(section_list[i]))

    def add_datapoint(self, paper_name, session_name, abstract):
        self.papers_data['paper_name'].append(paper_name)
        self.papers_data['paper_session'].append(session_name)
        self.papers_data['abstract'].append(abstract)
        self.papers_data['paper_authors'].append([])
        self.papers_data['paper_authors_institution'].append([])
        self.papers_data['section_titles'].append([])
        self.papers_data['references'].append([])

        self.current_index = self.current_index + 1

    def add_full_datapoint(self, paper_name, session_name, abstract, authors, full_authors, section_titles, references): #, sections, references):
        self.papers_data['paper_name'].append(paper_name)
        self.papers_data['paper_session'].append(session_name)
        self.papers_data['abstract'].append(abstract)
        self.papers_data['paper_authors'].append(authors)
        self.papers_data['paper_authors_institution'].append(full_authors)
        self.papers_data['section_titles'].append(section_titles)
        self.papers_data['references'].append(references)

    def update_datapoint(self, data_column, data):
        self.papers_data[data_column][self.current_index].append(data)

    def get_data(self):
        return self.papers_data

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
