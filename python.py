import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import time
from pynput.mouse import Controller
from datetime import datetime

class MouseTrackerPro:
    def __init__(self, root):
        self.root = root
        self.root.title("Mouse Position Tracker Pro")
        self.root.geometry("550x650")
        self.root.resizable(False, False)
        
        # Always on top by default
        self.root.attributes('-topmost', True)
        
        # Tracking state
        self.tracking = False
        self.coordinates = []
        self.mouse = Controller()
        self.timer = None
        
        # Setup GUI
        self.setup_gui()
        
    def setup_gui(self):
        # Title
        title_label = tk.Label(self.root, text="🖱️ Mouse Position Tracker Pro", 
                              font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Settings Frame
        settings_frame = ttk.LabelFrame(self.root, text="Settings", padding="10")
        settings_frame.pack(padx=10, pady=5, fill=tk.X)
        
        # Row 1: Start Delay
        row1 = ttk.Frame(settings_frame)
        row1.pack(fill=tk.X, pady=5)
        ttk.Label(row1, text="Start Delay (sec):").pack(side=tk.LEFT)
        self.delay_var = tk.StringVar(value="3")
        ttk.Entry(row1, textvariable=self.delay_var, width=8).pack(side=tk.LEFT, padx=5)
        
        # Row 2: Duration
        row2 = ttk.Frame(settings_frame)
        row2.pack(fill=tk.X, pady=5)
        ttk.Label(row2, text="Duration (sec):").pack(side=tk.LEFT)
        self.duration_var = tk.StringVar(value="5")
        ttk.Entry(row2, textvariable=self.duration_var, width=8).pack(side=tk.LEFT, padx=5)
        
        # Row 3: Recording Interval
        row3 = ttk.Frame(settings_frame)
        row3.pack(fill=tk.X, pady=5)
        ttk.Label(row3, text="Record Interval (sec):").pack(side=tk.LEFT)
        self.interval_var = tk.StringVar(value="0.5")
        ttk.Entry(row3, textvariable=self.interval_var, width=8).pack(side=tk.LEFT, padx=5)
        ttk.Label(row3, text="(how often to record position)").pack(side=tk.LEFT, padx=5)
        
        # Always on top checkbox
        self.ontop_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, text="Always on Top", 
                       variable=self.ontop_var, 
                       command=self.toggle_topmost).pack(pady=5)
        
        # Current position display
        self.position_label = tk.Label(self.root, text="Current Position: X=0, Y=0", 
                                       font=('Arial', 14), fg='blue')
        self.position_label.pack(pady=10)
        
        # Status label
        self.status_label = tk.Label(self.root, text="Ready to track", 
                                     font=('Arial', 12, 'bold'), fg='green')
        self.status_label.pack(pady=5)
        
        # Timer label
        self.timer_label = tk.Label(self.root, text="Time Remaining: 0.0s", 
                                    font=('Arial', 11))
        self.timer_label.pack(pady=5)
        
        # Buttons Frame
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        self.start_btn = ttk.Button(btn_frame, text="▶ Start Tracking", 
                                   command=self.start_tracking, width=18)
        self.start_btn.grid(row=0, column=0, padx=5)
        
        self.save_btn = ttk.Button(btn_frame, text="💾 Save Log", 
                                  command=self.save_log, width=18)
        self.save_btn.grid(row=0, column=1, padx=5)
        
        self.clear_btn = ttk.Button(btn_frame, text="🗑️ Clear Log", 
                                   command=self.clear_log, width=18)
        self.clear_btn.grid(row=1, column=0, padx=5, pady=5)
        
        self.auto_save_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(btn_frame, text="Auto-save after tracking", 
                       variable=self.auto_save_var).grid(row=1, column=1, padx=5)
        
        # Coordinates display
        coords_label = tk.Label(self.root, text="📋 Tracked Coordinates Log:", 
                               font=('Arial', 12, 'bold'))
        coords_label.pack(pady=5)
        
        # Scrollable text widget
        text_frame = ttk.Frame(self.root)
        text_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.coords_text = tk.Text(text_frame, height=12, width=65, 
                                   yscrollcommand=scrollbar.set, 
                                   font=('Courier', 9))
        self.coords_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.coords_text.yview)
        
        # Statistics
        self.stats_label = tk.Label(self.root, text="Total Points: 0 | Interval: 0.0s", 
                                    font=('Arial', 10))
        self.stats_label.pack(pady=5)
        
    def toggle_topmost(self):
        self.root.attributes('-topmost', self.ontop_var.get())
        
    def start_tracking(self):
        try:
            delay = float(self.delay_var.get())
            duration = float(self.duration_var.get())
            interval = float(self.interval_var.get())
            
            if delay < 0 or duration <= 0 or interval <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid positive numbers!")
            return
            
        # Disable buttons during tracking
        self.start_btn.config(state='disabled')
        self.save_btn.config(state='disabled')
        self.clear_btn.config(state='disabled')
        
        # Start tracking in separate thread
        track_thread = threading.Thread(target=self.track_mouse, 
                                       args=(delay, duration, interval))
        track_thread.daemon = True
        track_thread.start()
        
    def track_mouse(self, delay, duration, interval):
        # Countdown phase
        for i in range(int(delay), 0, -1):
            self.root.after(0, lambda t=i: self.status_label.config(
                text=f"Starting in {t} seconds...", fg='orange'))
            self.root.after(0, lambda: self.timer_label.config(
                text=f"Countdown: {i}s"))
            time.sleep(1)
        
        # Start tracking
        self.tracking = True
        self.coordinates = []
        start_time = time.time()
        recording_count = 0
        
        self.root.after(0, lambda: self.status_label.config(
            text="🔴 RECORDING... Move your mouse!", fg='red'))
        
        # Record at intervals
        while self.tracking and (time.time() - start_time) < duration:
            elapsed = time.time() - start_time
            remaining = duration - elapsed
            
            # Get current mouse position
            pos = self.mouse.position
            x, y = pos
            
            # Record position with timestamp
            self.coordinates.append((x, y, elapsed))
            recording_count += 1
            
            # Update UI
            self.root.after(0, lambda x=x, y=y: self.update_position(x, y))
            self.root.after(0, lambda r=remaining: self.timer_label.config(
                text=f"Time Remaining: {r:.1f}s"))
            
            # Wait for interval before next recording
            time.sleep(interval)
        
        # Stop tracking
        self.tracking = False
        
        # Display results
        self.root.after(0, self.display_results)
        
    def update_position(self, x, y):
        self.position_label.config(text=f"Current Position: X={x}, Y={y}")
        
    def display_results(self):
        self.status_label.config(text="✅ Tracking Complete!", fg='green')
        self.timer_label.config(text="Time Remaining: 0.0s")
        
        # Clear text widget
        self.coords_text.delete(1.0, tk.END)
        
        # Add header with timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.coords_text.insert(tk.END, f"Recording Session: {current_time}\n")
        self.coords_text.insert(tk.END, f"Duration: {self.duration_var.get()}s | ")
        self.coords_text.insert(tk.END, f"Interval: {self.interval_var.get()}s\n")
        self.coords_text.insert(tk.END, "=" * 70 + "\n\n")
        
        # Display all coordinates
        self.coords_text.insert(tk.END, f"{'#':<6} {'X':<10} {'Y':<10} {'Time (s)':<12} {'Timestamp':<15}\n")
        self.coords_text.insert(tk.END, "-" * 70 + "\n")
        
        for idx, (x, y, t) in enumerate(self.coordinates, 1):
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            line = f"{idx:<6} {x:<10} {y:<10} {t:<12.3f} {timestamp:<15}\n"
            self.coords_text.insert(tk.END, line)
        
        # Update statistics
        total = len(self.coordinates)
        interval = float(self.interval_var.get())
        self.stats_label.config(text=f"Total Points: {total} | Interval: {interval}s")
        
        # Add summary
        if total > 0:
            avg_x = sum(coord[0] for coord in self.coordinates) / total
            avg_y = sum(coord[1] for coord in self.coordinates) / total
            max_x = max(coord[0] for coord in self.coordinates)
            max_y = max(coord[1] for coord in self.coordinates)
            min_x = min(coord[0] for coord in self.coordinates)
            min_y = min(coord[1] for coord in self.coordinates)
            
            self.coords_text.insert(tk.END, "\n" + "=" * 70 + "\n")
            self.coords_text.insert(tk.END, "STATISTICS:\n")
            self.coords_text.insert(tk.END, f"  Average Position: X={avg_x:.2f}, Y={avg_y:.2f}\n")
            self.coords_text.insert(tk.END, f"  Range X: {min_x} to {max_x}\n")
            self.coords_text.insert(tk.END, f"  Range Y: {min_y} to {max_y}\n")
        
        # Re-enable buttons
        self.start_btn.config(state='normal')
        self.save_btn.config(state='normal')
        self.clear_btn.config(state='normal')
        
        # Auto-save if enabled
        if self.auto_save_var.get():
            self.root.after(500, self.save_log_auto)
        
    def save_log(self):
        if not self.coordinates:
            messagebox.showwarning("No Data", "No coordinates to save!")
            return
        
        # Ask for file location
        filename = filedialog.asksaveasfilename(
            title="Save Mouse Tracking Log",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), 
                      ("CSV files", "*.csv"),
                      ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w') as file:
                    # Write content from text widget
                    content = self.coords_text.get(1.0, tk.END)
                    file.write(content)
                
                messagebox.showinfo("Saved", f"Log saved successfully to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")
    
    def save_log_auto(self):
        if not self.coordinates:
            return
        
        # Auto-save with timestamp filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"mouse_log_{timestamp}.txt"
        
        try:
            with open(filename, 'w') as file:
                content = self.coords_text.get(1.0, tk.END)
                file.write(content)
            
            self.status_label.config(text=f"✅ Auto-saved: {filename}", fg='green')
        except Exception as e:
            self.status_label.config(text=f"❌ Auto-save failed!", fg='red')
        
    def clear_log(self):
        self.coords_text.delete(1.0, tk.END)
        self.coordinates = []
        self.stats_label.config(text="Total Points: 0 | Interval: 0.0s")
        self.position_label.config(text="Current Position: X=0, Y=0")
        self.status_label.config(text="Ready to track", fg='green')
        self.timer_label.config(text="Time Remaining: 0.0s")

if __name__ == "__main__":
    root = tk.Tk()
    app = MouseTrackerPro(root)
    root.mainloop()
