class Assessment:
    def __init__(self, name=None, dob=None, payerName=None, payerId=None, haveReferral=None, referral=None,
                 reason=None, demographics=None, contact=None, doctor=None, available_doctors=None, appointment_time=None):
        self.name = name
        self.dob = dob
        self.payer_name = payerName
        self.payer_id = payerId
        self.haveReferral = haveReferral
        self.referral = referral
        self.reason = reason
        self.demographics = demographics
        self.contact = contact
        self.doctor = doctor
        self.appointment_time = appointment_time
        self.available_doctors = available_doctors
