# Evaluation tools
The evaluation tools in this directory visualize e2e latencies on the ROS dependency graph.

## How to use
Before playing rosbag for measurement, make sure that there is `~/.ros/eval_log` directory on your machine.

After playing rosbag, you can see several log files in the directory. You can see e2e latency graphs by executing the script as below.

```
$ python parse2graph.py <path to log directory (~/.ros/eval_log)> <tail latency rate(0.05)>
```

The log files are appended by default, so when you retake, do not forget to replace the old log files.

Author: @sykwer
