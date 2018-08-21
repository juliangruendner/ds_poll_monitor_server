from flask_restful import Resource, Api, reqparse, abort
import os
import signal
import psutil
import re

examples = [
    {
        'id': 1,
        'data': 'data1'
    }
]

class ControlList(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('data', type=str, required=True, help='No data provided', location='json')
        super(ControlList, self).__init__()

    def get(self):

        process_dicts = []

        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=['pid', 'cmdline', 'name', 'username'])
            except psutil.NoSuchProcess:
                pass
            else:

                cur_cmdline = pinfo['cmdline']

                r = re.compile('.*python.*')
                if any(r.match(line) for line in cur_cmdline):
                    process_dict = {"pid": pinfo['pid'], "cmd_line": cur_cmdline }
                    process_dicts.append(process_dict)
        
                    
        return process_dicts

    def delete(self):

        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=['pid', 'cmdline', 'name', 'username'])
            except psutil.NoSuchProcess:
                pass
            else:

                cur_cmdline = pinfo['cmdline']

                r = re.compile('.*python.*')
                if any(r.match(line) for line in cur_cmdline):
                    print(pinfo['pid'])
                    print(cur_cmdline)

        return "poll killed muhahaha"

    def post(self):
        args = self.parser.parse_args()
        example = {
            'id': examples[-1]['id'] + 1,
            'data': args['data']
        }
        examples.append(example)
        return example, 201

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