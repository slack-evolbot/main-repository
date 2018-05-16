import sys
import urllib.request
import json
import os

APP_URL = 'https://api.apigw.smt.docomo.ne.jp/dialogue/v1/dialogue'

class DocomoChat(object):
    context_info = 'DUMMY'
    mode_info = 'dialog'
    
    def __init__(self, api_key, context, mode):
        api_key = os.environ.get('DOCOMO_DIALOGUE_API_KEY', api_key)
        super(DocomoChat, self).__init__()
        self.api_url = APP_URL + ('?APIKEY=%s' % api_key)
        self.context, self.mode = context, mode

    def __send_message(self, input_message = '', custom_dict = None):
        req_data = {'utt': input_message}
        if self.context:
            req_data['context'] = self.context
        if self.mode:
            req_data['mode'] = self.mode
        if custom_dict:
            req_data.update(custom_dict)
        request = urllib.request.Request(self.api_url,
                                         data = json.dumps(req_data).encode('utf-8'))
        request.add_header('Content-Type', 'application/json')
        try:
            response = urllib.request.urlopen(request)
        except Exception as e:
            print(e)
            sys.exit()
        return response

    def __process_response(self, response):
        resp_json = json.loads(response.read().decode("utf-8"))
        self.context = resp_json['context']
        self.mode    = resp_json['mode']
        return resp_json['utt'], self.context, self.mode

    def send_and_get(self, input_message):
        response = self.__send_message(input_message)
        received_message, received_context, received_mode = self.__process_response(response)
        return received_message, received_context, received_mode

def main(message, context, mode):
    api_key = '664a7059443847546d446a6f3761526b386f4d424b425568657146664a32455a33417164644d4371437444'
    chat = DocomoChat(api_key, context, mode)
    resp, context, mode = chat.send_and_get(message)

    return resp, context, mode

if __name__ == "__main__":
    main()
