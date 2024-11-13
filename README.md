# A Unified Cross-Scene Cross-Domain Benchmark for Open-World Drone Active Tracking
[![Software License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Document-en](https://img.shields.io/badge/doc-guide-blue)](https://forcvpr2025.github.io/anonymous/)
[![Document-zh](https://img.shields.io/badge/文档-指引-blue)](https://forcvpr2025.github.io/anonymous/zh/index.html)

![cover1](./readmeCache/cover1.png)
![cover](./readmeCache/cover.gif)

## Abstract
Drone Visual Active Tracking aims to autonomously follow a target object by controlling the motion system based on visual observations, providing a more practical solution for effective tracking in dynamic environments. However, accurate Drone Visual Active Tracking using reinforcement learning remains challenging due to the absence of a unified benchmark, the complexity of real-world environments with frequent interference, and the diverse behaviors of dynamic targets. To address these issues, we propose a novel drone visual active tracking benchmark called **DAT**. The DAT benchmark provides 24 visually complex environments to assess cross-domain and cross-scene generalization abilities of tracking algorithms, along with high-fidelity modeling of realistic robot dynamics. Additionally, we propose a reinforcement learning-based drone tracking method called **R-VAT**. Specifically, inspired by curriculum learning, we introduce a Curriculum-Based Training strategy for tracking that progressively enhances the agent tracking performance in increasingly difficult scenarios. We develop a goal-centered reward function to provide precise rewards to the drone agent. Experiments demonstrate that the R-VAT has about 400% improvement over the SOTA method in terms of the cumulative reward metric.


## Citing
```bibtex
@article{ ,
  title={An Open-World Cross-Scene Benchmark for Drone Visual Active Tracking},
  author={},
  journal={},
  year={},
  publisher={}
}
```
