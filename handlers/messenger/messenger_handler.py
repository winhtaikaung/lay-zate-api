#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
from _blake2 import blake2b

import os
import re
import requests
import tornado
from tornado import gen

from const import QUESTIONS_PAYLOAD, ABOUT_MORE_PAYLOAD, CHECK_PP_PAYLOAD, INITIAL_QUICK_REPLY, ABOUT_QUICK_REPLY, \
    CHECK_AGAIN_POSITIVE_PAYLOAD, CHECK_AGAIN_NEGATIVE_PAYLOAD, RESTART_QUICK_REPLY, CHECK_AGAIN_QUICK_REPLY, \
    ABOUT_PAGE_PAYLOAD, PRIVACY_POLICY_PAYLOAD, LICENSE_PAYLOAD
from const.messages import MSG_INITIAL_GREETING, MSG_GOOD_BYE, MSG_PP_CHECK_INSTRUCTION, MSG_WELL_PRESS_BELOW, \
    MSG_ABOUT_US, MSG_PRIVACY_POLICY, MSG_LICENSE, MSG_INVALID_PP_NO
from db.user_repo import UserRepository
from handlers.base_handler import BaseHandler
from scraper.mom_scraper import MOMScrapper
from utils.messenger_template_util import send_list_templates, send_quick_reply, send_typing_off, \
    send_typing_on


class MessengerHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def get(self, params):
        if self.get_argument("hub.mode") == "subscribe" and self.get_argument("hub.challenge"):
            if not self.get_argument("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
                return self.send_error({}, 403)
            print("BOT HANDSHAKE complete")
            return self.write(self.get_argument("hub.challenge"))

    @tornado.web.asynchronous
    @gen.engine
    def post(self, action):
        msg_body = json.loads(self.request.body)
        # merchant_repo = merchant_repository.MerchantRepository()
        user_repo = UserRepository()
        mom_scrapper = MOMScrapper
        # messenger_model = MessengerModel(mom_scrapper, user_repo)

        # messenger_model.chat_automated_response(msg_body)
        if msg_body["object"] == "page":
            for entry in msg_body["entry"]:
                if entry.get("messaging"):
                    for messaging_event in entry["messaging"]:
                        sender_id = messaging_event["sender"]["id"]
                        recipient_id = messaging_event["recipient"]["id"]

                        if messaging_event.get("message"):
                            send_typing_on(recipient_id=sender_id)
                            if messaging_event["message"].get("text"):

                                if messaging_event["message"].get("quick_reply"):
                                    """
                                    HERE IS quick Reply Area
                                    """
                                    payload = messaging_event["message"]["quick_reply"]["payload"]

                                    if payload == QUESTIONS_PAYLOAD:
                                        response = {}
                                        # yield gen.Task(merchant_repo.get_random_merchants, 5)
                                        send_list_templates(sender_id, response)
                                    elif payload == CHECK_PP_PAYLOAD:
                                        # Send CHECK Passport response and give chance to user to type in
                                        send_quick_reply(sender_id,
                                                         MSG_PP_CHECK_INSTRUCTION,
                                                         RESTART_QUICK_REPLY)
                                    elif payload == ABOUT_MORE_PAYLOAD:
                                        # Send about response
                                        send_quick_reply(sender_id, MSG_WELL_PRESS_BELOW, ABOUT_QUICK_REPLY)
                                    elif payload == ABOUT_PAGE_PAYLOAD:
                                        send_quick_reply(sender_id, MSG_ABOUT_US, ABOUT_QUICK_REPLY)
                                    elif payload == PRIVACY_POLICY_PAYLOAD:
                                        send_quick_reply(sender_id, MSG_PRIVACY_POLICY, ABOUT_QUICK_REPLY)
                                    elif payload == LICENSE_PAYLOAD:
                                        send_quick_reply(sender_id, MSG_LICENSE, ABOUT_QUICK_REPLY)
                                    elif payload == CHECK_AGAIN_POSITIVE_PAYLOAD:
                                        send_quick_reply(sender_id,
                                                         MSG_PP_CHECK_INSTRUCTION,
                                                         CHECK_AGAIN_QUICK_REPLY)
                                    elif payload == CHECK_AGAIN_NEGATIVE_PAYLOAD:
                                        send_quick_reply(sender_id,
                                                         MSG_GOOD_BYE,
                                                         INITIAL_QUICK_REPLY)
                                else:
                                    message_text = messaging_event["message"]["text"]
                                    match_obj = re.match('^(?!^0+$)[a-zA-Z0-9]{3,20}$',
                                                         str(message_text).strip().replace(" ", ""), re.M | re.I)
                                    if match_obj:
                                        mom_param = {'travelDocNo': str(message_text).strip().replace(" ", "")}
                                        mom_request = requests.post(os.environ["MOM_URL"], mom_param)
                                        response = yield gen.Task(mom_scrapper.get_scrapped_result, self,
                                                                  mom_request.content)

                                        # response = yield gen.Task(mom_scrapper.get_scrapped_result, self,
                                        #                           os.environ["MOM_SUCCESS_RESPONSE"])
                                        # save user_data
                                        if response["meta"]["code"] is 200:
                                            yield gen.Task(user_repo.upsert_user, sender_id,
                                                           response["data"]["pass_type"],
                                                           blake2b(str(response["data"]["fin"]).encode(
                                                               "utf8")).hexdigest(),
                                                           blake2b(str(message_text).strip().replace(" ",
                                                                                                     "").upper().encode(
                                                               "utf8")).hexdigest(),
                                                           response["data"]["status"],
                                                           response["data"]["date_of_application"])
                                        send_quick_reply(sender_id,
                                                         response["meta"]["message"],
                                                         CHECK_AGAIN_QUICK_REPLY)
                                    else:
                                        # Invalid Passport Number
                                        send_quick_reply(sender_id,
                                                         MSG_INVALID_PP_NO,
                                                         CHECK_AGAIN_QUICK_REPLY)
                                send_typing_off(recipient_id=sender_id)

                        if messaging_event.get("delivery"):  # delivery confirmation
                            pass

                        if messaging_event.get("optin"):  # optin confirmation
                            pass

                        if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                            if messaging_event["postback"]["payload"] == "GET_STARTED_PAYLOAD":
                                send_quick_reply(sender_id,
                                                 MSG_INITIAL_GREETING, INITIAL_QUICK_REPLY)
                            pass
                elif entry.get("postback"):
                    print("callback")
                    pass

        self.respond({}, 200)
