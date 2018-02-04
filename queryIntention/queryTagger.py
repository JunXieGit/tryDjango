import json
import subprocess
import urllib.parse


class QueryTagger:
    def __init__(self):
        self.command_base = """
            curli --no-log --fabric ei-ltx1 --pretty-print \
            'd2://queryAnnotations/commonContext.queryContext.rawQuery={}&QueryTaggerContext.numTaggings=2&commonContext.memberContext.member=urn:li:member:1288' \
            -X GET -H 'X-RestLi-Protocol-Version:1.0.0'"""

    def tag(self, raw_query='java engineer LinkedIn'):
        raw_query = urllib.parse.quote(raw_query)
        command = self.command_base.format(raw_query)
        c_output, c_error = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).communicate()
        json_out = json.loads(c_output, encoding='utf-8')
        query_tagger = set()
        for clause in json_out['structuredQueryAnnotations']['clauseAnnotations']:
            for queryTaggerInterpretation in clause['queryTaggerInterpretations']:
                for entity in queryTaggerInterpretation['entityAnnotations']:
                    query_tagger.add(entity['queryTaggingResult']['segmentTag'])
        return query_tagger
