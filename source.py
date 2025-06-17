import time
import threading
import multiprocessing
import platform
import matplotlib.pyplot as plt
import psutil
import statistics
import os

# Função simulando carga CPU-bound
def tarefa_pesada(n):
    total = 0
    for i in range(n):
        total += i
    return total

# Execução com threads
def executar_threading(n_threads, tamanho):
    threads = []
    inicio = time.time()
    for _ in range(n_threads):
        t = threading.Thread(target=tarefa_pesada, args=(tamanho,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    fim = time.time()
    return fim - inicio

# Execução com processos
def executar_multiprocessing(n_proc, tamanho):
    processos = []
    inicio = time.time()
    for _ in range(n_proc):
        p = multiprocessing.Process(target=tarefa_pesada, args=(tamanho,))
        processos.append(p)
        p.start()
    for p in processos:
        p.join()
    fim = time.time()
    return fim - inicio

if __name__ == "__main__":
    nome = input("Digite seu nome completo: ")
    tamanho_tarefa = 10**7
    paralelismos = [1, 2, 4, 8]

    tempos_thread = []
    tempos_proc = []

    print("\nIniciando teste de desempenho em ambiente virtualizado...\n")

    for n in paralelismos:
        tempo_t = executar_threading(n, tamanho_tarefa)
        tempo_p = executar_multiprocessing(n, tamanho_tarefa)
        tempos_thread.append(tempo_t)
        tempos_proc.append(tempo_p)

    # Cálculo de métricas
    speedup_t = [tempos_thread[0] / t for t in tempos_thread]
    speedup_p = [tempos_proc[0] / p for p in tempos_proc]
    eficiencia_t = [s / n for s, n in zip(speedup_t, paralelismos)]
    eficiencia_p = [s / n for s, n in zip(speedup_p, paralelismos)]

    throughput_t = [tamanho_tarefa / t for t in tempos_thread]
    throughput_p = [tamanho_tarefa / p for p in tempos_proc]

    desvio_thread = statistics.stdev(tempos_thread)
    desvio_proc = statistics.stdev(tempos_proc)

    os.makedirs("graficos", exist_ok=True)

    plt.figure()
    plt.plot(paralelismos, tempos_thread, 'o-', label='Threading')
    plt.plot(paralelismos, tempos_proc, 'o-', label='Multiprocessing')
    plt.xlabel('Threads/Processos')
    plt.ylabel('Tempo (s)')
    plt.title('Tempo de Execução')
    plt.grid(True)
    plt.legend()
    plt.savefig("graficos/tempo_execucao.png")

    plt.figure()
    plt.plot(paralelismos, speedup_t, 'o-', label='Speedup Threading')
    plt.plot(paralelismos, speedup_p, 'o-', label='Speedup Multiprocessing')
    plt.xlabel('Threads/Processos')
    plt.ylabel('Speedup')
    plt.title('Speedup Comparativo')
    plt.grid(True)
    plt.legend()
    plt.savefig("graficos/speedup.png")

    plt.figure()
    plt.plot(paralelismos, eficiencia_t, 'o-', label='Eficiência Threading')
    plt.plot(paralelismos, eficiencia_p, 'o-', label='Eficiência Multiprocessing')
    plt.xlabel('Threads/Processos')
    plt.ylabel('Eficiência')
    plt.title('Eficiência vs Threads')
    plt.grid(True)
    plt.legend()
    plt.savefig("graficos/eficiencia.png")

    # Salvar resultados
    with open("graficos/relatorio.txt", "w") as f:
        f.write(f"Nome: {nome}\n")
        f.write(f"CPU: {platform.processor()}\n")
        f.write(f"Clock (GHz): {psutil.cpu_freq().max / 1000:.2f}\n\n")

        f.write("Resultados por Paralelismo:\n")
        for i, n in enumerate(paralelismos):
            f.write(f"{n} threads:\n")
            f.write(f"  Threading: {tempos_thread[i]:.2f}s | Speedup: {speedup_t[i]:.2f} | Eficiência: {eficiencia_t[i]:.2f} | Throughput: {throughput_t[i]:.2f} it/s\n")
            f.write(f"  Multiproc: {tempos_proc[i]:.2f}s | Speedup: {speedup_p[i]:.2f} | Eficiência: {eficiencia_p[i]:.2f} | Throughput: {throughput_p[i]:.2f} it/s\n")

        f.write(f"\nDesvio Padrão (Threading): {desvio_thread:.4f} s\n")
        f.write(f"Desvio Padrão (Multiproc): {desvio_proc:.4f} s\n")

        f.write("\n\nLei de Amdahl (estimativa):\n")
        f.write("Speedup_total = 1 / ((1 - f) + (f / p))\n")
        f.write("Para f = 0.95 e p = 8: S ≈ %.2f\n" % (1 / ((1 - 0.95) + (0.95 / 8))))

    print("\nTestes finalizados! Verifique a pasta 'graficos' para imagens e relatórios.")

