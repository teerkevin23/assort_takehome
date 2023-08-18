# from deepgram import Deepgram
from flask import Flask, jsonify, request
from threading import Thread
from twilio.twiml.voice_response import VoiceResponse, Gather

# from assistant import Assistant
from asssessment import Assessment

# import asyncio
# import aiohttp
import logging

from utilities import get_caller_number, generate_availability
from sms import send_sms

# Example filename: deepgram_test.py
app = Flask(__name__)
ASSESSMENT = Assessment()
logging.basicConfig(level=logging.DEBUG)

# URL for the realtime streaming audio you would like to transcribe
# URL = 'http://stream.live.vc.bbcmedia.co.uk/bbc_world_service'

# @app.route("/", methods=['GET'])
# def home():
#     print("hello world home")
#     # run all async stuff in another thread
#     th = Thread(target=async_main_wrapper)
#     th.start()
#
#     resp = jsonify(success=True)
#     return resp


@app.route("/name", methods=['POST'])
def name():
    resp = VoiceResponse()
    resp.say("Hello. Thanks for calling Assort Health.", voice='Polly.Amy')
    gather = Gather(input="speech", timeout="6", action='/action/name')
    gather.say("What is your first and last name?", voice='Polly.Amy')
    resp.append(gather)

    resp.redirect('/name')
    return str(resp)


@app.route("/action/name", methods=['GET', 'POST'])
def set_name():
    """Processes results from the <Gather> prompt in /name"""
    resp = VoiceResponse()
    if 'SpeechResult' in request.values:
        fullname = request.values['SpeechResult']
        ASSESSMENT.name = fullname
        app.logger.info("Got SpeechResult for {subject}: {name}"
                        .format(subject='name', name={fullname}))
        app.logger.debug(request.values)

        resp.redirect('/dob', method='POST')
    else:
        resp.say("Oops, I did not catch that.", voice='Polly.Amy')
        resp.redirect('/name')

    return str(resp)


@app.route("/dob", methods=['POST'])
def dob():
    resp = VoiceResponse()

    gather = Gather(input="speech", timeout="6", action='/action/dob')
    gather.say("What is your date of birth?", voice='Polly.Amy')
    resp.append(gather)

    resp.redirect('/dob')
    return str(resp)


@app.route("/action/dob", methods=['POST'])
def set_dob():
    """Processes results from the <Gather> prompt in /dob"""
    resp = VoiceResponse()
    if 'SpeechResult' in request.values:
        dob = request.values['SpeechResult']
        ASSESSMENT.dob = dob

        app.logger.info("Got SpeechResult for {subject}: {dob}"
                        .format(subject='dob', dob={dob}))
        app.logger.debug(request.values)

        resp.redirect('/haveReferral')
    else:
        resp.say("Oops, I did not catch that.", voice='Polly.Amy')
        resp.redirect('/dob')

    return str(resp)


@app.route("/haveReferral", methods=['POST'])
def have_referral():
    resp = VoiceResponse()

    gather = Gather(input="speech", timeout="4", action='/action/haveReferral')
    gather.say("Do you have a referral?", voice='Polly.Amy')
    resp.append(gather)

    resp.redirect('/haveReferral')
    return str(resp)


@app.route("/action/haveReferral", methods=['POST'])
def set_have_referral():
    """Processes results from the <Gather> prompt in /haveReferral"""
    yes_utterances = ['Yup', 'Yes', 'Yeah', 'Yup.', 'Yes.', 'Yeah.']
    resp = VoiceResponse()
    if 'SpeechResult' in request.values:
        have_referral_answer = request.values['SpeechResult']
        ASSESSMENT.haveReferral = have_referral_answer
        app.logger.info("Got SpeechResult for {subject}: {have_referral_answer}"
                        .format(subject='haveReferral', have_referral_answer={have_referral_answer}))
        app.logger.debug(request.values)

        if have_referral_answer in yes_utterances:
            app.logger.info("...gathering referral information")
            resp.redirect('/referral')
        else:
            app.logger.info("...skipping referral information")
            resp.redirect('/reason')
    else:
        resp.say("Oops, I did not catch that.", voice='Polly.Amy')
        resp.redirect('/haveReferral')

    return str(resp)


