# from elevenlabs import clone, generate, play, set_api_key
# import requests
# import logging
# import asyncio
# import asssessment
# from validator import NameValidator
#
#
# class Interaction:
#     def __init__(self, questionId, validator, assessment):
#         self.questionId = questionId
#         self.validator = validator
#         self.assessment = assessment
#         self.response = ""
#         self.errors = 0
#
#     def interact(self):
#         url = "https://api.elevenlabs.io/v1/history/{id}/audio".format(id=self.questionId)
#         headers = {
#             "Accept": "audio/mpeg",
#             "xi-api-key": "057385abc3fd5bd8bac2ca4c5623005f"
#         }
#         response = requests.get(url, headers=headers)
#         play(response.content)
#         # logger.info("Assistant inquired for {questionId}; {errors} errors".format(questionId=self.questionId,errors=self.errors))
#
#         # get response, set it
#
#         self.response = "Kevin Teer and April 29 1993"
#         self.validate()
#
#     def validate(self):
#         try:
#             ok = self.validator.validate(self.response)
#             if not ok:
#                 self.errors += 1
#                 if self.errors >= 3:
#                     # logger.error("Ran into {errors} errors".format(errors=self.errors))
#                     return
#                     # raise Exception("You've provided three bad inputs")
#                 self.interact()
#             else:
#                 self.assessment.name = 'Kevin'
#                 self.assessment.dob = '04/29/1993'
#         except ValueError as e:
#             print(e)
#
#
# class Assistant:
#     def __init__(self, assessment):
#         self.assessment = assessment
#
#     async def resolve(self):
#         if self.assessment.name is None:
#             name_interaction = Interaction('ttNUqTOqqK0TnOwbpQyL', NameValidator(), self.assessment)
#             name_interaction.interact()
#
#         # if self.assessment.dob is None:
#         #     dob_interaction = Interaction('ttNUqTOqqK0TnOwbpQyL', NameAndDOBValidator(), self.assessment)
#         #     dob_interaction.interact()
#         #
#         # if self.assessment.payer_name is None:
#         #     dob_interaction = Interaction('sPX3IXNcM3HTPLaqOOJ7', NameAndDOBValidator(), self.assessment)
#         #     dob_interaction.interact()
#         #
#         # if self.assessment.payer_id is None:
#         #     dob_interaction = Interaction('ttNUqTOqqK0TnOwbpQyL', NameAndDOBValidator(), self.assessment)
#         #     dob_interaction.interact()
#
