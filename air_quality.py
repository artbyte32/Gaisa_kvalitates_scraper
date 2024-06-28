import requests
from bs4 import BeautifulSoup
import re
import json
from datetime import datetime
import os
import sys

url = "http://gmsd.riga.lv/main.php"


def extract_script_data(script):
    data_match = re.search(r"data:\s*(\[.+?\])", script.string, re.DOTALL)
    label_match = re.search(r'label:\s*[\'"](.+?)[\'"]', script.string)
    labels_match = re.search(r"labels:\s*(\[.+?\])", script.string, re.DOTALL)

    data = eval(data_match.group(1)) if data_match else []
    label = label_match.group(1) if label_match else "Unknown"

    if labels_match:
        labels_str = labels_match.group(1)
        labels = [label.strip(" '\"") for label in labels_str.strip("[]").split(",")]
    else:
        labels = []

    return label, data, labels


try:
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    tabs = soup.find_all("div", class_="c-tab__content")

    output_data = []

    for tab in tabs:
        tab_data = {"span_information": [], "measurements": []}

        spans = tab.find_all("span", class_="c_span_tval")
        if spans:
            tab_data["span_information"] = [span.text.strip() for span in spans]

        scripts = tab.find_all("script")
        for script in scripts:
            if script.string and "datasets" in script.string:
                label, data, labels = extract_script_data(script)
                if data:
                    tab_data["measurements"].append(
                        {"measurement": label, "labels": labels, "data": data}
                    )

        output_data.append(tab_data)

    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(script_dir, f"air_quality_{current_time}.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"Data successfully saved to {filename}")
except Exception as e:
    error_message = f"Error occurred: {str(e)}"
    print(error_message, file=sys.stderr)
    sys.exit(1)
