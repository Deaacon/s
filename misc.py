
import os
import requests


START_STATE = "OPTIMAL"


def open_urls_file(filepath):
    with open(filepath, 'r') as file:
        text_lines = file.read().split('\n')

    return text_lines


def get_page(url):
    response = requests.get(url)
    page_text = response.content.decode()

    return page_text


def parse_page(page_text):
    data = {}

    dimension = 0
    capacity = 0
    nodes_list = []
    demand_list = []

    content = page_text.split('\n')

    idx = 0
    state = START_STATE

    while idx < len(content) and content[idx] != "EOF":
        buffer = content[idx]
        idx += 1
        match state:
            case "OPTIMAL":
                if "COMMENT" in buffer:
                    position = buffer.find("Optimal value:") + 15
                    optimal_value = int(buffer[position:-1])
                    state = "DIMENSION"
            case "DIMENSION":
                if "DIMENSION" in buffer:
                    dimension = int(buffer[12:])
                    state = "CAPACITY"
            case "CAPACITY":
                if "CAPACITY" in buffer:
                    capacity = int(buffer[11:])
                    state = "NODES"
                    idx += 1
            case "NODES":
                if "DEMAND_SECTION" in buffer:
                    state = "DEMAND"
                else:
                    _, x, y = buffer.split()
                    nodes_list.append((int(x), int(y)))
            case "DEMAND":
                if "DEPOT_SECTION" in buffer:
                    state = "EOF"
                else:
                    _, x = buffer.split()
                    demand_list.append(int(x))

    if state != "EOF":
        print(f"Error on {state} state!")
        raise Exception

    data["optimal_value"] = optimal_value
    data["dimension"] = dimension
    data["capacity"] = capacity
    data["nodes"] = nodes_list
    data["demand"] = demand_list

    return data


def open_data():
    data = []

    data_folder = 'data'

    for sub_folder in os.listdir(data_folder):
        sub_path = os.path.join(data_folder, sub_folder)
        for filename in os.listdir(sub_path):
            filepath = os.path.join(sub_path, filename)
            if filename[-4:] != ".vrp":
                continue

            with open(filepath, 'r') as file:
                file_text = file.read()
                try:
                    file_data = parse_page(file_text)
                except:
                    print(f"Parse Error on file:\n{filepath}")
                data.append(file_data)

    return data
