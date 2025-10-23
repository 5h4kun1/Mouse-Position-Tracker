import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import time
from pynput.mouse import Controller
from datetime import datetime

class MouseTrackerMultiPhase:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Phase Mouse Tracker")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        self.root.attributes('-topmost', True)
        
        self.tracking = False
        self.coordinates = []
        self.mouse = Controller()
        self.current_phase = 0
        
        self.setup_gui()
        
    def setup_gui(self):
        # Title
        title_label = tk.Label(self.root, text="🖱️ Multi-Phase Mouse Tracker", 
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
        
        # Row 2: Duration per phase
        row2 = ttk.Frame(settings_frame)
        row2.pack(fill=tk.X, pady=5)
        ttk.Label(row2, text="Duration per Phase (sec):").pack(side=tk.LEFT)
        self.duration_var = tk.StringVar(value="5")
        ttk.Entry(row2, textvariable=self.duration_var, width=8).pack(side=tk.LEFT, padx=5)
        
        # Row 3: Recording Interval
        row3 = ttk.Frame(settings_frame)
        row3.pack(fill=tk.X, pady=5)
        ttk.Label(row3, text="Record Interval (sec):").pack(side=tk.LEFT)
        self.interval_var = tk.StringVar(value="0.5")
        ttk.Entry(row3, textvariable=self.interval_var, width=8).pack(side=tk.LEFT, padx=5)
        
        # Row 4: Number of Phases
        row4 = ttk.Frame(settings_frame)
        row4.pack(fill=tk.X, pady=5)
        ttk.Label(row4, text="Number of Phases:").pack(side=tk.LEFT)
        self.phases_var = tk.StringVar(value="3")
        ttk.Entry(row4, textvariable=self.phases_var, width=8).pack(side=tk.LEFT, padx=5)
        ttk.Label(row4, text="(separate recording sessions)").pack(side=tk.LEFT, padx=5)
        
        # Row 5: Transition Delay
        row5 = ttk.Frame(settings_frame)
        row5.pack(fill=tk.X, pady=5)
        ttk.Label(row5, text="Transition Delay (sec):").pack(side=tk.LEFT)
        self.transition_var = tk.StringVar(value="3")
        ttk.Entry(row5, textvariable=self.transition_var, width=8).pack(side=tk.LEFT, padx=5)
        ttk.Label(row5, text="(time to move between phases)").pack(side=tk.LEFT, padx=5)
        
        # Always on top checkbox
        self.ontop_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, text="Always on Top", 
                       variable=self.ontop_var, 
                       command=self.toggle_topmost).pack(pady=5)
        
        # Phase indicator
        self.phase_label = tk.Label(self.root, text="Phase: 0/0", 
                                    font=('Arial', 14, 'bold'), fg='purple')
        self.phase_label.pack(pady=5)
        
        # Current position display
        self.position_label = tk.Label(self.root, text="Current Position: X=0, Y=0", 
                                       font=('Arial', 12), fg='blue')
        self.position_label.pack(pady=5)
        
        # Status label with larger font for visibility
        self.status_label = tk.Label(self.root, text="Ready to track", 
                                     font=('Arial', 14, 'bold'), fg='green',
                                     bg='lightyellow', padx=10, pady=5)
        self.status_label.pack(pady=10, fill=tk.X, padx=20)
        
        # Timer label
        self.timer_label = tk.Label(self.root, text="Time Remaining: 0.0s", 
                                    font=('Arial', 11))
        self.timer_label.pack(pady=5)
        
        # Buttons Frame
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        self.start_btn = ttk.Button(btn_frame, text="▶ Start Multi-Phase Tracking", 
                                   command=self.start_tracking, width=22)
        self.start_btn.grid(row=0, column=0, padx=5)
        
        self.save_btn = ttk.Button(btn_frame, text="💾 Save Log", 
                                  command=self.save_log, width=18)
        self.save_btn.grid(row=0, column=1, padx=5)
        
        self.clear_btn = ttk.Button(btn_frame, text="🗑️ Clear Log", 
                                   command=self.clear_log, width=18)
        self.clear_btn.grid(row=1, column=0, padx=5, pady=5)
        
        self.auto_save_var = tk.BooleanVar(value=True)
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
        
        self.coords_text = tk.Text(text_frame, height=15, width=70, 
                                   yscrollcommand=scrollbar.set, 
                                   font=('Courier', 9))
        self.coords_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.coords_text.yview)
        
        # Statistics
        self.stats_label = tk.Label(self.root, text="Total Points: 0 | Phases: 0", 
                                    font=('Arial', 10))
        self.stats_label.pack(pady=5)
        
    def toggle_topmost(self):
        self.root.attributes('-topmost', self.ontop_var.get())
        
    def start_tracking(self):
        try:
            delay = float(self.delay_var.get())
            duration = float(self.duration_var.get())
            interval = float(self.interval_var.get())
            phases = int(self.phases_var.get())
            transition = float(self.transition_var.get())
            
            if delay < 0 or duration <= 0 or interval <= 0 or phases <= 0 or transition < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid positive numbers!")
            return
            
        # Disable buttons during tracking
        self.start_btn.config(state='disabled')
        self.save_btn.config(state='disabled')
        self.clear_btn.config(state='disabled')
        
        # Clear previous data
        self.coordinates = []
        self.current_phase = 0
        
        # Start tracking in separate thread
        track_thread = threading.Thread(target=self.track_multi_phase, 
                                       args=(delay, duration, interval, phases, transition))
        track_thread.daemon = True
        track_thread.start()
        
    def track_multi_phase(self, delay, duration, interval, phases, transition):
        # Initial countdown
        for i in range(int(delay), 0, -1):
            self.root.after(0, lambda t=i: self.status_label.config(
                text=f"🕐 GET READY - Starting in {t} seconds...", 
                fg='orange', bg='lightyellow'))
            self.root.after(0, lambda t=i: self.phase_label.config(
                text=f"Phase: 0/{phases}"))
            time.sleep(1)
        
        # Loop through each phase
        for phase in range(1, phases + 1):
            self.current_phase = phase
            
            # Update phase indicator
            self.root.after(0, lambda p=phase: self.phase_label.config(
                text=f"Phase: {p}/{phases}", fg='purple'))
            
            # Record for this phase
            self.track_single_phase(duration, interval, phase)
            
            # Check if there's another phase
            if phase < phases:
                # Show transition message
                self.root.after(0, lambda p=phase: self.show_transition_message(p, phases))
                
                # Countdown for transition
                for i in range(int(transition), 0, -1):
                    self.root.after(0, lambda t=i, p=phase: self.status_label.config(
                        text=f"⏳ NOW MOVE TO DIFFERENT POSITION! Next phase in {t}s", 
                        fg='white', bg='orange'))
                    self.root.after(0, lambda t=i: self.timer_label.config(
                        text=f"Transition Time: {t}s"))
                    time.sleep(1)
        
        # All phases complete
        self.root.after(0, self.display_results)
        
    def track_single_phase(self, duration, interval, phase):
        self.tracking = True
        start_time = time.time()
        phase_coords = []
        
        self.root.after(0, lambda: self.status_label.config(
            text=f"🔴 RECORDING PHASE {phase}... Move your mouse!", 
            fg='white', bg='red'))
        
        while self.tracking and (time.time() - start_time) < duration:
            elapsed = time.time() - start_time
            remaining = duration - elapsed
            
            # Get current mouse position
            pos = self.mouse.position
            x, y = pos
            
            # Record position with timestamp and phase
            self.coordinates.append((x, y, elapsed, phase))
            phase_coords.append((x, y, elapsed))
            
            # Update UI
            self.root.after(0, lambda x=x, y=y: self.update_position(x, y))
            self.root.after(0, lambda r=remaining: self.timer_label.config(
                text=f"Time Remaining: {r:.1f}s"))
            
            time.sleep(interval)
        
        self.tracking = False
        
    def show_transition_message(self, completed_phase, total_phases):
        # Create a prominent popup-style message
        self.status_label.config(
            text=f"✅ Phase {completed_phase} Complete! NOW MOVE TO A DIFFERENT POSITION!", 
            fg='white', bg='green')
        
    def update_position(self, x, y):
        self.position_label.config(text=f"Current Position: X={x}, Y={y}")
        
    def display_results(self):
        self.status_label.config(
            text="✅ ALL PHASES COMPLETE!", 
            fg='white', bg='green')
        self.timer_label.config(text="All phases finished!")
        
        # Clear text widget
        self.coords_text.delete(1.0, tk.END)
        
        # Add header with timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.coords_text.insert(tk.END, f"Multi-Phase Recording Session: {current_time}\n")
        self.coords_text.insert(tk.END, f"Duration per Phase: {self.duration_var.get()}s | ")
        self.coords_text.insert(tk.END, f"Interval: {self.interval_var.get()}s | ")
        self.coords_text.insert(tk.END, f"Total Phases: {self.current_phase}\n")
        self.coords_text.insert(tk.END, "=" * 75 + "\n\n")
        
        # Group coordinates by phase
        phases = {}
        for x, y, t, phase in self.coordinates:
            if phase not in phases:
                phases[phase] = []
            phases[phase].append((x, y, t))
        
        # Display coordinates grouped by phase
        for phase_num in sorted(phases.keys()):
            self.coords_text.insert(tk.END, f"\n{'='*75}\n")
            self.coords_text.insert(tk.END, f"PHASE {phase_num} - {len(phases[phase_num])} points\n")
            self.coords_text.insert(tk.END, f"{'='*75}\n")
            self.coords_text.insert(tk.END, f"{'#':<6} {'X':<10} {'Y':<10} {'Time (s)':<12}\n")
            self.coords_text.insert(tk.END, "-" * 75 + "\n")
            
            for idx, (x, y, t) in enumerate(phases[phase_num], 1):
                line = f"{idx:<6} {x:<10} {y:<10} {t:<12.3f}\n"
                self.coords_text.insert(tk.END, line)
            
            # Phase statistics
            avg_x = sum(coord[0] for coord in phases[phase_num]) / len(phases[phase_num])
            avg_y = sum(coord[1] for coord in phases[phase_num]) / len(phases[phase_num])
            self.coords_text.insert(tk.END, f"\nPhase {phase_num} Average: X={avg_x:.2f}, Y={avg_y:.2f}\n")
        
        # Overall statistics
        total = len(self.coordinates)
        self.stats_label.config(text=f"Total Points: {total} | Phases: {self.current_phase}")
        
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
        
        filename = filedialog.asksaveasfilename(
            title="Save Multi-Phase Mouse Tracking Log",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), 
                      ("CSV files", "*.csv"),
                      ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w') as file:
                    content = self.coords_text.get(1.0, tk.END)
                    file.write(content)
                
                messagebox.showinfo("Saved", f"Log saved successfully to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")
    
    def save_log_auto(self):
        if not self.coordinates:
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"mouse_multiphase_log_{timestamp}.txt"
        
        try:
            with open(filename, 'w') as file:
                content = self.coords_text.get(1.0, tk.END)
                file.write(content)
            
            self.status_label.config(
                text=f"✅ Auto-saved: {filename}", 
                fg='white', bg='green')
        except Exception as e:
            self.status_label.config(text=f"❌ Auto-save failed!", 
                                    fg='white', bg='red')
        
    def clear_log(self):
        self.coords_text.delete(1.0, tk.END)
        self.coordinates = []
        self.current_phase = 0
        self.stats_label.config(text="Total Points: 0 | Phases: 0")
        self.position_label.config(text="Current Position: X=0, Y=0")
        self.phase_label.config(text="Phase: 0/0")
        self.status_label.config(text="Ready to track", fg='green', bg='lightyellow')
        self.timer_label.config(text="Time Remaining: 0.0s")

if __name__ == "__main__":
    root = tk.Tk()
    app = MouseTrackerMultiPhase(root)
    root.mainloop()
