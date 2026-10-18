Title: PhD Research: Optics & Single-Molecule Biophysics
Slug: phd
Date: 2017-01-01
Template: work-page
Category: Academia & Research
Summary: Experimental physics PhD at Leiden University focused on building novel optical setups and instrumentation to investigate single molecules and nanoscale physical phenomena.
Company: Leiden University
Role: PhD Researcher
Technologies: Optics, Single-Molecule Spectroscopy, Instrumentation, Python, Nanophotonics, Lasers
Hero_image: images/aquiles_carattino_bw.jpeg
Metrics: 4 Years:Doctoral research|Multiple:Peer-reviewed papers|100%:Custom instrumentation
Highlights: Optical Setup Development::Designed and built custom microscopy setups combining single-molecule sensitivity and microsecond time resolution::|Python for Setup Control::Authored modular Python software to synchronize lasers, detectors, and piezo stages in real time::|Thesis Defense::Completed and defended doctoral dissertation at Huygens-Kamerlingh Onnes Laboratory::
Project_url: https://notes.aquiles.me/my_phd/

# The Research & The Big Picture

<!--
TODO: Introduce the scientific context of your doctoral research at Leiden University (Huygens-Kamerlingh Onnes Laboratory / Michel Orrit's group).
- What was the core scientific question or phenomenon you investigated?
- Why was existing technology or commercially available equipment insufficient?
-->

I pursued my PhD in experimental physics in the Single-Molecule Optics group at Leiden University. My research centered around developing novel optical instrumentation and measurement techniques to observe physical and photophysical phenomena at the single-molecule scale.

## Building the Experimental Setups

<!--
TODO: Detail the hardware, optical design, and engineering challenges you tackled.
- Optical layout: lasers, confocal/widefield configurations, detectors (APDs, EMCCDs), cryogenics or fluidics.
- Alignment, laser coupling, mechanical stability, noise reduction.
-->

A major part of my PhD was learning how to *make* things from scratch. Rather than relying on turnkey systems, we built custom setups on optical tables:

- **Laser alignment and coupling:** Achieving stability and precise beam control.
- **Detector integration:** Coordinating sensitive avalanche photodiodes (APDs) and spectrometers.
- **Sub-nanometer positioning:** Controlling piezo scanners and sample holders with high reproducibility.

## Software as the Catalyst: Controlling the Lab with Python

<!--
TODO: Explain how the need for lab automation led you to Python.
- Moving away from slow/rigid legacy tools (LabVIEW, vendor software).
- Building modular drivers and acquisition software.
- How this sparked the foundation for Python for the Lab and future projects like PyNTA / PyMoDAQ.
-->

One of the earliest and most impactful bottlenecks I faced was setup control. Commercial software was either too rigid, proprietary, or closed off. I turned to Python to build flexible, modular software that synchronized hardware in real time:

- Coordinating multiple instruments (stages, lasers, counters) through clear interfaces.
- Real-time data streaming, visualization, and reduction.
- Laying the groundwork for software patterns that would later inspire [Python for the Lab]({filename}python-for-the-lab.md) and open-source packages.

## Key Scientific Discoveries & Contributions

<!--
TODO: Summarize your key papers, findings, and thesis highlights.
- Key findings or publications.
- Novel observations or methodologies developed.
-->

Through these custom-built setups, we were able to observe:

- Dynamics and photophysics of individual emitters.
- High-precision localization and tracking with microsecond-level temporal resolution.
- Novel insights into nano-optics and light-matter interactions at nanoscale dimensions.

## Lessons from the Lab: Transitioning to Entrepreneurship

<!--
TODO: Share personal reflections on how your PhD shaped your career, problem-solving mindset, and the transition into founding Dispertech.
-->

Doing a PhD taught me how to embrace ambiguity, troubleshoot problems methodically from first principles, and push beyond existing limitations. More importantly, it gave me the confidence that any instrument can be broken down, understood, and rebuilt. That mindset ultimately paved the way for my transition from academic research to deep-tech entrepreneurship and founding [Dispertech]({filename}dispertech.md).
