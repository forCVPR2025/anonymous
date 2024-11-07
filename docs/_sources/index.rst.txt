.. UAV_VAT documentation master file, created by
   sphinx-quickstart on Fri Aug  9 21:33:31 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

DART documentation
=====================

.. raw:: html

    <!-- Language switch buttons -->
    <div id="language-switch">
        <button onclick="switchLanguage('zh')">中文</button>
        <button onclick="switchLanguage('en')">English</button>
    </div>

    <script>
        function switchLanguage(lang) {
            if (lang === 'zh') {
                window.location.href = 'index.html';
            } else if (lang === 'en') {
                window.location.href = 'index_en.html';
            }
        }
    </script>

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   Overview
   Installation
   Algorithm/index
   Webots_Simulator/index
