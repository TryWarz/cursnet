
# CursNet

**CursNet** is a Python-based terminal tool for real-time network monitoring, designed to display dynamic data rates and statistics for a specified network interface.

## Features

- Monitors **incoming** and **outgoing** network traffic in real-time
- Shows **current**, **average**, **min**, **max**, and **total** data usage statistics
- Automatically converts data rates to Kbit/s, Mbit/s, or Gbit/s and totals to KBytes, MBytes, GBytes, or TBytes
- Displays results in an easy-to-read terminal interface using the `curses` library

## Requirements

- **Python 3**
- **psutil** library
- **curses** library (usually built into Python)

To install `psutil`, run:
```bash
pip install psutil
```

## How It Works

1. **Initialize**: The program initializes the network interface (default is `eth0`, but can be changed in the code).
2. **Data Collection**: Each second, it captures the current data sent and received on the interface.
3. **Calculations**:
   - Computes **current** send and receive rates.
   - Updates **maximum**, **minimum**, **average**, and **total** data rates.
   - Formats these values for display.
4. **Display**: Using `curses`, CursNet displays statistics for incoming and outgoing traffic in the terminal.

## Usage

1. Clone or download the script.
2. Run the program in the terminal:
    ```bash
    python net_monitor.py
    ```
   Replace `net_monitor.py` with the actual filename if different.

3. **Navigate**: The interface refreshes every second, showing live updates of network statistics.

## Code Overview

- `format_bandwidth(rate)`: Converts data rates to Kbit/s, Mbit/s, or Gbit/s.
- `format_data_size(total_bytes)`: Converts data totals to KBytes, MBytes, GBytes, or TBytes.
- `get_network_stats(interface)`: Retrieves network statistics for the specified interface.
- `display_network_monitor(stdscr)`: Main function for displaying stats in the terminal using `curses`.

## Customization

- **Interface**: Change the `interface` variable in `display_network_monitor()` to monitor a different network interface (e.g., `wlan0` for Wi-Fi).
- **Refresh Rate**: Adjust the `time.sleep(1)` line to change the update frequency.

## Example

After running, you’ll see something like:

```plaintext
Device eth0 [Monitoring]:

Incoming:
Curr: 45.00 Kbit/s
Avg:  30.00 Kbit/s
Min:  10.00 Kbit/s
Max:  70.00 Kbit/s
Ttl:  1.20 MBytes

Outgoing:
Curr: 30.00 Kbit/s
Avg:  20.00 Kbit/s
Min:  5.00 Kbit/s
Max:  40.00 Kbit/s
Ttl:  0.75 MBytes
```

## License

This project is licensed under the MIT License.
