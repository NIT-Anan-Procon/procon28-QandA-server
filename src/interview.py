
class InterviewRecord:
    def __init__(self, question, answer):
        """
        question : text
        answer : text
        """
        self.question = question
        self.answer = answer


class InterviewData:
    def __init__(self, patient_id, date, state, latlng, interview_scenario_id, interview_record_texts, care_ids, care_ids_recommend):
        """
        patient_id : int
        date : string '%Y年%m月%d日 %H時%M分'
        latlng : text (lat/lng)
        interview_scenario_id : int
        interview_records_text : [text]
        care_ids : [int]
        care_ids_recommend : [int]
        """

        self.patient_id = patient_id
        self.date = date
        self.state = state
        self.latlng = latlng
        self.interview_scenario_id = interview_scenario_id
        self.interview_records = self.convert_interviewrecord(interview_record_texts)
        self.care_ids = care_ids
        self.care_ids_recommend = care_ids_recommend

    def convert_interviewrecord(self, interview_record_texts):
        interview_records = []
        for interview_record_text in interview_record_texts:
            interview_records.append(interview_record_text.split(":"))
        return interview_records

    def get_dict(self):
        interview_dict = {
            "patient_id" : self.patient_id,
            "date" : self.date,
            "state" : self.state,
            "latlng" : self.latlng,
            "interview_scenario_id" : self.interview_scenario_id,
            "interview_records" : self.interview_records,
            "care_ids" : self.care_ids,
            "care_ids_recommend" : self.care_ids_recommend,
        }

        return interview_dict