@app.route("/referral", methods=['POST'])
def referral():
    resp = VoiceResponse()

    gather = Gather(input="speech", timeout="5", action='/action/referral')
    gather.say("What is your doctors name?", voice='Polly.Amy')
    resp.append(gather)

    resp.redirect('/referral')
    return str(resp)


@app.route("/action/referral", methods=['POST'])
def set_referral():
    """Processes results from the <Gather> prompt in /referral"""
    resp = VoiceResponse()
    if 'SpeechResult' in request.values:
        referral_name = request.values['SpeechResult']
        ASSESSMENT.referral = referral_name
        app.logger.info("Got SpeechResult for {subject}: {referral}"
                        .format(subject='referral', referral={referral_name}))
        app.logger.debug(request.values)

        resp.redirect('/reason')
    else:
        resp.say("Oops, I did not catch that.", voice='Polly.Amy')
        resp.redirect('/referral')

    return str(resp)


@app.route("/reason", methods=['POST'])
def medical_reason():
    resp = VoiceResponse()

    gather = Gather(input="speech", timeout="6", action='/action/reason')
    gather.say("What is the reason for your appointment?", voice='Polly.Amy')
    resp.append(gather)

    resp.redirect('/reason')
    return str(resp)


@app.route("/action/reason", methods=['POST'])
def set_medical_reason():
    """Processes results from the <Gather> prompt in /reason"""
    resp = VoiceResponse()
    if 'SpeechResult' in request.values:
        reason = request.values['SpeechResult']
        ASSESSMENT.reason = reason
        app.logger.info("Got SpeechResult for {subject}: {reason}"
                        .format(subject='reason', reason={reason}))
        app.logger.debug(request.values)

        resp.redirect('/demographics')
    else:
        resp.say("Oops, I did not catch that.", voice='Polly.Amy')
        resp.redirect('/reason')

    return str(resp)


@app.route("/demographics", methods=['POST'])
def demographics():
    resp = VoiceResponse()

    gather = Gather(input="speech", timeout="7", action='/action/demographics')
    gather.say("What is your current address on file?", voice='Polly.Amy')
    resp.append(gather)

    resp.redirect('/demographics')
    return str(resp)


@app.route("/action/demographics", methods=['POST'])
def set_demographics():
    """Processes results from the <Gather> prompt in /demographics"""
    resp = VoiceResponse()
    if 'SpeechResult' in request.values:
        address = request.values['SpeechResult']
        ASSESSMENT.demographics = address
        app.logger.info("Got SpeechResult for {subject}: {demographics}"
                        .format(subject='demographics', demographics={address}))
        app.logger.debug(request.values)

        resp.redirect('/contact')
    else:
        resp.say("Oops, I did not catch that.", voice='Polly.Amy')
        resp.redirect('/demographics')

    return str(resp)


@app.route("/contact", methods=['POST'])
def contact():
    resp = VoiceResponse()

    gather = Gather(input="speech", timeout="7", action='/action/contact')
    gather.say("What is the best phone number to contact you by?", voice='Polly.Amy')
    resp.append(gather)

    resp.redirect('/contact')
    return str(resp)


@app.route("/action/contact", methods=['POST'])
def set_contact():
    """Processes results from the <Gather> prompt in /contact"""
    resp = VoiceResponse()
    if 'SpeechResult' in request.values:
        number = request.values['SpeechResult']
        ASSESSMENT.contact = number

        app.logger.info("Got SpeechResult for {subject}: {contact}"
                        .format(subject='contact', contact={number}))
        app.logger.debug(request.values)

        resp.redirect('/appointments')
    else:
        resp.say("Oops, I did not catch that number.", voice='Polly.Amy')
        resp.redirect('/contact')

    return str(resp)


@app.route("/appointments", methods=['POST'])
def offer_appointments():
    resp = VoiceResponse()
    gather = Gather(num_digits=1, action='/action/appointments')
    generate_availability(ASSESSMENT)
    for index, appointment in enumerate(ASSESSMENT.available_doctors):
        doctor = appointment.name
        time = appointment.time
        gather.say("We have availability at " + time + " with " + doctor, voice='Polly.Amy')
        gather.say("press {number}".format(number=index+1), voice='Polly.Amy')

    resp.append(gather)

    resp.redirect('/appointments')
    return str(resp)


