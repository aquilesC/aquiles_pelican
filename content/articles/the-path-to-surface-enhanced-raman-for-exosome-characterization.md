---
Title: The path to Surface Enhanced Raman for exosome characterization
Slug: the-path-to-surface-enhanced-raman-for-exosome-characterization/
Date: 2025-11-04
Category: Science
Tags:
  - extracellular-vesicles
  - exosomes
  - Raman
  - SERS
Summary: Extracellular Vesicles are a fascinating object of study. A paper in which they used SERS to identify samples from cancer patients through machine-learning algorithms shows great promise, but raises many questions. Is there a path forward for using label-free methods with EV's? I think so, but the tools are not there yet.
---
Using Surface Enhanced Raman Spectroscopy (SERS) to identify exosomes seems like a fantastic idea, but a very hard to realize one. The premise of label-free tools is that they shouldn’t introduce the type of biases that arise from the heavy manipulation required to label samples.

SERS relies on creating very small hotspots in which the Raman signal is greatly enhanced. The spectrum of the light that comes out of the sample, depends very strongly on some fundamental aspects of the molecules. Since each component has a unique spectral fingerprint, it is possible to use the signal to identify the composition of a sample.

The technique works very well for small molecules that can sit in the hotspot, and that have very clear spectral features. With larger objects, such as extracellular vesicles, it becomes harder (if not impossible) to get them close enough to the surface. On top of that, the recorded signal is too complex to quickly identify the components in the sample.

Signals in which identifying patterns is challenging, are an ideal target application for machine learning tools.

In [the paper by Yeonho Choi et al on Nature Comms](https://www.nature.com/articles/s41467-023-37403-1), they seem to overcome some of the challenges associated with SERS and exosomes, and move two steps further: they show they can train a deep learning model to identify EV samples from cancer patients and they can even define the tissue of origin.

However, the paper triggered me several questions.

When working with EV’s, one of the challenges is to get enough data to build good statistics. In the paper, they analyzed ‘100 signals’ which, based on the geometry of their chip and sample preparation approach, would mean they saw ~1000 particles per sample, or around 10 particles per analyzed spot.

What are the odds that at least one EV in that pool is coming from a cancerous cell?

My rough estimate puts the odds at around 1 in a million.

Even assuming the sample was enriched and the chances were in their favor, there is still the question of the size of the hotspot. SERS happens in very small gaps in between metallic structures. From that perspective, EV’s are relatively bulky objects. Even if they are sufficiently close to the hotspot, it has to be the differentiating protein the one that sits in the gap and that generates a meaningful signal.

With all these odds against, it was still possible to train an AI algorithm that can determine which samples came from cancer patients. [The reviewers comments](https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-023-37403-1/MediaObjects/41467_2023_37403_MOESM2_ESM.pdf) focused on the SERS aspects (and more superficially on the data analysis) and not too much on the exosome aspects.

Sadly, the data that was made available does not include the spectra, only the results of their trained algorithms, which allows only some partial reproducibility.

I am confident that spectroscopy and machine-learning analysis will open many doors in the coming years. Label-free methods like SERS can become crucial to get information out of complex samples. However, there is still a long road ahead to match the efforts put on [extracellular vesicles](http://notes.aquiles.me/extracellular_vesicles) research and clinical applications.

One of the more pressing challenges is throughput. A system designed for working with EV’s needs to be able to analyze at least tens of thousands or even millions of particles in order to identify the few ones that can be of interest. The “signal-to-noise” ratio will be extremely small, and the only way of improving it is by devising better sample isolation and enrichment devices and techniques.

I guess the real breakthrough will come from combining technologies either sequentially or directly in the same device.

In the meantime, fluorescence-based systems are the best candidates to get useful information out. The biggest challenge is to limit the number of false-positives. My gut-feeling tells me that the value of EV’s as diagnostic agents will arise from very small number statistics unless the sample preparation approach is radically improved. False-positives are the worst enemy for small number statistics.

I am still confident that fluorescence-based tools can build the ground knowledge that leads to the clinical application of small exosomes as biomarkers, and as therapeutic agents.

It is an exciting time for Extracellular Vesicles. Many tools are becoming available, many techniques are being adapted to work with them, which means there are many synergistic opportunities in the field.