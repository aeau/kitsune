import pandas as pd


class CollectedPapers:

    def __init__(self, dataset_name):
        self.dataset_name = dataset_name
        self.papers_data = {}
        self.papers_data.update({'paper_name': []})  # Week number!
        self.papers_data.update({'paper_session': []})  # Week number!
        self.papers_data.update({'paper_authors': [[]]})  # If supervision in person! (yes. no, canceled)
        self.papers_data.update({'paper_authors_institution': [[]]})  # Motivated data (1-10)
        self.papers_data.update({'abstract': []})  # work done by student/team (1-10)
        self.papers_data.update({'section_titles': [[]]})  # work done by student/team (1-10)
        self.papers_data.update({'sections': [[]]})  # work done by student/team (1-10)
        self.papers_data.update({'references': [[]]})  # Session generated new ideas? (1-10)

        self.current_index = -1

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
