# An Open-World Cross-Scene Benchmark for Drone Visual Active Tracking
[![Software License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Document-en](https://img.shields.io/badge/doc-guide-blue)](https://forcvpr2025.github.io/anonymous/)
[![Document-zh](https://img.shields.io/badge/文档-指引-blue)](https://forcvpr2025.github.io/anonymous/zh/index.html)

![cover1](./readmeCache/cover1.png)
![cover](./readmeCache/cover.gif)

## Abstract
Drone Visual Active Tracking aims to autonomously follow a target object by controlling the motion system based on visual observations, providing a more practical solution for effective tracking in dynamic environments. However, this task is very challenging due to the diverse and dynamic nature of real-world scenarios and difficulties such as limited access to real-world training data and complex algorithm training requirements. To address the above challenges, we propose a novel drone visual active tracking benchmark called **DAT**. The DAT benchmark provides 24 visually complex environments to assess cross-domain and cross-scene generalization abilities of tracking algorithms, along with high-fidelity modeling of realistic robot dynamics. Additionally, we propose a new reinforcement learning-based drone tracking method called **R-VAT**. Specifically, we develop a goal-centered reward function to provide precise rewards to the drone agent. Inspired by curriculum learning, we introduce a Curriculum-Based Training strategy for tracking that progressively enhances the agent tracking performance in increasingly difficult scenarios. Experiments demonstrate that the R-VAT has about 400\% improvement over the SOTA method in the *CR* metric.


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