# INFO: main:CombinedMultiDict([ImmutableMultiDict([]), ImmutableMultiDict(
#     [('AccountSid', 'ACc0866e24af5ee9d35ee8cb71156f571f'), ('ApiVersion', '2010-04-01'),
#      ('CallSid', 'CA837880d17d7b73173c08b0768b2888ff'), ('CallStatus', 'in-progress'), ('Called', '+18445490474'),
#      ('CalledCity', ''), ('CalledCountry', 'US'), ('CalledState', ''), ('CalledZip', ''), ('Caller', '+16199483103'),
#      ('CallerCity', 'CHULA VISTA'), ('CallerCountry', 'US'), ('CallerState', 'CA'), ('CallerZip', '91913'),
#      ('Confidence', '0.6121141'), ('Direction', 'inbound'), ('From', '+16199483103'), ('FromCity', 'CHULA VISTA'),
#      ('FromCountry', 'US'), ('FromState', 'CA'), ('FromZip', '91913'), ('Language', 'en-US'), ('SpeechResult', 'Yes.'),
#      ('To', '+18445490474'), ('ToCity', ''), ('ToCountry', 'US'), ('ToState', ''), ('ToZip', '')])])
from datetime import timedelta, date

from doctor_availability import DoctorAvailability


def get_caller_number(multidict):
    return multidict['Caller']


# def randomize_appointment_days():
#     date1 = fake_appointment(date.today() + timedelta(days=7))
#     date2 = fake_appointment(date.today() + timedelta(days=8))
#     date3 = fake_appointment(date.today() + timedelta(days=9))
#     return [date1, date2, date3]
#
#
# def fake_appointment(end_date):
#     """ fake date at 1pm """
#     return end_date.strftime("%A") + " " \
#         + end_date.strftime("%B") + " " \
#         + end_date.strftime("%d") + " " \
#         + "at 1 pm PST"


def generate_availability(assessment):
    """ FAKE GENERATION OF AVAIL DOCTORS AND TIMES """
    d1 = DoctorAvailability('Dr. Kenny Smith', "August 21 at 1:00pm PST")
    d2 = DoctorAvailability("Dr. John Doe", "August 22 at 2:00pm PST")
    d3 = DoctorAvailability("Dr. Penny Halligan", "August 23 at 3:00pm PST")
    assessment.available_doctors = [d1, d2, d3]
