import json
import sys
import xml.etree.ElementTree as ET

def convert_trufflehog_to_junit(json_file, xml_file):
    with open(json_file) as f:
        data = json.load(f)

    testsuites = ET.Element('testsuites')
    testsuite = ET.SubElement(testsuites, 'testsuite', name='Trufflehog Scan', tests=str(len(data)), failures=str(len(data)))

    for item in data:
        testcase = ET.SubElement(testsuite, 'testcase', classname=item['path'], name=item['rule'])
        failure = ET.SubElement(testcase, 'failure', message=item['rule'])
        failure.text = item['message']

    tree = ET.ElementTree(testsuites)
    tree.write(xml_file, encoding='utf-8', xml_declaration=True)

if __name__ == '__main__':
    convert_trufflehog_to_junit('/results/trufflehog-secret-scan-report.json', '/results/trufflehog-secret-scan-report.xml')
