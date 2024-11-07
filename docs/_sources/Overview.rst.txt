Overview
=================

.. raw:: html

    <style>
        #language-switch {
           display: flex; /* Use Flexbox layout */
           justify-content: center; /* Center buttons horizontally */
           align-items: center; /* Center buttons vertically */
           gap: 10px; /* Space between buttons */
           margin-top: 20px;
           margin-bottom: 20px;
       }
       #language-switch button {
           width: 180px;
           height: 40px;
           font-size: 16px;
           padding: 10px;
           margin: 5px;
           border: 1px solid #ccc;
           border-radius: 5px;
           cursor: pointer;
           text-align: center;
           background-color: #f0f0f0;
           display: flex;
           align-items: center; /* Center text vertically */
           justify-content: center; /* Center text horizontally */
       }
   </style>

    <!-- Language switch buttons -->
    <div id="language-switch" style="background-color: #fae3e3; padding: 15px; border-radius: 5px; border: 2px solid #cb7474;">
        <b style="font-size: 18px;">You can choose language by </b>
        <button onclick="switchLanguage('zh')">中文</button>
        <button onclick="switchLanguage('en')">English</button>
    </div>

    <script>
        function switchLanguage(lang) {
            if (lang === 'zh') {
                window.location.href = '../zh/Overview.html';
            } else if (lang === 'en') {
                window.location.href = '../en/Overview.html';
            }
        }
    </script>
    </br>
    <hr style="border: 2px solid #d3d3d3; width: 95%; margin: 10px auto;">
    </br>
    </br>


1 Visual Active Tracking
------------------------------------

VAT Task
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **Real-world Task**: A real-world visual task where the target exhibits high dynamic characteristics. The main challenge is actively controlling the camera to improve visual accuracy.
* **Existing Methods**: Existing PVT (Passive Visual Tracking) methods are based on the assumption that the target remains within a preset frame, only tracking in the video dimension.
* **VAT Task**: VAT (Visual Active Tracking) simultaneously models visual tracking and control, achieving active camera control to track dynamic targets, making it more realistic.


.. figure:: ./_static/image/VisualActiveTracking.png
   :alt: Visual Active Tracking
   :width: 600px
   :align: center

   Differences between VAT Tasks and PVT Settings

.. raw:: html

    </br>

VAT Scheme
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **Existing VAT Scheme**: Directly connect the VT model and the control model for VAT (e.g., siamask+PID)

   **Limitation 1**: The visual model requires a lot of manual labeling

   **Limitation 2**: The control model is sensitive to parameters and requires parameter fine-tuning for each different scenario

* **This Project's VAT Scheme**: Use MDP (Markov Decision Process) to model both visual and control tasks simultaneously, solving visual and control tasks with a single model

   **Advantage**: End-to-end RL is more efficient and better suited for cross-scenario tasks

.. figure:: ./_static/image/1_2stages.png
   :alt: VAT Model
   :width: 600px
   :align: center

   Single-Stage and Two-Stage VAT Scheme Illustration

2 Benchmark Presentation
------------------------------------

.. figure:: ./_static/image/statistics.png
   :alt: VAT Model
   :width: 600px
   :align: center

   Statistics and simulator component examples of the DART

Diverse and Complex Scenarios:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    * **Diverse Scenario Settings**: Featuring a total of 24 environments combining 6 scenarios and 4 weather conditions. For detailed scenarios, see: :ref:`Environment Introduction`

    * **Complex Scenario Elements**: The complexity of the real scene is constructed from 7 aspects, including scene area, building density, color richness, road complexity, terrain complexity, tree density, and tunnel density. The scene statistics are shown in Figure a above, and the difficult elements are shown in Figure b above. For detailed scenarios, see: :ref:`Environment Introduction`

Rich and Diverse Trackers and Targets:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    * **Diverse Trackers**: Pre-set ground robots and drones as Trackers, with support for autonomous model integration of ground robots.

    * **Diverse Targets**: There are 24 pre-set targets to support autonomous model access, as shown in Figure d above. For details on tracking target objects, see: :ref:`Tracked Objects`

    * **Real and Rich Behavior management**: Integrated with the traffic simulator SUMO for unified vehicle management, ensuring the authenticity and randomness of Target movements within the environment.

Flexible and Customizable Task Settings:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    * **Multi-sensor**: Equipped with 6 common visual and motion sensors, as shown in Figure c above.

    * **Customizable Task Parameters**: AThe task is highly extensible, and the additional task parameters are customized. For diverse task configurations, see: :ref:`customized parameter interface`


.. figure:: ./_static/image/24Scene_Colorful2.png
   :alt: 24 Scenes
   :width: 600px
   :align: center

   Schematic diagram of 24 open scenes
