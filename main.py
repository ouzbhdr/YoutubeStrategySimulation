import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Global UI Settings
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ViralSimulatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Configuration
        self.title("Viral-Optimus Pro v1.1")
        self.geometry("1150x650")

        # Main Layout Configuration
        self.grid_columnconfigure(0, weight=1) # Sidebar (Inputs)
        self.grid_columnconfigure(1, weight=3) # Main Dashboard (Graphics)
        self.grid_rowconfigure(0, weight=1)

        # --- LEFT SIDEBAR: CONTROLS ---
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="VIRAL OPTIMUS", font=ctk.CTkFont(size=22, weight="bold"))
        self.logo_label.pack(pady=(20, 5))
        
        self.tagline = ctk.CTkLabel(self.sidebar, text="Strategy & Growth Modeling", font=ctk.CTkFont(size=12))
        self.tagline.pack(pady=(0, 20))

        # --- PARAMETER: TOTAL TIME ---
        self.time_label = ctk.CTkLabel(self.sidebar, text="Total Simulation Time (Days): 365", anchor="w")
        self.time_label.pack(fill="x", padx=20)
        self.time_slider = ctk.CTkSlider(self.sidebar, from_=30, to=1000, command=self.update_ui)
        self.time_slider.set(365)
        self.time_slider.pack(pady=(5, 20), padx=20)

        # --- PARAMETER: COMPLEXITY FACTOR ---
        self.comp_label = ctk.CTkLabel(self.sidebar, text="Complexity Factor: 0.05", anchor="w")
        self.comp_label.pack(fill="x", padx=20)
        self.comp_slider = ctk.CTkSlider(self.sidebar, from_=0.01, to=0.1, command=self.update_ui)
        self.comp_slider.set(0.05)
        self.comp_slider.pack(pady=(5, 5), padx=20)
        
        # Educational info about Complexity Factor
        self.info_box = ctk.CTkTextbox(self.sidebar, height=100, font=("Arial", 11))
        self.info_box.pack(pady=10, padx=20)
        self.info_box.insert("0.0", "INFO: Complexity Factor defines how 'expensive' quality is. High values mean top-tier quality takes significantly more time to produce (Law of Diminishing Returns).")
        self.info_box.configure(state="disabled")

        # --- RIGHT SIDE: DASHBOARD ---
        self.dashboard_frame = ctk.CTkFrame(self)
        self.dashboard_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        # Success Metrics Display
        self.stats_label = ctk.CTkLabel(self.dashboard_frame, text="Ready to Simulate...", font=("Arial", 18, "bold"), text_color="#2ecc71")
        self.stats_label.pack(pady=15)

        # Matplotlib Figure Integration
        self.fig, self.ax1 = plt.subplots(figsize=(8, 5), dpi=100)
        self.fig.patch.set_facecolor('#2b2b2b') 
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.dashboard_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=20)

        # Initial Run
        self.update_ui()

    def update_ui(self, *args):
        """
        Main simulation logic and UI update trigger.
        Called whenever a slider is moved.
        """
        # 1. Fetch values from UI
        days = self.time_slider.get()
        comp = self.comp_slider.get()
        
        # Update text labels
        self.time_label.configure(text=f"Total Simulation Time (Days): {int(days)}")
        self.comp_label.configure(text=f"Complexity Factor: {comp:.2f}")

        # 2. Mathematical Modeling
        quality_levels = np.arange(1, 101)
        
        # Production Time: Exponential cost of quality
        # Formula: time = base + exp(complexity * quality) * coefficient
        time_per_video = 0.1 + np.exp(comp * quality_levels) * 0.05
        
        # Viral Chance: Sigmoid curve representing audience behavior
        viral_prob = 0.25 / (1 + np.exp(-0.15 * (quality_levels - 60)))
        
        # Output Metrics
        videos_produced = days / time_per_video
        expected_hits = videos_produced * viral_prob

        # Find Optimal Point (Maximum Success)
        opt_idx = np.argmax(expected_hits)
        opt_quality = quality_levels[opt_idx]
        max_hits = expected_hits[opt_idx]
        
        # 3. Update Graphics
        self.ax1.clear()
        self.ax1.set_facecolor('#1e1e1e')
        
        # Plot Success Curve
        self.ax1.plot(quality_levels, expected_hits, color='#3498db', linewidth=4, label='Expected Viral Success')
        self.ax1.fill_between(quality_levels, expected_hits, color='#3498db', alpha=0.2)
        
        # Visual Indicators
        self.ax1.axvline(x=opt_quality, color='#e74c3c', linestyle='--', alpha=0.8)
        self.ax1.set_title("Success Efficiency vs. Content Quality", color='white', fontsize=14, pad=20)
        self.ax1.set_xlabel("Quality Level (1-100)", color='gray')
        self.ax1.set_ylabel("Expected Viral Hits", color='gray')
        self.ax1.tick_params(colors='white')
        self.ax1.grid(True, linestyle=':', alpha=0.3)
        
        # Update Top Stats Label
        self.stats_label.configure(
            text=f"OPTIMAL QUALITY: {opt_quality}/100  |  EXPECTED HITS: {max_hits:.2f}  |  TOTAL VIDEOS: {int(videos_produced[opt_idx])}"
        )
        
        # Render the canvas
        self.canvas.draw()

if __name__ == "__main__":
    app = ViralSimulatorApp()
    app.mainloop()
