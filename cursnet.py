import psutil
import time
import curses

# Function to automatically convert bandwidth rates to Kbit/s, Mbit/s, or Gbit/s
def format_bandwidth(rate):
    if rate < 1_000:  # Less than 1000 Kbit/s
        return f"{rate:.2f} Kbit/s"
    elif rate < 1_000_000:  # Less than 1000 Mbit/s
        return f"{rate / 1_000:.2f} Mbit/s"
    else:  # Beyond 1000 Mbit/s
        return f"{rate / 1_000_000:.2f} Gbit/s"

# Function to convert total data sizes to KBytes, MBytes, GBytes, TBytes
def format_data_size(total_bytes):
    total_kbytes = total_bytes / 1024  # Conversion to KBytes
    if total_kbytes < 1_000:  # Less than 1000 KBytes
        return f"{total_kbytes:.2f} KBytes"
    elif total_kbytes < 1_000_000:  # Less than 1000 MBytes
        return f"{total_kbytes / 1_000:.2f} MBytes"
    elif total_kbytes < 1_000_000_000:  # Less than 1000 GBytes
        return f"{total_kbytes / 1_000_000:.2f} GBytes"
    else:  # Beyond 1000 GBytes (in TBytes)
        return f"{total_kbytes / 1_000_000_000:.2f} TBytes"

# Function to get network statistics
def get_network_stats(interface):
    stats = psutil.net_io_counters(pernic=True)[interface]
    return stats.bytes_sent, stats.bytes_recv

# Main function for rendering with curses
def display_network_monitor(stdscr):
    interface = "eth0"  # Change the interface if necessary (e.g., "eth0" or "wlan0")

    # Initialization of variables for calculating statistics
    prev_sent, prev_recv = get_network_stats(interface)
    max_sent, max_recv = 0, 0
    total_sent, total_recv = 0, 0
    min_sent, min_recv = float('inf'), float('inf')
    count = 0

    stdscr.nodelay(True)
    curses.curs_set(0)

    while True:
        # Capture current data
        curr_sent, curr_recv = get_network_stats(interface)

        # Calculate the rate in bits per second
        sent_rate = (curr_sent - prev_sent) * 8 / 1024  # Convert to Kbit/s
        recv_rate = (curr_recv - prev_recv) * 8 / 1024

        # Update max, min, total statistics
        max_sent = max(max_sent, sent_rate)
        max_recv = max(max_recv, recv_rate)
        min_sent = min(min_sent, sent_rate)
        min_recv = min(min_recv, recv_rate)
        total_sent += sent_rate
        total_recv += recv_rate
        count += 1

        avg_sent = total_sent / count
        avg_recv = total_recv / count

        # Update previous data
        prev_sent, prev_recv = curr_sent, curr_recv

        # Clear the screen
        stdscr.clear()

        # Display statistics with dynamic unit conversion
        stdscr.addstr(0, 0, f"Device {interface} [Monitoring]:", curses.A_BOLD)
        stdscr.addstr(2, 0, "Incoming:")
        stdscr.addstr(3, 0, f"Curr: {format_bandwidth(recv_rate)}")
        stdscr.addstr(4, 0, f"Avg:  {format_bandwidth(avg_recv)}")
        stdscr.addstr(5, 0, f"Min:  {format_bandwidth(min_recv)}")
        stdscr.addstr(6, 0, f"Max:  {format_bandwidth(max_recv)}")
        stdscr.addstr(7, 0, f"Ttl:  {format_data_size(total_recv * 1024)}")

        stdscr.addstr(9, 0, "Outgoing:")
        stdscr.addstr(10, 0, f"Curr: {format_bandwidth(sent_rate)}")
        stdscr.addstr(11, 0, f"Avg:  {format_bandwidth(avg_sent)}")
        stdscr.addstr(12, 0, f"Min:  {format_bandwidth(min_sent)}")
        stdscr.addstr(13, 0, f"Max:  {format_bandwidth(max_sent)}")
        stdscr.addstr(14, 0, f"Ttl:  {format_data_size(total_sent * 1024)}")

        stdscr.refresh()
        time.sleep(1)

# Launch the curses interface
if __name__ == "__main__":
    curses.wrapper(display_network_monitor)
