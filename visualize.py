import dearpygui.dearpygui as dpg
import json
from datetime import datetime, timedelta
import os
import re

# from typing import List, Tuple, Union

# Global variables
data = {}
selected_date = None
selected_station = None
selected_measurements = set()


def load_json_files(directory):
    global data
    data = {}
    date_pattern = re.compile(r"air_quality_(\d{4}-\d{2}-\d{2})_.*\.json")

    for filename in os.listdir(directory):
        match = date_pattern.match(filename)
        if match:
            file_date = datetime.strptime(match.group(1), "%Y-%m-%d").date()
            with open(os.path.join(directory, filename), "r", encoding="utf-8") as f:
                json_data = json.load(f)
                for entry in json_data:
                    station = entry["span_information"][2].strip('"')
                    if file_date not in data:
                        data[file_date] = {}
                    if station not in data[file_date]:
                        data[file_date][station] = {}
                    for measurement in entry["measurements"]:
                        data[file_date][station][measurement["measurement"]] = {
                            "labels": measurement["labels"],
                            "data": measurement["data"],
                        }

    update_date_selector()


def update_date_selector():
    dates = sorted(list(data.keys()))
    dpg.configure_item("date_selector", items=[date.strftime("%Y-%m-%d") for date in dates])


def update_stations():
    if selected_date:
        stations = list(data[selected_date].keys())
        dpg.configure_item("station_selector", items=stations)


def update_measurements():
    if selected_date and selected_station:
        measurements = list(data[selected_date][selected_station].keys())
        dpg.configure_item("measurement_selector", items=measurements)


def get_plot_data(date, station, measurement):
    measurement_data = data[date][station][measurement]
    labels = measurement_data["labels"]
    values = measurement_data["data"]

    x = []
    y = []
    for i, label in enumerate(labels):
        if label != "Nav datu":
            x.append(label)
            y.append(values[i])
    # print(x)
    # print("-------------")
    # print(y)
    return x, y


def plot_data():
    dpg.delete_item("plot", children_only=True)

    if selected_date:
        dpg.set_value("plot_title", f"Starting from {selected_date.strftime('%Y-%m-%d')}")
    else:
        dpg.set_value("plot_title", "No data selected")

    with dpg.plot(label="Measurement Plot", height=400, width=-1, parent="plot"):
        dpg.add_plot_legend()
        x_axis = dpg.add_plot_axis(dpg.mvXAxis, label="Time")
        y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="Value")

        if selected_date and selected_station and selected_measurements:
            for measurement in selected_measurements:
                x, y = get_plot_data(selected_date, selected_station, measurement)
                x_float = [float(time.split(":")[0]) for time in x]
            # combined_x_y = tuple((f"{x_float}", x_float) for x_float in y)
            print(x)
            print(y)
            # print(combined_x_y)
            dpg.add_line_series(x_float, y, label=measurement, parent=y_axis)

            dpg.fit_axis_data(y_axis)

            # Set x-axis ticks
            # dpg.set_axis_ticks(x_axis, combined_x_y)
        else:
            dpg.set_axis_limits(y_axis, 0, 100)


def on_date_selected(sender, app_data, user_data):
    global selected_date
    selected_date = datetime.strptime(app_data, "%Y-%m-%d").date()
    update_stations()


def on_station_selected(sender, app_data, user_data):
    global selected_station
    selected_station = app_data
    update_measurements()


def on_measurement_selected(sender, app_data, user_data):
    global selected_measurements
    if app_data in selected_measurements:
        selected_measurements.remove(app_data)
    else:
        selected_measurements.add(app_data)
    plot_data()


def reset_plot():
    global selected_date, selected_station, selected_measurements
    selected_date = None
    selected_station = None
    selected_measurements = set()
    dpg.set_value("date_selector", "")
    dpg.set_value("station_selector", "")
    dpg.set_value("measurement_selector", "")
    plot_data()


dpg.create_context()

with dpg.window(label="Air Quality Visualization", tag="primary_window"):
    dpg.add_text("Select JSON files directory:")
    dpg.add_input_text(tag="directory_input", default_value=".")
    dpg.add_button(
        label="Load Data", callback=lambda: load_json_files(dpg.get_value("directory_input"))
    )

    with dpg.group(horizontal=True):
        dpg.add_listbox(tag="date_selector", callback=on_date_selected, width=200)
        dpg.add_listbox(tag="station_selector", callback=on_station_selected, width=200)
        dpg.add_listbox(tag="measurement_selector", callback=on_measurement_selected, width=200)

    dpg.add_button(label="Reset Plot", callback=reset_plot)

    dpg.add_text("", tag="plot_title")
    dpg.add_group(tag="plot")

dpg.create_viewport(title="Air Quality Visualization", width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("primary_window", True)
dpg.start_dearpygui()
dpg.destroy_context()
