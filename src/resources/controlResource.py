from flask_restful import Resource, Api, reqparse, abort
from flask_restplus import inputs
import os
import signal
import psutil
import re
import time
import sys
import requests

examples = [
    {
        'id': 1,
        'data': 'data1'
    }
]

class ControlList(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        #self.parser.add_argument('data', type=str, required=True, help='No data provided', location='json')
        self.parser.add_argument('pollStatus', type=inputs.boolean, default=False, required=False, location='args')
        self.parser.add_argument('changeStatus', type=str, default=False, required=False, location='args')
        self.parser.add_argument('queueServer', type=str, default=False, required=False, location='args')
        self.parser.add_argument('opalServer', type=str, default=False, required=False, location='args')
        self.parser.add_argument('resetQueue', type=str, default=False, required=False, location='args')
        super(ControlList, self).__init__()

    def get(self):

        args = self.parser.parse_args()
        if args['pollStatus']:
           return {"status": self.get_poll_active()}

        regex = '.*python*'
        process_dicts = self.get_process_by_cmd_regex(regex)
             
        return process_dicts

    def delete(self):
        args = self.parser.parse_args()
        if args['resetQueue']:
            request = 'https://' + args['queueServer']
            res = requests.get(request, params={'resetQueue': True}, verify=False)
            return "queue reset", 200

        if self.get_poll_active() == False:
            return {"status": False}

        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=['pid', 'cmdline', 'name', 'username'])
            except psutil.NoSuchProcess:
                pass
            else:

                cur_cmdline = pinfo['cmdline']

                r = re.compile('.*ds_poll.py*')
                if any(r.match(line) for line in cur_cmdline):
                    proc.kill()
                    return {"status": False}

        return {"status": False}

    def post(self):
        args = self.parser.parse_args()

        pollActive = self.get_poll_active()

        queue_server = args['queueServer'] if args['queueServer'] else 'queue_server:8001'
        opal_server = args['opalServer'] if args['opalServer'] else 'datashield_opal:8443'

        if not pollActive:
            proc = psutil.Popen(['python3', '/root/ds_poll/ds_poll.py' ,'-q' ,queue_server ,'-o', opal_server , '-s','-v'], cwd='/root/ds_poll')
            time.sleep(2)
            return {"status": self.get_poll_active()} 

        return {"status": self.get_poll_active()}, 201

    def get_process_by_cmd_regex(self, regex):
        process_dicts = []

        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=['pid', 'cmdline', 'name', 'username'])
            except psutil.NoSuchProcess:
                pass
            else:
                cur_cmdline = pinfo['cmdline']
                r = re.compile(regex)
                if any(r.match(line) for line in cur_cmdline):
                    process_dict = {"id": pinfo['pid'], "cmd": cur_cmdline }
                    process_dicts.append(process_dict)
        
        return process_dicts


    def get_poll_active(self):
        regex = '.*ds_poll.py'
        process_dicts = self.get_process_by_cmd_regex(regex)
        return bool(process_dicts)
    

class Control(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('data', type=str, required=True, help='No data provided', location='json')
        super(Control, self).__init__()

    def abort_if_example_doesnt_exist(self, example_id):
        if example_id not in examples:
            abort(404, message="example {} doesn't exist".format(example_id))

    def get(self, example_id):
        example = [x for x in examples if x['id'] == example_id]
        if len(example) == 0:
            self.abort_if_example_doesnt_exist(example_id)
        return example

    def delete(self, example_id):
        example = [x for x in examples if x['id'] == example_id]
        if len(example) == 0:
            self.abort_if_example_doesnt_exist(example_id)
        examples.remove(example[0])
        return {'result': True}, 204

    def put(self, example_id):
        example = [x for x in examples if x['id'] == example_id]
        if len(example) == 0:
            self.abort_if_example_doesnt_exist(example_id)
        example = example[0]
        args = self.parser.parse_args()
        for k, v in args.items():
            if v is not None:
                example[k] = v
        return example, 201

