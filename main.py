import matplotlib.pyplot as plt
from pythonping import ping
import time

# Get IP address from the user
ip_address = input("Enter IP address or domain to ping: ")

# Set up the live plot
plt.style.use('dark_background')
fig, ax = plt.subplots()
x_data = []
y_data = []

# Create the line object
line, = ax.plot(x_data, y_data, marker='o', color='cyan')
ax.set_title(f"Live Ping to {ip_address}")
ax.set_xlabel("Ping Attempt")
ax.set_ylabel("Latency (ms)")
plt.grid(True, alpha=0.3)

iteration = 0
try:
    while True:
        # Send 1 ICMP request
        response = ping(ip_address, count=1, timeout=2)
        
        # Extract latency or handle packet loss
        if response.rtt_avg_ms is not None:
            latency = response.rtt_avg_ms
        else:
            latency = 1000 # Spike graph if the ping fails
            
        # Update data arrays
        x_data.append(iteration)
        y_data.append(latency)
        
        # Keep only the last 20 points for a moving timeline
        if len(x_data) > 20:
            x_data.pop(0)
            y_data.pop(0)
            
        # Refresh the graph
        line.set_xdata(x_data)
        line.set_ydata(y_data)
        ax.relim()
        ax.autoscale_view()
        
        plt.draw()
        plt.pause(1)
        iteration += 1

except KeyboardInterrupt:
    print("\nPing monitoring stopped.")
    plt.close()
    