@app.route("/action/appointments", methods=['POST'])
def set_appointments():
    resp = VoiceResponse()
    if 'Digits' in request.values:
        choice = request.values['Digits']
        phoneNumber = get_caller_number(request.values)

        if choice == '1':
            availability = ASSESSMENT.available_doctors[0]
            ASSESSMENT.doctor = availability.name
            ASSESSMENT.appointment_time = availability.time
            resp.say('You chose {doctor} at {time}'.format(doctor=availability.name, time=availability.time), voice='Polly.Amy')
            completed_assessment(phoneNumber, ASSESSMENT)
            return str(resp)
        elif choice == '2':
            availability = ASSESSMENT.available_doctors[1]
            ASSESSMENT.doctor = availability.name
            ASSESSMENT.appointment_time = availability.time
            resp.say('You chose {doctor} at {time}'.format(doctor=availability.name, time=availability.time), voice='Polly.Amy')
            completed_assessment(phoneNumber, ASSESSMENT)
            return str(resp)
        elif choice == '3':
            availability = ASSESSMENT.available_doctors[2]
            ASSESSMENT.doctor = availability.name
            ASSESSMENT.appointment_time = availability.time
            resp.say('You chose {doctor} at {time}'.format(doctor=availability.name, time=availability.time), voice='Polly.Amy')
            completed_assessment(phoneNumber, ASSESSMENT)
            return str(resp)
        else:
            # If the caller didn't choose 1, 2, or 3 apologize and assign
            resp.say("Sorry, I don't understand. We will assign an appointment for you.")
            availability = ASSESSMENT.available_doctors[2]
            ASSESSMENT.doctor = availability.name
            ASSESSMENT.time = availability.time
            completed_assessment(phoneNumber, ASSESSMENT)
    else:
        resp.redirect('/appointments')

    return str(resp)


def completed_assessment(phoneNumber, assessment):
    print(assessment.name, assessment.referral, assessment.demographics)
    app.logger.info(assessment)
    print(vars(assessment))
    app.logger.info(vars(assessment))
    return send_sms(phoneNumber, assessment)


# async def main():
#     # Initialize the Deepgram SDK
#     deepgram = Deepgram(DEEPGRAM_API_KEY)
#
#     # Create a websocket connection to Deepgram
#     # In this example, punctuation is turned on, interim results are turned off, and language is set to UK English.
#     try:
#         deepgramLive = await deepgram.transcription.live({
#             'smart_format': True,
#             'interim_results': False,
#             'language': 'en-US',
#             'model': 'nova',
#         })
#     except Exception as e:
#         print(f'Could not open socket: {e}')
#         return
#
#     # Listen for the connection to close
#     deepgramLive.registerHandler(deepgramLive.event.CLOSE, lambda c: print(f'Connection closed with code {c}.'))
#
#     # Listen for any transcripts received from Deepgram and write them to the console
#     deepgramLive.registerHandler(deepgramLive.event.TRANSCRIPT_RECEIVED, print)
#
#     # Listen for the connection to open and send streaming audio from the URL to Deepgram
#     async with aiohttp.ClientSession() as session:
#         async with session.get(URL) as audio:
#             assessment = Assessment()
#             assistant = Assistant(assessment)
#             # assistant.resolve()
#
#             task_1 = asyncio.create_task(assistant.resolve())
#             # await asyncio.wait([task_1])
#
#             # t1 = multiprocessing.Process(target=assistant.resolve())
#             # t1.start()
#             # print('start')
#             # t1.join()
#             # print('join')
#             #
#             # print('awaiaint data')
#             while True:
#
#                 data = await audio.content.readany()
#                 deepgramLive.send(data)
#
#                 # If no data is being sent from the live stream, then break out of the loop.
#                 if not data:
#                     break
#
#     # Indicate that we've finished sending data by sending the customary zero-byte message to the Deepgram streaming endpoint, and wait until we get back the final summary metadata object
#     await deepgramLive.finish()


# def async_main_wrapper():
#     """Not async Wrapper around async_main to run it as target function of Thread"""
#     asyncio.run(main())


