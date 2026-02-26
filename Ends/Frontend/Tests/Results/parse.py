import xml.etree.ElementTree as ET
try:
    tree = ET.parse('output.xml')
    fails = []
    for test in tree.iter('test'):
        status = test.find('status')
        if status is not None and status.attrib['status'] == 'FAIL':
            fails.append(f"{test.attrib['name']}: {status.text}")
    print("FAILS:\n" + "\n".join(fails))
except Exception as e:
    print(e)
