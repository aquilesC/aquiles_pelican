Title: Dispertech
Slug: dispertech
Date: 2025-01-01
Template: work-page
Category: Scipreneurship
Summary: Spinning out a hardware company from the university. Single-particle detection for biomarker identification
Company: Dispertech
Role: Co-Founder
Technologies: Microscopy, Instrumentation, Fluorescence
Hero_image: images/aquiles_carattino_bw.jpeg
Metrics: 1.5M€:Funding raised|2:Product lines|1:Engaged team
Highlights: Feature Launch::Launched a major feature that increased user engagement by 40%::https://example.com|Team Leadership::Led a team of 5 developers to deliver on time and under budget::|Technical Innovation::Implemented a novel caching strategy that reduced server costs by 30%::
Project_url: https://www.dispertech.com


# From research to product
Dispertech was born to create products around scientific results in the field of nanoparticle characterization. 

We translated research that allowed to measure nanoparticle sizes with unprecedented accuracy, and later developed an in-house system for concentration measurements. 

## NanoCET

The first product, the **nanoCET**, is a compact instrument that measures the size and refractive index of nano particles in a liquid. The technology was developed around hollow optical fibers that would guide light and contain the fluid. Scattered light is captured by a microscope placed right below the fiber. 

### Challenges
- `Fibers could be used only once`. Liquid would enter by capillary forces, and any traces of the previous samples would clog it. 

To overcome this challenge, we mounted the fiber on a cartridge, fabricated by laser cutting black acrylic, but this created new challenges

- `Laser coupling` to a single-mode fiber that is mounted on a disposable cartridge. 

We found out that, as soon as there was a part of the laser light coupled to the fiber (even the cladding mode) we could clearly see the core lighting up by placing a second inspection microscope looking at the fiber tip. 

We automated the laser coupling by using a scanning mirror and a linear stage for the lens, giving 3 degrees of freedom. In a few seconds we could achieve optimal and reproducible coupling. 

- `Data analysis in real time` to lower the amount of information that had to be stored. 

Before we became a company, the project started with pushing the limits of nanoparticle tracking analysis by performing real-time data reduction. Instead of storing the entire frame, we could store only the locations of the particles. It was nicknamed [PyNTA](https://github.com/aquilesC/pynta). And was meant to work on 2D images with sparse particles. 

The NanoCET, however, had the advantage of producing 1-D data, also called *kymographs*. Datasets could be compressed, and in turn the framerate could easily increase to 1kHz yielding an exquisite balance between signal-to-noise and localization accuracy. 

- The largest challenge was `business-ralted`. 

We understood the nanoCET as a continuation what Nanoparticle Tracking Analysis (NTA) could do. We positioned ourselves in that space. However, we couldn't find enough traction. Even if NTA was not satisfying the requirements of scientists, switching has an immense cost, and we couldn't immediately prove it was worth it. 

We focused too much on size, while the real benefit was measuring refractive index and proving we could distinguish loading efficiencies. 

For the fibers, we were dependent on Heraeus, a massive German company. However, our purchasing volumes were too small to be able to secure interest and better pricing. It lead to a high cost-per-measurement situation, which was not affordable by our customers. 

So we knew we had to move on to new challenges. 

## NanoQNT 
I learned, perhaps the hard way, that trying to do something *better* than what is available is not sufficient to convince people the value you deliver warrants the cost of switching. 

On the other hand, if you do something *new*, then there's no switching, but just opportunity cost. 

I spent a lot of time exploring the world of Extracellular Vesicles. I believed the sweetspot for the nanoCET lied in there. And through that exploration came to understand what were the questions people asked and had to clear answers for. One of them was how to measure the concentration of vesicles in a fluid. 

I came across a project from **Erasmus MC**, a prestigious medical university in Rotterdam. They had developed a protocol to immobilize particles in a hydrogel and fluorescently label them. They were missing a readout system that would generate enough statistical significance. 

For me it was clear: a light-sheet microscope would address their problems, their protocol would address our problems, we should work together. 

I set to build the OpenSPIM. One of the first successful open-hardware projects. It was not a walk in the park as I initially expected. Some of the parts that had to be built had wrong specs or wrong tech drawings. Choices of optics and distances did not match. But the team managed to pull through and the first data was acquired within a couple of months. 

The more interesting thing was that people would simply get it. It didn't take a long time to explain what we do, how that would help them, and why it would be worth talking to us. 
# Closing a Chapter: Leaving Dispertech

The entire process of creating a spinout can be draining. On top of that, Covid hit right when the first product was ready, when we were supposed to go to conferences, visit customers, and strengthen the commercial side of the team. 

Covid was too long, and we missed what was happening in the community. It was clear the nanoCET would not find product-market fit without a massive re-engineering that we couldn't afford. 

The nanoQNT would be the best path forward, and it coincided to securing a professional seed-round for the company. 

However, I just hadn't in me to keep going. I stopped being an asset for the team and couldn't reinvent myself. 

