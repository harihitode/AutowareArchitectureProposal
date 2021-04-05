import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math
import sys

log_path = ""
log_file_names = [
    "convert.log",
    "interpolate.log",
    "filter.log",
    "ndt_scan_matcher.log",
]
sub_file_names = [
    "convert_sub.log",
    "interpolate_sub.log",
    "filter_sub.log",
    "ndt_scan_matcher_sub.log",
]

log_node_name_2_idx = {
    "/sensing/lidar/top/velodyne_nodelet_manager_cloud start": 0,
    "/sensing/lidar/top/velodyne_nodelet_manager_cloud end" : 1,
    "/sensing/lidar/top/velodyne_nodelet_manager_crop_box_filter_self start": 2,
    "/sensing/lidar/top/velodyne_nodelet_manager_crop_box_filter_self end": 3,
    "/sensing/lidar/top/velodyne_nodelet_manager_crop_box_filter_mirror start": 4,
    "/sensing/lidar/top/velodyne_nodelet_manager_crop_box_filter_mirror end": 5,
    "/sensing/lidar/top/velodyne_nodelet_manager_fix_distortion start": 6,
    "/sensing/lidar/top/velodyne_nodelet_manager_fix_distortion end": 7,
    "/localization/util/crop_box_filter_mesurement_range start": 8,
    "/localization/util/crop_box_filter_mesurement_range end": 9,
    "/localization/util/voxel_grid_filter start": 10,
    "/localization/util/voxel_grid_filter end": 11,
    "/localization/pose_estimator/ndt_scan_matcher start": 12,
    "/localization/pose_estimator/ndt_scan_matcher end": 13,
}

log_graph = [
    [1], # node-0
    [0, 2], # node-1
    [1, 3], # node-2
    [2, 4], # node-3
    [3, 5], # node-4
    [4, 6], # node-5
    [5, 7], # node-6
    [6, 8], # node-7
    [7, 9], # node-8
    [8, 10], # node-9
    [9, 11], # node-10
    [10, 12], # node-11
    [11, 13], # node-12
    [12], # node-13
]

viz_node_names = [
    "velodyne_cloud", # node-0
    "velodyne_crop_box_filter_self", # node-1
    "velodyne_crop_box_filter_mirror", # node-2
    "velodyne_fix_distortion", # node-3
    "crop_box_filter_mesurement_range", # node-4
    "voxel_grid_filter", # node-5
    "ndt_scan_matcher", # node-6
]

viz_edges = [
    (0, 1), # edge-0
    (1, 2), # edge-1
    (2, 3), # edge-2
    (3, 4), # edge-3
    (4, 5), # edge-4
    (5, 6), # edge-5
]

IS_NODE = 0
IS_EDGE = 1

section2id = {
    (0, 1): (IS_NODE, 0),
    (1, 2): (IS_EDGE, 0),
    (2, 3): (IS_NODE, 1),
    (3, 4): (IS_EDGE, 1),
    (4, 5): (IS_NODE, 2),
    (5, 6): (IS_EDGE, 2),
    (6, 7): (IS_NODE, 3),
    (7, 8): (IS_EDGE, 3),
    (8, 9): (IS_NODE, 4),
    (9, 10): (IS_EDGE, 4),
    (10, 11): (IS_NODE, 5),
    (11, 12): (IS_EDGE, 5),
    (12, 13): (IS_NODE, 6),
}

data_nodes = [{} for _ in range(len(log_node_name_2_idx))]
sub_data_nodes = [{} for _ in range(len(log_node_name_2_idx))]
viz_nodes_latencies = [[] for _ in range(len(viz_node_names))]
viz_edges_latencies = [[] for _ in range(len(viz_edges))]
e2e_latencies = []
nodes_latency_ave = np.array([0 for _ in range(len(viz_nodes_latencies))])
edges_latency_ave = np.array([0 for _ in range(len(viz_edges_latencies))])
nodes_latency_tail = np.array([0 for _ in range(len(viz_nodes_latencies))])
edges_latency_tail = np.array([0 for _ in range(len(viz_edges_latencies))])

def parse_files():
    for log_file_name in log_file_names:
        with open(log_path + log_file_name) as f:
            for line in f:
                ret = line.rstrip().split()
                if len(ret) != 4:
                    continue
                name, part, stamp, realtime = ret
                log_node_name = name + "." + part
                if not log_node_name in log_node_name_2_idx:
                    continue
                idx = log_node_name_2_idx[log_node_name]
                data_nodes[idx][int(stamp)] = int(realtime)

def parse_sub_files():
    for sub_file_name in sub_file_names:
        with open(log_path + sub_file_name) as f:
            for line in f:
                ret = line.rstrip().split()
                if len(ret) != 3:
                    continue
                name, start_stamp, end_stamp = ret
                if not (name + ".start") in log_node_name_2_idx:
                    continue
                if not (name + ".end") in log_node_name_2_idx:
                    continue
                sub_data_nodes[log_node_name_2_idx[name + ".start"]][int(start_stamp)] = int(end_stamp)
                sub_data_nodes[log_node_name_2_idx[name + ".end"]][int(end_stamp)] = int(start_stamp)

