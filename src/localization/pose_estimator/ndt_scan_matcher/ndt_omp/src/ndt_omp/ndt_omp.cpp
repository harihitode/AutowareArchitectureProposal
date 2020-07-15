/*
 * Copyright 2020 Tier IV, Inc. All rights reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#include <ndt_omp/ndt_omp.h>
#include <ndt_omp/ndt_omp_impl.hpp>

template class ndt_omp::NormalDistributionsTransform<pcl::PointXYZ, pcl::PointXYZ>;
template class ndt_omp::NormalDistributionsTransform<pcl::PointXYZI, pcl::PointXYZI>;

std::string
ndt_omp::NeighborSearchMethodToString(ndt_omp::NeighborSearchMethod method) {
  switch (method) {
  case ndt_omp::KDTREE:
    return "KDTREE";
  case ndt_omp::DIRECT26:
    return "DIRECT26";
  case ndt_omp::DIRECT7:
    return "DIRECT7";
  case ndt_omp::DIRECT1:
    return "DIRECT1";
  default:
    return "unknown";
  }
}
