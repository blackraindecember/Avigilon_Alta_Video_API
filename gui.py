import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import pandas as pd
import matplotlib.pyplot as plt
import traceback


# =====================================================
# BUILD DATETIME STRING
# =====================================================
def build_datetime_string(date_entry, hour_spin, minute_spin, second_spin):
    date_str = date_entry.get_date().strftime("%y-%m-%d")
    hour = hour_spin.get().zfill(2)
    minute = minute_spin.get().zfill(2)
    second = second_spin.get().zfill(2)
    return f"{date_str}/{hour}-{minute}-{second}"


# =====================================================
# SMART CHART
# =====================================================
def show_chart(df):

    print("[DEBUG] Chart columns:", df.columns.tolist())

    if "time" not in df.columns:
        print("[ERROR] No time column")
        return

    df["time"] = pd.to_datetime(df["time"])

    plt.figure(figsize=(12, 6))
    plotted = False

    # ---- People Crossing ----
    if "in" in df.columns or "out" in df.columns:

        if "in" in df.columns:
            plt.plot(df["time"], df["in"], label="People IN")
            plotted = True

        if "out" in df.columns:
            plt.plot(df["time"], df["out"], label="People OUT")
            plotted = True

        plt.title("People Crossing")

    # ---- People Occupancy ----
    elif "occupancy_max" in df.columns or "occupancy_min" in df.columns:

        if "occupancy_max" in df.columns:
            plt.plot(df["time"], df["occupancy_max"], label="Max Occupancy")
            plotted = True

        if "occupancy_min" in df.columns:
            plt.plot(df["time"], df["occupancy_min"], label="Min Occupancy")
            plotted = True

        plt.title("People Occupancy")

    # ---- Vehicle Crossing ----
    elif "vehicle_in" in df.columns or "vehicle_out" in df.columns:

        if "vehicle_in" in df.columns:
            plt.plot(df["time"], df["vehicle_in"], label="Vehicle IN")
            plotted = True

        if "vehicle_out" in df.columns:
            plt.plot(df["time"], df["vehicle_out"], label="Vehicle OUT")
            plotted = True

        plt.title("Vehicle Crossing")

    if not plotted:
        print("[WARNING] No valid counting columns found")
        return

    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# =====================================================
