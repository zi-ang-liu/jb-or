import matplotlib.pyplot as plt
import numpy as np

# Parameters
Q = 100                   # Order quantity
demand_mean = 350         # Average demand rate
demand_std = 100           # Standard deviation of demand
T = 10
L = 3                  # Lead time
z = 1.645                 # For 95% service level

# Safety stock based on uncertainty during lead time
safety_stock = 10

# Time array
t = np.linspace(0, 3 * T, 1000)

# Simulate cumulative demand over time with uncertainty
np.random.seed(0)
dt = t[1] - t[0]
random_demand = np.random.normal(demand_mean, demand_std, size=len(t)) * dt
cumulative_demand = np.cumsum(random_demand)

# Initialize inventory level
inventory = np.zeros_like(t)
inventory[0] = Q + safety_stock  # Start with full cycle + safety stock

# Track orders
order_times = [0]
next_order_time = T

for i in range(1, len(t)):
    time = t[i]
    
    # Consume inventory
    inventory[i] = inventory[i - 1] - random_demand[i]

    # Place order if time has reached the next cycle
    if time >= next_order_time:
        inventory[i] += Q  # Replenishment
        order_times.append(time)
        next_order_time += T

# Ensure inventory does not drop below 0 (stockouts possible)
inventory = np.maximum(inventory, 0)

# --- Plotting ---
plt.figure(figsize=(12, 6))
plt.plot(t, inventory, label="Inventory Level (with SS, L, demand variability)", color="black", linewidth=2)
plt.axhline(safety_stock, color="red", linestyle="--", label="Safety Stock")
for ot in order_times:
    plt.axvline(ot, color="blue", linestyle=":", alpha=0.3)

plt.xlabel("Time", fontsize=14)
plt.ylabel("Inventory Level", fontsize=14)
plt.ylim(bottom=0, top=Q + safety_stock + 100)
plt.title("(r, Q) Policy with Uncertain Demand, Lead Time, and Safety Stock", fontsize=16)
plt.legend(fontsize=12)
plt.grid(True)
plt.tight_layout()
plt.show()
