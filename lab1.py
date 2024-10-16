import numpy as np
import matplotlib.pyplot as plt
import sqlite3
from scipy import signal

# Функция генерации сигнала
def create_signal(time, num_exp, num_cos, num_log, amp_exp, amp_cos, amp_log):
    total_signal = np.zeros_like(time)

    # Константы
    exp_const = 1  # Константа для экспоненциальной функции
    freq_base = 2 * np.pi  # Базовая частота для косинусных членов
    phase_shift = 0  # Начальный фазовый сдвиг для косинусных членов

    # Добавляем экспоненциальные члены
    if num_exp > 0:
        for i in range(num_exp):
            exp_amp = amp_exp[i] if i < len(amp_exp) else 0
            total_signal += exp_amp * np.exp(-time / exp_const)

    # Добавляем косинусные члены
    if num_cos > 0:
        for j in range(num_cos):
            cos_amp = amp_cos[j] if j < len(amp_cos) else 0
            frequency = freq_base * (j + 1)
            total_signal -= cos_amp * np.cos(frequency * time + phase_shift)

    # Добавляем логарифмические члены
    if num_log > 0:
        for k in range(num_log):
            log_amp = amp_log[k] if k < len(amp_log) else 0
            total_signal += log_amp * np.log(1 + time)  # Используем log(1 + time), чтобы избежать log(0)

    return total_signal

# Время t
t = np.linspace(0.1, 10, 1000)

# Значения для варианта 24
n = 3  # Экспоненциальные члены
m = 1  # Косинусные члены
l = 2  # Логарифмические члены
A_vals = [0.73, 0.15, 0.5]  # Амплитуды экспоненциальных членов
B_vals = [1.0]  # Амплитуда косинусного члена
C_vals = [0.3, 0.2]  # Амплитуды логарифмических членов

# Генерация сигнала
generated_signal = create_signal(t, n, m, l, A_vals, B_vals, C_vals)

# Визуализация результата
plt.plot(t, generated_signal)
plt.title('Сгенерированный сигнал для варианта 24 с логарифмическими членами')
plt.xlabel('Время (t)')
plt.ylabel('Сигнал (s)')
plt.grid(True)
plt.show()
