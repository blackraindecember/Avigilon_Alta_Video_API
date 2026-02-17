import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import pandas as pd
import matplotlib.pyplot as plt
import traceback


def build_datetime_string(date_entry, hour_spin, minute_spin, second_spin):
    """
    Convert UI datetime -> format: YY-MM-DD/HH-MM-SS
    """
    date_str = date_entry.get_date().strftime("%y-%m-%d")
    hour = hour_spin.get().zfill(2)
    minute = minute_spin.get().zfill(2)
    second = second_spin.get().zfill(2)

    return f"{date_str}/{hour}-{minute}-{second}"


def show_chart(df):

    if "time" not in df.columns:
        raise Exception(f"No time column found. Columns: {df.columns}")

    df["time"] = pd.to_datetime(df["time"])

    plt.figure(figsize=(12,6))

    if "in" in df.columns:
        plt.plot(df["time"], df["in"], label="IN")

    if "out" in df.columns:
        plt.plot(df["time"], df["out"], label="OUT")

    plt.legend()
    plt.grid(True)
    plt.title("People Counting")
    plt.tight_layout()
    plt.show()


def build_gui(dashboard):

    root = tk.Tk()
    root.title("Alta Counting Dashboard")
    root.geometry("650x600")

    status_label = ttk.Label(root, text="Status: Connecting...", foreground="orange")
    status_label.pack(pady=5)

    area_combo = ttk.Combobox(root, state="disabled")
    area_combo.pack(pady=5)

    # AUTO CONNECT
    try:
        dashboard.connect()
        dashboard.reload_areas()

        area_combo["values"] = list(dashboard.area_map.keys())
        area_combo.config(state="readonly")

        status_label.config(text="Status: Connected ✓", foreground="green")
        print("[INFO] Connected successfully")

    except Exception:
        status_label.config(text="Status: Failed", foreground="red")
        print("[ERROR] Connection failed")
        traceback.print_exc()

    # RELOAD
    def reload_areas():
        try:
            dashboard.reload_areas()
            area_combo["values"] = list(dashboard.area_map.keys())
            print("[INFO] Counting areas reloaded")
        except Exception:
            print("[ERROR] Reload failed")
            traceback.print_exc()

    ttk.Button(root, text="Reload Areas", command=reload_areas).pack(pady=5)

    # ======================
    # START DATETIME
    # ======================
    ttk.Label(root, text="Start Date & Time").pack(pady=5)

    start_frame = ttk.Frame(root)
    start_frame.pack()

    start_date = DateEntry(start_frame, width=12)
    start_date.grid(row=0, column=0, padx=5)

    start_hour = tk.Spinbox(start_frame, from_=0, to=23, width=3)
    start_hour.grid(row=0, column=1)
    start_hour.delete(0, tk.END)
    start_hour.insert(0, "00")

    start_min = tk.Spinbox(start_frame, from_=0, to=59, width=3)
    start_min.grid(row=0, column=2)
    start_min.delete(0, tk.END)
    start_min.insert(0, "00")

    start_sec = tk.Spinbox(start_frame, from_=0, to=59, width=3)
    start_sec.grid(row=0, column=3)
    start_sec.delete(0, tk.END)
    start_sec.insert(0, "00")

    # ======================
    # END DATETIME
    # ======================
    ttk.Label(root, text="End Date & Time").pack(pady=5)

    end_frame = ttk.Frame(root)
    end_frame.pack()

    end_date = DateEntry(end_frame, width=12)
    end_date.grid(row=0, column=0, padx=5)

    end_hour = tk.Spinbox(end_frame, from_=0, to=23, width=3)
    end_hour.grid(row=0, column=1)
    end_hour.delete(0, tk.END)
    end_hour.insert(0, "23")

    end_min = tk.Spinbox(end_frame, from_=0, to=59, width=3)
    end_min.grid(row=0, column=2)
    end_min.delete(0, tk.END)
    end_min.insert(0, "59")

    end_sec = tk.Spinbox(end_frame, from_=0, to=59, width=3)
    end_sec.grid(row=0, column=3)
    end_sec.delete(0, tk.END)
    end_sec.insert(0, "59")

    # ======================
    # STEP
    # ======================
    ttk.Label(root, text="Step").pack(pady=10)

    step_frame = ttk.Frame(root)
    step_frame.pack()

    ttk.Label(step_frame, text="Hours").grid(row=0, column=0)
    hours_entry = ttk.Entry(step_frame, width=5)
    hours_entry.insert(0, "1")
    hours_entry.grid(row=1, column=0, padx=5)

    ttk.Label(step_frame, text="Minutes").grid(row=0, column=1)
    minutes_entry = ttk.Entry(step_frame, width=5)
    minutes_entry.insert(0, "0")
    minutes_entry.grid(row=1, column=1, padx=5)

    ttk.Label(step_frame, text="Seconds").grid(row=0, column=2)
    seconds_entry = ttk.Entry(step_frame, width=5)
    seconds_entry.insert(0, "0")
    seconds_entry.grid(row=1, column=2, padx=5)

    # ======================
    # LOAD BUTTON
    # ======================
    def load_chart():
        try:
            if not area_combo.get():
                print("[WARNING] No counting area selected")
                return

            h = int(hours_entry.get())
            m = int(minutes_entry.get())
            s = int(seconds_entry.get())

            if h == 0 and m == 0 and s == 0:
                print("[WARNING] Step must be greater than 0")
                return

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

            print("[INFO] Data loaded successfully")
            show_chart(df)

        except Exception:
            print("[ERROR] Load chart failed")
            traceback.print_exc()

    ttk.Button(root, text="Load Chart", command=load_chart).pack(pady=20)

    root.mainloop()
