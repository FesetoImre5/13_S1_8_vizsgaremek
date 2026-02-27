import json
import unittest
from django.test.runner import DiscoverRunner
from django.test.client import Client

# Patch Django's test client to store responses
original_request = Client.request
def patched_request(self, **kwargs):
    response = original_request(self, **kwargs)
    if not hasattr(self, '_api_responses'):
        self._api_responses = []
    
    try:
        content = response.json()
    except Exception:
        try:
            content = getattr(response, 'content', b'').decode('utf-8', errors='replace')
        except Exception:
            content = str(getattr(response, 'content', ''))
            
    self._api_responses.append({
        "status_code": response.status_code,
        "content": content
    })
    return response

Client.request = patched_request

class JsonTestResult(unittest.TextTestResult):
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.json_data = []

    def startTest(self, test):
        super().startTest(test)
        # Clear previous responses for this test's client
        client = getattr(test, 'client', None)
        if client:
            client._api_responses = []

    def get_test_name(self, test):
        return test.id()

    def _get_api_message(self, test, error_msg=""):
        responses = []
        try:
            client = getattr(test, 'client', None)
            if client and hasattr(client, '_api_responses'):
                if len(client._api_responses) == 1:
                    resp = client._api_responses[0]
                    responses = resp['content']
                    if not responses and resp['status_code'] == 204:
                        responses = "API returned 204 No Content (Successful empty response)."
                elif len(client._api_responses) > 1:
                    responses = []
                    for r in client._api_responses:
                        if not r['content'] and r['status_code'] == 204:
                            responses.append("API returned 204 No Content")
                        else:
                            responses.append(r['content'])
        except Exception:
            pass
            
        if not responses:
            responses = "No API calls were made during this test (e.g. Model/Serializer unit test)."
            
        if error_msg:
            return {"api_response": responses, "traceback": error_msg}
        return responses

    def addSuccess(self, test):
        super().addSuccess(test)
        self.json_data.append({"test": self.get_test_name(test), "status": "success", "message": self._get_api_message(test)})

    def addFailure(self, test, err):
        super().addFailure(test, err)
        error_msg = self._exc_info_to_string(err, test)
        self.json_data.append({"test": self.get_test_name(test), "status": "failure", "message": self._get_api_message(test, error_msg)})

    def addError(self, test, err):
        super().addError(test, err)
        error_msg = self._exc_info_to_string(err, test)
        self.json_data.append({"test": self.get_test_name(test), "status": "error", "message": self._get_api_message(test, error_msg)})

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.json_data.append({"test": self.get_test_name(test), "status": "skipped", "message": reason})

class JsonTestRunner(unittest.TextTestRunner):
    def _makeResult(self):
        return JsonTestResult(self.stream, self.descriptions, self.verbosity)

    def run(self, test):
        result = super().run(test)
        with open("test_results.json", "w", encoding='utf-8') as f:
            json.dump({
                "testsRun": int(result.testsRun),
                "failures": len(result.failures),
                "errors": len(result.errors),
                "skipped": len(result.skipped),
                "results": getattr(result, 'json_data', [])
            }, f, indent=4, ensure_ascii=False)
        print("\nJSON test results successfully written to test_results.json")
        return result

class JSONDiscoverRunner(DiscoverRunner):
    test_runner = JsonTestRunner
