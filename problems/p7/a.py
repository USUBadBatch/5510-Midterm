from AStar.a_star import main as main_a_star
from BidirectionalAStar.bidirectional_a_star import main as main_bidirect_a_star
from BreadthFirstSearch.breadth_first_search import main as main_breadth_first_search
from Dijkstra.dijkstra import main as main_dijkstra
from RRTStar.rrt_star import main as main_rrt_star
from BadBatchAStar import main as main_bad_batch_a_star
import time
import tracemalloc


def ave(num_list):
    count = 0
    for num in num_list:
        count += num

    return count / len(num_list)

def main():
    algo_names = [
        "a_star",
        "bad_batch_a_star",
        "bidirectional",
        "breadth_first_search",
        "dijkstra",
        "rrt_star",
    ]
    algo_functions = [
        main_a_star,
        main_bad_batch_a_star,
        main_bidirect_a_star,
        main_breadth_first_search,
        main_dijkstra,
        main_rrt_star,
    ]

    algos = {}
    for algo, func in zip(algo_names, algo_functions):
        algos[algo] = {"time": [], "memory": [], "function": func, "num_nodes": []}


    for _ in range(10):
        for algo in algos:
            start_time = time.time()
            tracemalloc.start()
            algos[algo]['function']()
            algos[algo]['time'].append(time.time() - start_time)
            algos[algo]["memory"].append(tracemalloc.get_traced_memory()[1])
            tracemalloc.stop()


    results = open("RESULTS.md", "w+")
    results.write("### Average Times in Seconds ###\n\n")
    results.write("|  A *  | Bad Batch A * | Bi-Directional A* | Breadth First Search | Dijkstra | RRT Star |\n")
    results.write("|-------|---------------|-------------------|----------------------|----------|----------|\n")

    results.write(f" {ave(algos['a_star']['time']):.2f} |")
    results.write(f" {ave(algos['bad_batch_a_star']['time']):.2f}|")
    results.write(f" {ave(algos['bidirectional']['time']):.2f} |")
    results.write(f" {ave(algos['breadth_first_search']['time']):.2f} |")
    results.write(f" {ave(algos['dijkstra']['time']):.2f} |")
    results.write(f" {ave(algos['rrt_star']['time']):.2f} |")
    results.write('\n\n\n')

    results.write("### Average Peak Memory Use in kB ###\n\n")
    results.write("|  A *  | Bad Batch A * | Bi-Directional A* | Breadth First Search | Dijkstra | RRT Star |\n")
    results.write("|-------|---------------|-------------------|----------------------|----------|----------|\n")
    results.write(f" {ave(algos['a_star']['memory'])/1000:.3f} |")
    results.write(f" {ave(algos['bad_batch_a_star']['memory'])/1000:.3f}|")
    results.write(f" {ave(algos['bidirectional']['memory'])/1000:.3f} |")
    results.write(f" {ave(algos['breadth_first_search']['memory'])/1000:.3f} |")
    results.write(f" {ave(algos['dijkstra']['memory'])/1000:.3f} |")
    results.write(f" {ave(algos['rrt_star']['memory'])/1000:.3f} |")
    # TODO FIgure the cost of the algorithms.


    results.close()

main()
