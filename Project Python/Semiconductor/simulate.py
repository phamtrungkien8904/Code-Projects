import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt

# -----------------------------
# Problem setup
# -----------------------------
omega_n = 2.0
zeta = 0.15
x0 = 1.0
v0 = 0.0

# Analytic solution (underdamped)
omega_d = omega_n * np.sqrt(1 - zeta**2)
def analytic(t):
    A = x0
    B = (v0 + zeta*omega_n*x0) / omega_d
    return np.exp(-zeta*omega_n*t) * (A*np.cos(omega_d*t) + B*np.sin(omega_d*t))

# -----------------------------
# PINN model
# -----------------------------
class PINN(nn.Module):
    def __init__(self, layers):
        super().__init__()
        self.net = nn.Sequential()
        for i in range(len(layers)-1):
            self.net.add_module(f"layer_{i}", nn.Linear(layers[i], layers[i+1]))
            if i < len(layers)-2:
                self.net.add_module(f"tanh_{i}", nn.Tanh())

    def forward(self, t):
        return self.net(t)

# Physics residual
def physics_residual(model, t):
    t.requires_grad_(True)
    x = model(t)
    x_t = torch.autograd.grad(x, t, grad_outputs=torch.ones_like(x), create_graph=True)[0]
    x_tt = torch.autograd.grad(x_t, t, grad_outputs=torch.ones_like(x_t), create_graph=True)[0]
    return x_tt + 2*zeta*omega_n*x_t + omega_n**2 * x

# -----------------------------
# Training data
# -----------------------------
t_colloc = torch.linspace(0, 10, 200).reshape(-1,1)
t0 = torch.tensor([[0.0]], requires_grad=True)

# Initial conditions
x0_t = torch.tensor([[x0]])
v0_t = torch.tensor([[v0]])

# -----------------------------
# Train PINN
# -----------------------------
model = PINN([1, 32, 32, 32, 1])
optimizer = optim.Adam(model.parameters(), lr=1e-3)

for epoch in range(3000):
    optimizer.zero_grad()
    # Physics loss
    res = physics_residual(model, t_colloc)
    loss_physics = torch.mean(res**2)

    # Initial condition losses
    x_init = model(t0)
    x_t_init = torch.autograd.grad(x_init, t0, grad_outputs=torch.ones_like(x_init), create_graph=True)[0]
    loss_ic = (x_init - x0_t).pow(2).mean() + (x_t_init - v0_t).pow(2).mean()

    loss = loss_physics + loss_ic
    loss.backward()
    optimizer.step()

    if epoch % 500 == 0:
        print(f"Epoch {epoch}, Loss: {loss.item():.6e}")

# -----------------------------
# Compare with analytic solution
# -----------------------------
t_test = np.linspace(0, 10, 400)
x_true = analytic(t_test)

with torch.no_grad():
    t_tensor = torch.tensor(t_test.reshape(-1,1), dtype=torch.float32)
    x_pred = model(t_tensor).numpy().flatten()

plt.figure(figsize=(8,5))
plt.plot(t_test, x_true, label="Analytic", linewidth=2)
plt.plot(t_test, x_pred, "--", label="PINN Prediction")
plt.xlabel("t")
plt.ylabel("x(t)")
plt.legend()
plt.title("Damped Oscillator: PINN vs Analytic")
plt.grid(True)
plt.show()