if __name__ == "__main__":
    app.logger.info("...starting server")
    app.run(port=5002, debug=True)
    # th = Thread(target=async_main_wrapper)
    # th.start()
    # th.join()
    # resp = jsonify(success=True)
    # return resp

# import asyncio
# import base64
# import json
# import sys
# import websockets
# import ssl
# from pydub import AudioSegment
#
# subscribers = {}
#
#
# def deepgram_connect():
#     extra_headers = {
#         'Authorization': '65b287b2d586dcc2ec6febf78d3b4ccf184cbe25'
#     }
#     deepgram_ws = websockets.connect(
#         'wss://api.deepgram.com/v1/listen?encoding=mulaw&sample_rate=8000&channels=2&multichannel=true',
#         extra_headers=extra_headers)
#
#     return deepgram_ws
#
#
# async def twilio_handler(twilio_ws):
#     audio_queue = asyncio.Queue()
#     callsid_queue = asyncio.Queue()
#
#     async with deepgram_connect() as deepgram_ws:
#
#         async def deepgram_sender(deepgram_ws):
#             print('deepgram_sender started')
#             while True:
#                 chunk = await audio_queue.get()
#                 await deepgram_ws.send(chunk)
#
#         async def deepgram_receiver(deepgram_ws):
#             print('deepgram_receiver started')
#             # we will wait until the twilio ws connection figures out the callsid
#             # then we will initialize our subscribers list for this callsid
#             callsid = await callsid_queue.get()
#             subscribers[callsid] = []
#             # for each deepgram result received, forward it on to all
#             # queues subscribed to the twilio callsid
#             async for message in deepgram_ws:
#                 for client in subscribers[callsid]:
#                     client.put_nowait(message)
#
#             # once the twilio call is over, tell all subscribed clients to close
#             # and remove the subscriber list for this callsid
#             for client in subscribers[callsid]:
#                 client.put_nowait('close')
#
#             del subscribers[callsid]
#
#         async def twilio_receiver(twilio_ws):
#             print('twilio_receiver started')
#             # twilio sends audio data as 160 byte messages containing 20ms of audio each
#             # we will buffer 20 twilio messages corresponding to 0.4 seconds of audio to improve throughput performance
#             BUFFER_SIZE = 20 * 160
#             # the algorithm to deal with mixing the two channels is somewhat complex
#             # here we implement an algorithm which fills in silence for channels if that channel is either
#             #   A) not currently streaming (e.g. the outbound channel when the inbound channel starts ringing it)
#             #   B) packets are dropped (this happens, and sometimes the timestamps which come back for subsequent packets are not aligned)
#             inbuffer = bytearray(b'')
#             outbuffer = bytearray(b'')
#             inbound_chunks_started = False
#             outbound_chunks_started = False
#             latest_inbound_timestamp = 0
#             latest_outbound_timestamp = 0
#             async for message in twilio_ws:
#                 try:
#                     data = json.loads(message)
#                     if data['event'] == 'start':
#                         start = data['start']
#                         callsid = start['callSid']
#                         callsid_queue.put_nowait(callsid)
#                     if data['event'] == 'connected':
#                         continue
#                     if data['event'] == 'media':
#                         media = data['media']
#                         chunk = base64.b64decode(media['payload'])
#                         if media['track'] == 'inbound':
#                             # fills in silence if there have been dropped packets
#                             if inbound_chunks_started:
#                                 if latest_inbound_timestamp + 20 < int(media['timestamp']):
#                                     bytes_to_fill = 8 * (int(media['timestamp']) - (latest_inbound_timestamp + 20))
#                                     # NOTE: 0xff is silence for mulaw audio
#                                     # and there are 8 bytes per ms of data for our format (8 bit, 8000 Hz)
#                                     inbuffer.extend(b'\xff' * bytes_to_fill)
#                             else:
#                                 # make it known that inbound chunks have started arriving
#                                 inbound_chunks_started = True
#                                 latest_inbound_timestamp = int(media['timestamp'])
#                                 # this basically sets the starting point for outbound timestamps
#                                 latest_outbound_timestamp = int(media['timestamp']) - 20
#                             latest_inbound_timestamp = int(media['timestamp'])
#                             # extend the inbound audio buffer with data
#                             inbuffer.extend(chunk)
#                         if media['track'] == 'outbound':
#                             # make it known that outbound chunks have started arriving
#                             outbound_chunked_started = True
#                             # fills in silence if there have been dropped packets
#                             if latest_outbound_timestamp + 20 < int(media['timestamp']):
#                                 bytes_to_fill = 8 * (int(media['timestamp']) - (latest_outbound_timestamp + 20))
#                                 # NOTE: 0xff is silence for mulaw audio
#                                 # and there are 8 bytes per ms of data for our format (8 bit, 8000 Hz)
#                                 outbuffer.extend(b'\xff' * bytes_to_fill)
#                             latest_outbound_timestamp = int(media['timestamp'])
#                             # extend the outbound audio buffer with data
#                             outbuffer.extend(chunk)
#                     if data['event'] == 'stop':
#                         break
#
#                     # check if our buffer is ready to send to our audio_queue (and, thus, then to deepgram)
#                     while len(inbuffer) >= BUFFER_SIZE and len(outbuffer) >= BUFFER_SIZE:
#                         asinbound = AudioSegment(inbuffer[:BUFFER_SIZE], sample_width=1, frame_rate=8000, channels=1)
#                         asoutbound = AudioSegment(outbuffer[:BUFFER_SIZE], sample_width=1, frame_rate=8000, channels=1)
#                         mixed = AudioSegment.from_mono_audiosegments(asinbound, asoutbound)
#
#                         # sending to deepgram via the audio_queue
#                         audio_queue.put_nowait(mixed.raw_data)
#
#                         # clearing buffers
#                         inbuffer = inbuffer[BUFFER_SIZE:]
#                         outbuffer = outbuffer[BUFFER_SIZE:]
#                 except:
#                     break
#
#             # the async for loop will end if the ws connection from twilio dies
#             # and if this happens, we should forward an empty byte to deepgram
#             # to signal deepgram to send back remaining messages before closing
#             audio_queue.put_nowait(b'')
#
#         await asyncio.wait([
#             asyncio.ensure_future(deepgram_sender(deepgram_ws)),
#             asyncio.ensure_future(deepgram_receiver(deepgram_ws)),
#             asyncio.ensure_future(twilio_receiver(twilio_ws))
#         ])
#
#         await twilio_ws.close()
#
#
# async def client_handler(client_ws):
#     client_queue = asyncio.Queue()
#
#     # first tell the client all active calls
#     await client_ws.send(json.dumps(list(subscribers.keys())))
#
#     # then recieve from the client which call they would like to subscribe to
#     # and add our client's queue to the subscriber list for that call
#     try:
#         # you may want to parse a proper json input here
#         # instead of grabbing the entire message as the callsid verbatim
#         callsid = await client_ws.recv()
#         callsid = callsid.strip()
#         if callsid in subscribers:
#             subscribers[callsid].append(client_queue)
#         else:
#             await client_ws.close()
#     except:
#         await client_ws.close()
#
#     async def client_sender(client_ws):
#         while True:
#             message = await client_queue.get()
#             if message == 'close':
#                 break
#             try:
#                 await client_ws.send(message)
#             except:
#                 # if there was an error, remove this client queue
#                 subscribers[callsid].remove(client_queue)
#                 break
#
#     await asyncio.wait([
#         asyncio.ensure_future(client_sender(client_ws)),
#     ])
#
#     await client_ws.close()
#
#
# async def router(websocket, path):
#     if path == '/client':
#         print('client connection incoming')
#         await client_handler(websocket)
#     elif path == '/twilio':
#         print('twilio connection incoming')
#         await twilio_handler(websocket)
#
#
# def main():
#     # use this if using ssl
#     # ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
#     # ssl_context.load_cert_chain('cert.pem', 'key.pem')
#     # server = websockets.serve(router, '0.0.0.0', 443, ssl=ssl_context)
#
#     # use this if not using ssl
#     server = websockets.serve(router, 'localhost', 5000)
#
#     asyncio.get_event_loop().run_until_complete(server)
#     asyncio.get_event_loop().run_forever()
#
#
# if __name__ == '__main__':
#     sys.exit(main() or 0)
