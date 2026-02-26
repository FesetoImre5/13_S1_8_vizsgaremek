import xml.etree.ElementTree as ET
import shutil
import os

try:
    tree = ET.parse('output.xml')
    failed_screenshot = None
    for test in tree.iter('test'):
        if test.find('status').attrib['status'] == 'FAIL':
            for msg in test.iter('msg'):
                if msg.text and 'src="selenium-screenshot' in msg.text:
                    # Extract screenshot name from html in msg.text
                    import re
                    match = re.search(r'src="([^"]+)"', msg.text)
                    if match:
                        failed_screenshot = match.group(1)
            break
            
    if failed_screenshot:
        print(f"Failed screenshot: {failed_screenshot}")
        # Copy to artifacts directory
        artifact_path = r"C:\Users\Admill\.gemini\antigravity\brain\457d4d55-a1ef-456b-92bb-646189d96f57\failed_login.png"
        shutil.copy(failed_screenshot, artifact_path)
        print(f"Copied to {artifact_path}")
    else:
        print("No screenshot found.")

except Exception as e:
    import traceback
    traceback.print_exc()
