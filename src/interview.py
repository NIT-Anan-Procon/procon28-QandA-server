
class InterviewRecord:
    def __init__(self, question, answer):
        """
        question : text
        answer : text
        """
        self.question = question
        self.answer = answer


class InterviewData:
    def __init__(self, patient_id, date, latlng, interview_scenario_id, interview_record_texts, treat_ids, treat_ids_recommend):
        """
        patient_id : int
        date : string '%Y年%m月%d日 %H時%M分'
        latlng : [float]
        interview_scenario_id : int
        interview_records_text : [text]
        treat_ids : [int]
        treat_ids_recommend : [int]
        """

        self.patient_id = patient_id
        self.date = date
        self.latlng = latlng
        self.interview_scenario_id = interview_scenario_id
        self.interview_records = convert_interviewrecord(interview_record_texts)
        self.treat_ids = treat_ids
        self.treat_ids_recommend = treat_ids_recommend

    def convert_interviewrecord(self, interview_records_text):
        interview_records = []
        for interview_record_text in interview_record_texts:
            interview_records.append(interview_record_text.split(":"))
        return interview_records

    def get_dict(self):
        interview_dict = {
            "patient_id" : self.patient_id,
            "date" : self.date,
            "latlng" : latlng,
            "interview_scenario_id" : self.interview_scenario_id,
            "interview_records" : self.interview_records,
            "treat_ids" : self.treat_ids,
            "treat_ids_recommend" : self.treat_ids_recommend,
        }

        return interview_dict