# SHOW TABLE
# =====================================================
def show_table(df):

    table_window = tk.Toplevel()
    table_window.title("Counting Data Table")
    table_window.geometry("1100x500")

    tree = ttk.Treeview(table_window)
    tree["columns"] = list(df.columns)
    tree["show"] = "headings"

    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=140)

    for _, row in df.iterrows():
        tree.insert("", tk.END, values=list(row))

    tree.pack(expand=True, fill="both")

    scrollbar = ttk.Scrollbar(table_window, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")


# =====================================================
# BUILD GUI
# =====================================================
def build_gui(dashboard):

    root = tk.Tk()
    root.title("Alta Counting Dashboard")
    root.geometry("750x650")

    current_df = {"data": None}

    # -------------------------------------------------
    # STATUS
    # -------------------------------------------------
    status_label = ttk.Label(root, text="Status: Disconnected", foreground="red")
    status_label.pack(pady=5)

    # -------------------------------------------------
    # CONNECT BUTTON
    # -------------------------------------------------
    def connect():
        try:
            dashboard.connect()
            dashboard.reload_areas()

            area_combo["values"] = list(dashboard.area_map.keys())
            area_combo.config(state="readonly")

            status_label.config(text="Status: Connected ✓", foreground="green")
        except Exception:
            status_label.config(text="Status: Failed", foreground="red")
            traceback.print_exc()

    ttk.Button(root, text="Connect / Reconnect", command=connect).pack(pady=5)

    # -------------------------------------------------
    # AREA DROPDOWN
    # -------------------------------------------------
    area_combo = ttk.Combobox(root, state="disabled", width=40)
    area_combo.pack(pady=5)

    # -------------------------------------------------
    # RELOAD AREAS
    # -------------------------------------------------
    def reload_areas():
        try:
            dashboard.reload_areas()
            area_combo["values"] = list(dashboard.area_map.keys())
        except Exception:
            traceback.print_exc()

    ttk.Button(root, text="Reload Areas", command=reload_areas).pack(pady=5)

    # =====================================================
    # START DATE TIME
    # =====================================================
    ttk.Label(root, text="Start Date & Time").pack(pady=5)

    start_frame = ttk.Frame(root)
    start_frame.pack(pady=5)

    start_date = DateEntry(start_frame, width=12)
    start_date.grid(row=0, column=0, padx=5)

    start_hour = tk.Spinbox(start_frame, from_=0, to=23, width=3)
    start_hour.grid(row=0, column=1)

    ttk.Label(start_frame, text=":").grid(row=0, column=2)

    start_min = tk.Spinbox(start_frame, from_=0, to=59, width=3)
    start_min.grid(row=0, column=3)

    ttk.Label(start_frame, text=":").grid(row=0, column=4)

    start_sec = tk.Spinbox(start_frame, from_=0, to=59, width=3)
    start_sec.grid(row=0, column=5)

    # =====================================================
    # END DATE TIME
    # =====================================================
    ttk.Label(root, text="End Date & Time").pack(pady=5)

    end_frame = ttk.Frame(root)
    end_frame.pack(pady=5)

    end_date = DateEntry(end_frame, width=12)
    end_date.grid(row=0, column=0, padx=5)

    end_hour = tk.Spinbox(end_frame, from_=0, to=23, width=3)
    end_hour.grid(row=0, column=1)

    ttk.Label(end_frame, text=":").grid(row=0, column=2)

    end_min = tk.Spinbox(end_frame, from_=0, to=59, width=3)
    end_min.grid(row=0, column=3)

    ttk.Label(end_frame, text=":").grid(row=0, column=4)

    end_sec = tk.Spinbox(end_frame, from_=0, to=59, width=3)
    end_sec.grid(row=0, column=5)

    # =====================================================
    # STEP INPUT
    # =====================================================
    ttk.Label(root, text="Step Interval").pack(pady=10)

    step_frame = ttk.Frame(root)
    step_frame.pack(pady=5)

    ttk.Label(step_frame, text="Hours").grid(row=0, column=0)
    hours_entry = ttk.Entry(step_frame, width=5)
    hours_entry.insert(0, "1")
    hours_entry.grid(row=1, column=0, padx=15)

    ttk.Label(step_frame, text="Minutes").grid(row=0, column=1)
    minutes_entry = ttk.Entry(step_frame, width=5)
    minutes_entry.insert(0, "0")
    minutes_entry.grid(row=1, column=1, padx=15)

    ttk.Label(step_frame, text="Seconds").grid(row=0, column=2)
    seconds_entry = ttk.Entry(step_frame, width=5)
    seconds_entry.insert(0, "0")
    seconds_entry.grid(row=1, column=2, padx=15)

    # =====================================================
    # LOAD CHART
    # =====================================================
    def load_chart():

        if not area_combo.get():
            print("[WARNING] Select area first")
            return

        h = int(hours_entry.get())
        m = int(minutes_entry.get())
        s = int(seconds_entry.get())

        start_str = build_datetime_string(start_date, start_hour, start_min, start_sec)
        end_str = build_datetime_string(end_date, end_hour, end_min, end_sec)

        area_id = dashboard.area_map[area_combo.get()]

        df = dashboard.get_dataframe(
            area_id,
            start_str,
            end_str,
            hours=h,
            minutes=m,
            seconds=s
        )

        current_df["data"] = df
        show_chart(df)

    ttk.Button(root, text="Load Chart", command=load_chart).pack(pady=15)

    # =====================================================
    # SHOW TABLE
    # =====================================================
    def load_table():
        if current_df["data"] is None:
            print("[WARNING] Load data first")
            return
        show_table(current_df["data"])

    ttk.Button(root, text="Show Table", command=load_table).pack(pady=5)

    root.mainloop()
