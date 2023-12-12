import pandas as pd


class PapersGeneral:

    def __init__(self, dataset_name):
        self.dataset_name = dataset_name
        self.papers_data = {}
        self.papers_data.update({'paper_name': []})  # Week number!
        self.papers_data.update({'paper_session': []})  # Week number!
        self.papers_data.update({'paper_authors': []})  # If supervision in person! (yes. no, canceled)
        self.papers_data.update({'paper_authors_institution': []})  # Motivated data (1-10)
        self.papers_data.update({'abstract': []})  # work done by student/team (1-10)
        self.papers_data.update({'introduction': []})  # How the team worked this week (1-10)
        self.papers_data.update({'related_work': []})  # How the team worked this week (1-10)
        self.papers_data.update({'discussion': []})  # How engaged the student was (1-10)
        self.papers_data.update({'conclusion': []})  # Expressed thoughts (1 -10)
        self.papers_data.update({'body': []})  # Did everyone participated? (1-10)
        self.papers_data.update({'references': []})  # Session generated new ideas? (1-10)

        # New for error handling
        self.busstop_data.update(
            {'used': []})  # We want to verify the error in the data (how many of these validations are used)
        self.busstop_data.update(
            {'indexation': []})  # We want to verify the error in the data (how many of these validations are used)
        self.busstop_data.update({'occupancy_dif': []}) # this is occupancy_leaving - occupancy_arrive

        self.current_index = 0

    def add_datapoint(self, date, time, subtime, day, week, line, direction, going_time, occupancy_arrive, occupancy_leaving,
                      occupancy_rate_sit, occupancy_rate_stand, people_entering, people_leaving, people_entering_corrected,
                      people_leaving_corrected, entering_validation, leaving_validation, entering_validation_corrected,
                      leaving_validation_corrected, sit_cap, stand_cap, faringso, stomlinje):

        if going_time == 'Okänd':
            # print(time[0])
            if time[0] == '0':
                subtime = time[1]
            else:
                subtime = time.split(":")[0]

            going_time = time

        # print(subtime)
        # print(type(subtime))

        line = str(line)

        if line not in self.possible_lines:
            self.possible_lines.append(line)

        self.busstop_data['date'].append(date)  # Week number!
        self.busstop_data['time'].append(time)  # Week number!
        self.busstop_data['sub_time'].append(subtime)  # If supervision in person! (yes. no, canceled)
        self.busstop_data['day'].append(day)  # Motivated data (1-10)
        self.busstop_data['week'].append(week)  # work done by student/team (1-10)
        self.busstop_data['line'].append(line)  # How the team worked this week (1-10)
        self.busstop_data['direction'].append(direction)  # How the team worked this week (1-10)
        self.busstop_data['going_time'].append(going_time)  # How engaged the student was (1-10)
        self.busstop_data['occupancy_arrive'].append(occupancy_arrive)  # Expressed thoughts (1 -10)
        self.busstop_data['occupancy_leaving'].append(occupancy_leaving)  # Did everyone participated? (1-10)
        self.busstop_data['occupancy_rate_sit'].append(occupancy_rate_sit)  # Session generated new ideas? (1-10)
        self.busstop_data['occupancy_rate_stand'].append(occupancy_rate_stand)  # Session generated new ideas? (1-10)
        self.busstop_data['people_entering'].append(people_entering)  # Session generated new ideas? (1-10)
        self.busstop_data['people_leaving'].append(people_leaving)  # Session generated new ideas? (1-10)
        self.busstop_data['people_entering_corrected'].append(people_entering_corrected)  # Session generated new ideas? (1-10)
        self.busstop_data['people_leaving_corrected'].append(people_leaving_corrected)  # Session generated new ideas? (1-10)
        self.busstop_data['people_entering_validation'].append(entering_validation) # Session generated new ideas? (1-10)
        self.busstop_data['people_leaving_validation'].append(leaving_validation)  # Session generated new ideas? (1-10)
        self.busstop_data['people_entering_validation_corrected'].append(entering_validation_corrected)  # Session generated new ideas? (1-10)
        self.busstop_data['people_leaving_validation_corrected'].append(leaving_validation_corrected)  # Session generated new ideas? (1-10)
        self.busstop_data['sit_cap'].append(sit_cap)  # Session generated new ideas? (1-10)
        self.busstop_data['stand_cap'].append(stand_cap)  # Session generated new ideas? (1-10)
        self.busstop_data['faringso'].append(faringso)  # Session generated new ideas? (1-10)
        self.busstop_data['stomlinje'].append(faringso)  # Session generated new ideas? (1-10)
        self.busstop_data['indexation'].append(self.current_index)  # How engaged the student was (1-10)
        self.busstop_data['used'].append(0)  # How engaged the student was (1-10)
        self.busstop_data['occupancy_dif'].append(occupancy_leaving - occupancy_arrive)  # important if higher than 0
        self.current_index = self.current_index + 1

    def update_used(self, index):
        # print(self.busstop_data['validation_tickets'][index])
        # print(self.busstop_data['line'][index])
        # print(self.busstop_data['week'][index])
        # print(self.busstop_data['sub_time'][index])
        # print(self.busstop_data['date'][index])
        self.busstop_data['used'][index] = 1

    def update_used_last_index(self):
        self.busstop_data['used'][self.current_index - 1] = 1

    def get_filtered_data(self, sum : bool, data_frame,  **kwargs):
        for key, value in kwargs.items():
            print(key, value)

        if data_frame is None:
            df = pd.DataFrame(self.busstop_data, columns=self.busstop_data.keys())
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

        if sum :
            print("sum")

            sum = df.sum()
            df = pd.DataFrame(columns=self.busstop_data.keys())
            df = df.append((sum.transpose()), ignore_index=True)
        else:
            print("not sum")

        return df

        # other = []
        # for key, value in kwargs.items()

    def get_data_greater_than(self, sum : bool, data_frame,  **kwargs):
        for key, value in kwargs.items():
            print(key, value)

        if data_frame is None:
            df = pd.DataFrame(self.busstop_data, columns=self.busstop_data.keys())
        else:
            df = data_frame

        query = ' and '.join(['{0}>{1}'.format(key, value) for key, value in kwargs.items()])
        print(query)
        # matched = np.all([df[vn] == vv for vn, vv in kwargs.items()], axis=0)
        # filtered_df = df[matched]
        df = df.query(' and '.join(['{0}>{1}'.format(key, value) for key, value in kwargs.items()]))
        print("okay")

        if sum :
            print("sum")
        else:
            print("not sum")

        df = df.sort_values(by=['date'])
        return df

    def get_data_lesser_than(self, sum : bool, data_frame,  **kwargs):
        for key, value in kwargs.items():
            print(key, value)

        if data_frame is None:
            df = pd.DataFrame(self.busstop_data, columns=self.busstop_data.keys())
        else:
            df = data_frame

        query = ' and '.join(['{0}<{1}'.format(key, value) for key, value in kwargs.items()])
        print(query)
        # matched = np.all([df[vn] == vv for vn, vv in kwargs.items()], axis=0)
        # filtered_df = df[matched]
        df = df.query(' and '.join(['{0}<{1}'.format(key, value) for key, value in kwargs.items()]))
        print("okay")

        if sum :
            print("sum")
        else:
            print("not sum")

        return df

    def get_data_groupby(self, data_frame, groupby: []):

        if data_frame is None:
            df = pd.DataFrame(self.busstop_data, columns=self.busstop_data.keys())
        else:
            df = data_frame

        df = df.groupby(groupby, as_index=False).sum()

        return df

    def get_data_top_k(self, sum : bool, data_frame, k, column):

        if data_frame is None:
            df = pd.DataFrame(self.busstop_data, columns=self.busstop_data.keys())
        else:
            df = data_frame

        df = df.sort_values(by=[column], ascending=False)
        df = df[:k]

        return df
