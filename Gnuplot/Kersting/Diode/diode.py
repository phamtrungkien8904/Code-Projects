import math
import numpy as np

BOLTZMANN = 1.380649e-23
ELEMENTARY_CHARGE = 1.602176634e-19


def thermal_voltage(temperature_kelvin: float) -> float:
    """Return the thermal voltage kT/q for the supplied temperature."""
    return (BOLTZMANN * temperature_kelvin) / ELEMENTARY_CHARGE


def diode_series_current(
    v_source: float,
    v_stage: float,
    r_source: float,
    saturation_current: float,
    thermal_volt: float,
    max_iterations: int = 25,
    tolerance: float = 1e-12,
) -> float:
    """Solve the series resistor + diode current using the Shockley equation."""
    if v_source <= v_stage:
        return 0.0

    available_drop = v_source - v_stage
    diode_voltage = min(available_drop, 0.7)

    for _ in range(max_iterations):
        exp_term = math.exp(diode_voltage / thermal_volt)
        diode_current = saturation_current * (exp_term - 1.0)
        resistor_current = (available_drop - diode_voltage) / r_source
        residual = diode_current - resistor_current

        if abs(residual) < tolerance:
            break

        derivative = saturation_current * exp_term / thermal_volt + 1.0 / r_source
        diode_voltage -= residual / derivative

        if diode_voltage < 0.0:
            diode_voltage = 0.0
        elif diode_voltage > available_drop:
            diode_voltage = available_drop

    return max((available_drop - diode_voltage) / r_source, 0.0)

def sawtooth_wave(time_vector: np.ndarray, period: float, v_min: float, v_max: float) -> np.ndarray:
    phase = (time_vector / period) % 1.0
    return v_min + (v_max - v_min) * phase


def simulate_four_pole_diode_network(
    duration: float = 0.01,
    sample_rate: float = 500_000.0,
    source_frequency: float = 1_000.0,
    v_min: float = 0.0,
    v_max: float = 5.0,
    r_source: float = 500.0,
    r_stage: float = 1_000.0,
    c_stage: float = 1e-6,
    r_load: float = 10_000.0,
    diode_is: float = 4.352e-9,
    temperature: float = 300.0,
    n_stages: int = 4,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    n_steps = int(duration * sample_rate) + 1
    time_vector = np.arange(n_steps) / sample_rate
    vin = sawtooth_wave(time_vector, 1.0 / source_frequency, v_min, v_max)

    stage_voltages = np.zeros((n_stages, n_steps))
    dt = 1.0 / sample_rate
    vt = thermal_voltage(temperature)

    for k in range(1, n_steps):
        previous = stage_voltages[:, k - 1].copy()
        updated = previous.copy()

        input_current = diode_series_current(
            v_source=vin[k],
            v_stage=previous[0],
            r_source=r_source,
            saturation_current=diode_is,
            thermal_volt=vt,
        )

        if n_stages == 1:
            load_current = previous[0] / r_load
            updated[0] = previous[0] + dt * (input_current - load_current) / c_stage
        else:
            current_to_next = (previous[0] - previous[1]) / r_stage
            updated[0] = previous[0] + dt * (input_current - current_to_next) / c_stage

            for idx in range(1, n_stages - 1):
                current_from_prev = (previous[idx - 1] - previous[idx]) / r_stage
                current_to_next = (previous[idx] - previous[idx + 1]) / r_stage
                updated[idx] = previous[idx] + dt * (current_from_prev - current_to_next) / c_stage

            current_from_prev = (previous[-2] - previous[-1]) / r_stage
            load_current = previous[-1] / r_load
            updated[-1] = previous[-1] + dt * (current_from_prev - load_current) / c_stage

        stage_voltages[:, k] = updated

    outputs = np.column_stack((time_vector, vin, stage_voltages[-1]))
    header = "time,input_v,output_v"
    np.savetxt("diode_response.csv", outputs, delimiter=",", header=header, comments="")
    return time_vector, vin, stage_voltages[-1]


if __name__ == "__main__":
    simulate_four_pole_diode_network()