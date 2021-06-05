import json
import xmltodict


def xmltojson(xml_text: str):
    json_str = json.dumps(xmltodict.parse(xml_text))
    data = json.loads(json_str)
    return data
