from AStar.a_star import main as main_a_star
from BidirectionalAStar.bidirectional_a_star import main as main_bidirect_a_star
from BreadthFirstSearch.breadth_first_search import main as main_breadth_first_search
from Dijkstra.dijkstra import main as main_dijkstra
from RRTStar.rrt_star import main as main_rrt_star
import time


def ave(num_list):
    count = 0
    for num in num_list:
        count += num

    return count / len(num_list)

def main():
    a_star = []
    bad_batch_a_star = []
    bidirectional = []
    breadth_first_search = []
    dijkstra = []
    rrt_star = []


    for i in range(10):
        a_star_start = time.time()
        main_a_star()
        a_star.append(time.time() - a_star_start)

        # TODO: ask and implement this
        bad_batch_start = time.time()
        # main_bad_batch_a_star()
        bad_batch_a_star.append(time.time() - bad_batch_start)

        bidirect_star_start = time.time()
        main_bidirect_a_star()
        bidirectional.append(time.time() - bidirect_star_start)

        breadth_first_start = time.time()
        main_breadth_first_search()
        breadth_first_search.append(time.time() - breadth_first_start)

        dijkstra_start = time.time()
        main_dijkstra()
        dijkstra.append(time.time() - dijkstra_start)

        rrt_star_start = time.time()
        main_rrt_star()
        rrt_star.append(time.time() - rrt_star_start)


    results = open("RESULTS.md", "w+")
    results.write("### Average Times in Seconds ###\n\n")
    results.write("|  A *  | Bad Batch A * | Bi-Directional A* | Breadth First Search | Dijkstra | RRT Star |\n")
    results.write("|-------|---------------|-------------------|----------------------|----------|----------|\n")
    results.write(f' {ave(a_star):.2f} |')
    results.write(f" {ave(bad_batch_a_star):.2f}|")
    results.write(f" {ave(bidirectional):.2f} |")
    results.write(f" {ave(breadth_first_search):.2f} |")
    results.write(f" {ave(dijkstra):.2f} |")
    results.write(f" {ave(rrt_star):.2f} |")
    results.write('\n')

    # TODO FIgure the cost of the algorithms.


    results.close()

main()
