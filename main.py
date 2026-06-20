import sys
import time
import plotext as plt
from icmplib import ping

def run_cli():
    try:
        ip_address = input("Enter IP address or domain to ping: ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting.")
        return

    if not ip_address:
        print("Error: No IP or domain provided.")
        return

    x_data = []
    y_data = []
    iteration = 0

    # Hide the blinking terminal cursor for a cleaner look
    print("\033[?25l", end="")
    # Clear the entire terminal screen initially
    print("\033[2J", end="")

    try:
        while True:
            try:
                # Rootless ping via icmplib
                host = ping(ip_address, count=1, interval=1, timeout=2, privileged=False)
                
                if host.is_alive:
                    latency = host.avg_rtt
                else:
                    latency = 1000  # High spike for packet loss
            except Exception:
                latency = 1000

            # Manage history tracking arrays
            x_data.append(iteration)
            y_data.append(latency)
            
            # Keep only the last 30 data points for a smooth rolling view
            if len(x_data) > 30:
                x_data.pop(0)
                y_data.pop(0)

            # Clear plotext internal canvas for the next frame
            plt.clf()
            
            # Draw line graph with terminal-friendly themes
            plt.plot(x_data, y_data, marker="dot", color="cyan")
            plt.title(f" Live Ping to {ip_address} (Ctrl+C to Exit) ")
            plt.xlabel("Ping Count")
            plt.ylabel("Latency (ms)")
            plt.grid(True)
            plt.theme("dark")
            
            # Fix graph frame size dynamically inside the user's terminal window
            # Leaving 4 rows of padding at the bottom for safety
            plt.plotsize(plt.terminal_width(), plt.terminal_height() - 4)
            
            # CRITICAL FIX: Reset the terminal cursor back to the top-left (0,0) 
            # instead of letting the text spill downwards into new rows.
            print("\033[H", end="")
            
            # Render the canvas buffer directly onto the terminal
            plt.show()
            
            # Wait 1 second and increment counter
            time.sleep(1)
            iteration += 1

    except KeyboardInterrupt:
        # Restore the standard blinking text cursor when exiting
        print("\033[?25h\nPing monitoring stopped.")

if __name__ == "__main__":
    run_cli()
