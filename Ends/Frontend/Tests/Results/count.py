import xml.etree.ElementTree as ET
try:
    tree = ET.parse('output.xml')
    passed, failed = 0, 0
    for test in tree.iter('test'):
        status = test.find('status')
        if status is not None:
            if status.attrib['status'] == 'PASS': passed += 1
            if status.attrib['status'] == 'FAIL': failed += 1
    print(f"Total PASS: {passed}")
    print(f"Total FAIL: {failed}")
except Exception as e:
    print(e)
