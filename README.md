# 🖱️ Multi-Phase Mouse Position Tracker

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

A powerful, feature-rich Python GUI application for tracking and recording mouse movements across multiple phases. Perfect for automation development, user behavior analysis, game macro creation, and motion pattern studies.

![Demo](screenshot.png)

## 📋 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Technologies Used](#technologies-used)
- [Use Cases](#use-cases)
- [Log Format](#log-format)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)
- [Support](#support)

## ✨ Features

### Core Functionality
- **Multi-Phase Recording**: Track mouse positions across multiple separate recording sessions
- **Interval-Based Tracking**: Record positions at customizable intervals (default: 0.5s)
- **Real-Time Display**: Live X, Y coordinate updates during tracking
- **Phase Transitions**: Automatic prompts to move to different positions between phases
- **Visual Feedback**: Color-coded status indicators for each recording state

### Advanced Features
- **Always on Top**: Keep the tracker visible above all windows
- **Customizable Settings**:
  - Start delay (preparation time before recording)
  - Duration per phase (recording time)
  - Recording interval (frequency of position capture)
  - Number of phases (separate recording sessions)
  - Transition delay between phases (time to reposition)
- **Auto-Save**: Automatically save logs with timestamped filenames
- **Manual Save**: Export logs to custom locations (.txt or .csv format)
- **Statistics**: View average positions, ranges, and totals for each phase
- **Phase Grouping**: Logs organized by phase for easy analysis

### User Interface
- Clean, intuitive Tkinter-based GUI
- Color-coded status indicators (Orange=Transition, Red=Recording, Green=Complete)
- Progress timer with countdown display
- Phase indicator showing current phase number
- Scrollable log viewer with formatted output
- Professional data formatting with headers and separators

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/mouse-tracker.git
cd mouse-tracker
```

### Step 2: Install Dependencies
```bash
pip install pynput
```

**Note**: `tkinter` is usually included with Python. If not installed:
- **Ubuntu/Debian**: `sudo apt-get install python3-tk`
- **Fedora**: `sudo dnf install python3-tkinter`
- **macOS/Windows**: Included by default

### Step 3: Run the Application
```bash
python mouse_tracker.py
```

## 📖 Usage

### Basic Workflow

1. **Configure Settings**:
   - Set start delay (default: 3 seconds) - Time to prepare before recording
   - Set duration per phase (default: 5 seconds) - How long each phase records
   - Set recording interval (default: 0.5 seconds) - Time between captures
   - Set number of phases (default: 3) - Total recording sessions
   - Set transition delay (default: 3 seconds) - Time to move between phases

2. **Start Tracking**:
   - Click "▶ Start Multi-Phase Tracking"
   - Wait for countdown to complete
   - Move mouse naturally during recording phase
   - Status will show "🔴 RECORDING PHASE X..."

3. **Phase Transitions**:
   - After each phase completes, status shows: "⏳ NOW MOVE TO DIFFERENT POSITION!"
   - Reposition your mouse during the transition countdown
   - Next phase begins automatically after countdown
   - Process repeats for all configured phases

4. **Save Results**:
   - **Auto-save** (if enabled): Creates timestamped file `mouse_multiphase_log_YYYYMMDD_HHMMSS.txt`
   - **Manual save**: Click "💾 Save Log" to choose custom location and filename
   - **Clear log**: Click "🗑️ Clear Log" to reset and start fresh

### Example Use Cases

#### Game Automation
```
Phase 1: Record attack button position
Phase 2: Record defense button position  
Phase 3: Record inventory button position
Phase 4: Record menu navigation positions
```

#### UI Testing
```
Phase 1: Record login button locations
Phase 2: Record menu interactions
Phase 3: Record form field positions
Phase 4: Record submit button locations
```

#### Motion Analysis
```
Phase 1: Track mouse movement in top-left quadrant
Phase 2: Track mouse movement in top-right quadrant
Phase 3: Track mouse movement in bottom regions
```

#### Hardware Programming (ATtiny85/Digispark)
```
Record exact positions for programming USB HID devices
to automate mouse movements in games or applications
```

## ⚙️ Configuration

### Settings Breakdown

| Setting | Default | Range | Description |
|---------|---------|-------|-------------|
| Start Delay | 3 sec | 0-60s | Time before first recording starts |
| Duration per Phase | 5 sec | 0.1-300s | How long each phase records |
| Record Interval | 0.5 sec | 0.01-10s | Time between position captures |
| Number of Phases | 3 | 1-50 | Total recording sessions |
| Transition Delay | 3 sec | 0-60s | Time to move between phases |
| Always on Top | ✓ | On/Off | Keep window above others |
| Auto-save | ✓ | On/Off | Save automatically after completion |

### Recording Interval Tips
- **0.01-0.1s**: Very detailed tracking (100-10 points/sec) - for precise movements
- **0.5s**: Balanced tracking (2 points/sec) - recommended for most uses
- **1-2s**: Sparse tracking (1-0.5 points/sec) - for general position marking

## 📊 Log Format

The application generates formatted logs with:
- Session timestamp and configuration
- Phase-separated coordinates
- Individual point timestamps
- Statistical summaries per phase
- Overall averages and ranges

### Example Output
```
Multi-Phase Recording Session: 2025-10-23 23:12:45
Duration per Phase: 5.0s | Interval: 0.5s | Total Phases: 3
===========================================================================

===========================================================================
PHASE 1 - 10 points
===========================================================================
#      X          Y          Time (s)    
---------------------------------------------------------------------------
1      856        423        0.501       
2      892        445        1.002       
3      901        467        1.503       
4      910        489        2.004       
5      925        512        2.505       

Phase 1 Average: X=896.80, Y=467.20

===========================================================================
PHASE 2 - 10 points
===========================================================================
#      X          Y          Time (s)    
---------------------------------------------------------------------------
1      1245       678        0.501       
2      1267       689        1.002       
...

Phase 2 Average: X=1256.50, Y=684.30
```

## 🛠️ Technologies Used

- **Python 3.7+**: Core programming language
- **Tkinter**: GUI framework (built-in with Python)
- **pynput**: Mouse position detection and monitoring library
- **threading**: Concurrent tracking without UI freezing
- **datetime**: Timestamp generation and formatting
- **filedialog**: File save dialog integration

## 💡 Use Cases

### 1. Hardware Automation (ATtiny85/Digispark)
Record positions for programming hardware USB HID devices to automate mouse movements in games or applications that block software automation.

### 2. Macro Development
Create precise mouse macros by recording exact positions and timing sequences for repetitive tasks.

### 3. User Behavior Research
Study mouse movement patterns across different UI regions or tasks for UX optimization.

### 4. Game Automation
Record exact pixel positions for automated gameplay, farming, or testing game mechanics.

### 5. Accessibility Tools
Build assistive technology by understanding user interaction patterns and creating simplified interfaces.

### 6. Quality Assurance Testing
Record test sequences for UI element positioning and regression testing.

### 7. Motion Pattern Analysis
Study and analyze mouse movement efficiency and patterns for ergonomic studies.

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the Repository**
2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit Your Changes**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push to Branch**
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open a Pull Request**

### Ideas for Contributions
- Add CSV export with headers
- Implement click recording (not just position)
- Add visual heatmap generation
- Create playback functionality
- Add keyboard hotkey support
- Implement filters for duplicate positions
- Add screenshot capture at each recorded position
- Create a settings config file
- Add export to JSON format
- Implement pause/resume functionality

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

## 🙏 Acknowledgments

- Built with Python and Tkinter
- Mouse tracking powered by [pynput](https://github.com/moses-palmer/pynput)
- Inspired by automation and accessibility needs
- README template from [Best-README-Template](https://github.com/othneildrew/Best-README-Template)

## 📊 Project Status

**Current Version**: 1.0.0

**Status**: Active Development

**Last Updated**: October 2025

## 🐛 Known Issues

- Very fast mouse movements may be missed between intervals (reduce interval to capture more)
- Always-on-top may not work in some Linux window managers
- Large recording sessions (>1000 points) may slow down the UI slightly

## 📮 Support

For bugs, feature requests, or questions:
- Open an [Issue](https://github.com/yourusername/mouse-tracker/issues)
- Start a [Discussion](https://github.com/yourusername/mouse-tracker/discussions)
- Email: your.email@example.com

## 🗺️ Roadmap

- [ ] Add visual heatmap generation
- [ ] Implement playback mode
- [ ] Add click and drag recording
- [ ] Create keyboard hotkey support
- [ ] Add multi-monitor support
- [ ] Implement recording filters
- [ ] Create mobile companion app
- [ ] Add cloud sync for logs

## 📸 Screenshots

### Main Interface
![Main Interface](screenshots/main.png)

### Recording in Progress
![Recording](screenshots/recording.png)

### Phase Transition
![Transition](screenshots/transition.png)

### Log Output
![Log Output](screenshots/log.png)

---

⭐ **If you find this project useful, please star the repository!** ⭐

---

Made with ❤️ for the automation community
