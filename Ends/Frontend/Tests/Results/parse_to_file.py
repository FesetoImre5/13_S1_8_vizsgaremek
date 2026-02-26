import xml.etree.ElementTree as ET
try:
    tree = ET.parse('output.xml')
    with open('fails.txt', 'w', encoding='utf-8') as f:
        fails = []
        for test in tree.iter('test'):
            status = test.find('status')
            if status is not None and status.attrib['status'] == 'FAIL':
                msgs = [m.text for m in test.iter('msg')]
                f.write(f"FAIL: {test.attrib['name']} - {status.text}\n")
except Exception as e:
    print(e)