def calc_latency(start_node, start_stamp):
    viz_node_latencies = [-1 for _ in range(len(viz_node_names))]
    viz_edge_latencies = [-1 for _ in range(len(viz_edges))]

    visited = [False for _ in range(len(log_node_name_2_idx))]
    stack = []
    stack.append(start_node)
    stamp = start_stamp

    while len(stack) > 0:
        node = stack.pop()
        visited[node] = True
        for next_node in log_graph[node]:
            if visited[next_node]:
                continue

            is_edge, viz_idx = section2id[(min(node, next_node), max(node, next_node))]
            before_stamp = stamp

            if not is_edge:
                if not stamp in sub_data_nodes[node]:
                    continue
                stamp = sub_data_nodes[node][stamp]

            if not stamp in data_nodes[next_node]:
                continue

            stack.append(next_node)
            realtime_diff = abs(data_nodes[node][before_stamp] - data_nodes[next_node][stamp])

            if is_edge:
                viz_edge_latencies[viz_idx] = realtime_diff
            else:
                viz_node_latencies[viz_idx] = realtime_diff

    for val in viz_node_latencies:
        if val < 0:
            return
    for val in viz_edge_latencies:
        if val < 0:
            return

    for i in range(len(viz_node_latencies)):
        viz_nodes_latencies[i].append(viz_node_latencies[i])
    for i in range(len(viz_edge_latencies)):
        viz_edges_latencies[i].append(viz_edge_latencies[i])

    # TODO: Generalize this part
    sm = 0
    for val in viz_node_latencies:
        sm += val
    for val in viz_edge_latencies:
        sm += val
    e2e_latencies.append(sm)

def calc_latencies():
    for stamp in data_nodes[13]:
        calc_latency(13, stamp)

def calc_latency_ave():
    for i in range(len(nodes_latency_ave)):
        sm = 0
        for val in viz_nodes_latencies[i]:
            sm += val
        nodes_latency_ave[i] = sm / len(viz_nodes_latencies[i])
    for i in range(len(edges_latency_ave)):
        sm = 0
        for val in viz_edges_latencies[i]:
            sm += val
        edges_latency_ave[i] = sm / len(viz_edges_latencies[i])

def calc_latency_tail(rate):
    for i in range(len(viz_nodes_latencies)):
        n = len(viz_nodes_latencies[i])
        tail_num = math.ceil(n * rate)
        samples = viz_nodes_latencies[i].copy()
        samples.sort()
        sm = 0
        for j in range(n - tail_num, n):
            sm += samples[j]
        nodes_latency_tail[i] = sm / tail_num
    for i in range(len(viz_edges_latencies)):
        n = len(viz_edges_latencies[i])
        tail_num = math.ceil(n * rate)
        samples = viz_edges_latencies[i].copy()
        samples.sort()
        sm = 0
        for j in range(n - tail_num, n):
            sm += samples[j]
        edges_latency_tail[i] = sm / tail_num

def visualize_graph():
    edge_labels = {}
    for i in range(len(viz_edges)):
        edge_labels[viz_edges[i]] = str(edges_latency_ave[i].astype(int) / 1000) + "ms,\n" + \
          str(edges_latency_tail[i].astype(int) / 1000) + "ms"

    node_labels = {}
    for i in range(len(viz_node_names)):
        node_labels[i] = viz_node_names[i] + "\n" + str(nodes_latency_ave[i].astype(int) / 1000) + \
          "ms,\n" + str(nodes_latency_tail[i].astype(int) / 1000) + "ms"

    G = nx.DiGraph()
    G.add_edges_from(viz_edges)
    pos = nx.spring_layout(G, scale=0.8)
    nx.draw(G,pos,edge_color='black',width=1,linewidths=1,node_size=2000,node_color='pink',alpha=0.9, labels=node_labels)
    nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels,font_color='red')

def visualize_e2e_latencies(bins):
    fig = plt.figure(figsize=(16, 9))
    ax0 = fig.add_subplot(1, 1, 1)
    ax0.set_title("e2e latency (lidar_packet ~ ndt_scan_matcher)")
    ax0.set_xlabel("latency(msec)")
    ax0.set_ylabel("samples num")
    ax0.hist(np.array(e2e_latencies) / 1000, bins=bins)

def print_usage():
    print("Usage: python parse2graph.py <path to log direcotory> <tail latency rate>")

def main():
    global log_path
    if (len(sys.argv) != 3):
        print_usage()
        return
    log_path = sys.argv[1]
    tail_rate = float(sys.argv[2])

    parse_files()
    parse_sub_files()
    calc_latencies()
    calc_latency_ave()
    calc_latency_tail(tail_rate)

    plt.rcParams["figure.figsize"] = (16, 8)
    visualize_graph()
    visualize_e2e_latencies(200)
    plt.show()

if __name__ == "__main__":
    main()
