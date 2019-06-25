# -*- coding: utf-8 -*-
#BEGIN_HEADER
import os
import time
from installed_clients.RunTesterClient import RunTester as RTC
#END_HEADER


class RunTester:
    '''
    Module Name:
    RunTester

    Module Description:
    A KBase module: RunTester
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = ""
    GIT_COMMIT_HASH = ""

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        #END_CONSTRUCTOR
        pass


    def run_RunTester(self, ctx, params):
        """
        This example function accepts any number of parameters and returns results in a KBaseReport
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_RunTester
        depth = params['depth']
        parallel = params.get('parallel', 1)
        size = params.get('size', 0)
        print("Depth = %d" % (depth))
        depth -= 1
        if depth > 0:
            rtc = RTC(url=self.callback_url)
            if parallel==1:
               rtc.run_RunTester({'depth': depth, 'size': size})
            else:
                jobs = []
                for i in range(1, parallel):
                   print("Submiting thread %d" % (i))
                   id=rtc._run_RunTester_submit({'depth': depth, 'size': size})
                   print(id)
                   jobs.append(id)
                while len(jobs):
                    time.sleep(1)
                    for job_id in jobs: 
                       job_state = rtc._check_job(job_id)
                       if job_state['finished']:
                          jobs.remove(job_id)


        name='bogus'
        prov = ctx.provenance()
        print(prov)
        if size > 0:
             name = 'x' * size

        output = {
            'report_name': name
        }
        #END run_RunTester

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_RunTester return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]