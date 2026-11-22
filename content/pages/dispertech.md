Title: Dispertech: Co-Founding a Nanoparticle Instrumentation Spinout
Slug: dispertech
Date: 2023-06-01
Template: work-page
Category: Entrepreneurship & Instrumentation
Summary: Co-founded a university spinout building scientific instruments for exosome and lipid nanoparticle characterization, raising pre-seed and seed funding and leading product strategy.
Company: Dispertech
Role: Co-Founder
Period: Aug 2018 – Jun 2023
Location: Amsterdam, Netherlands
Cover_hue: 255
Technologies: Scientific Instrumentation, Optical Microscopy, Fluorescence, Product Management, Hardware Integration, Venture Fundraising, Python
Metrics: 1.5M€:Pre-seed & seed funding raised|2 Products:NanoCET & NanoQNT platforms|5 Years:Spinout from lab to seed stage
Highlights: Pre-Seed & Seed Fundraising::Secured public funding through the NWO Take-Off program alongside private VC pre-seed and seed financing::|NanoCET Launch::Designed, built, and led market introduction of a hollow-fiber optical instrument measuring nanoparticle size and refractive index::|Strategic Pivot to NanoQNT::Partnered with Erasmus MC and built an OpenSPIM light-sheet microscope readout after customer discovery showed clearer demand for vesicle concentration::

## From Research to Product

Dispertech was born to create products around scientific results in the field of nanoparticle characterization.

We translated research that allowed measuring nanoparticle sizes with high accuracy, and later developed an in-house system for exosome and lipid nanoparticle concentration measurements. Along the way, I led product management, system integration, IT, customer relations, and fundraising through the NWO Take-Off program and private investors.

## NanoCET

The first product, the **nanoCET**, is a compact instrument that measures the size and refractive index of nanoparticles in a liquid. The technology was developed around hollow optical fibers that guide light and contain the fluid. Scattered light is captured by a microscope placed directly below the fiber.

### Technical & Commercial Challenges

- **Single-use fibers:** Liquid entered by capillary forces, and traces of previous samples clogged the fiber. To overcome this, we mounted the fiber on a disposable cartridge fabricated by laser-cutting black acrylic, which introduced a new alignment constraint.
- **Automated laser coupling:** Coupling a laser into a single-mode fiber mounted on a disposable cartridge had to work reliably without manual tweaking. We found that as soon as any laser light coupled into the fiber (even the cladding mode), a second inspection microscope looking at the fiber tip clearly showed the core lighting up. Using a scanning mirror and a linear stage for the lens (3 degrees of freedom), we automated coupling to reach reproducible alignment in seconds.
- **Real-time data reduction:** Before incorporating the company, the project began by pushing the limits of nanoparticle tracking analysis through real-time data reduction—storing particle locations instead of full frames—in an open-source tool nicknamed [PyNTA](https://github.com/aquilesC/pynta). The NanoCET produced 1-D *kymographs*, allowing high compression and framerates up to 1 kHz with strong signal-to-noise and localization accuracy.
- **Business-related hurdles:** We positioned nanoCET as an improvement over Nanoparticle Tracking Analysis (NTA), focusing heavily on size rather than our true differentiator: refractive index measurements capable of distinguishing loading efficiencies. Switching costs for scientists were high, and dependency on small-volume specialty fibers from Heraeus kept cost-per-measurement above what customers would pay.

## NanoQNT

I learned the hard way that doing something *better* than an existing standard is rarely enough to justify the cost of switching. Doing something genuinely *new* shifts the conversation from switching cost to opportunity.

Spending time in the Extracellular Vesicles community clarified a pressing unanswered question: measuring the concentration of specific vesicles in a fluid. Through a collaboration with **Erasmus MC** in Rotterdam—who had developed a protocol to immobilize fluorescently labeled particles in a hydrogel—we saw a clear match. They needed a high-throughput optical readout; we needed a compelling commercial anchor.

I built an OpenSPIM light-sheet microscope prototype from scratch. Despite spec mismatches and mechanical drawing errors in early open-hardware parts, the team pulled through and acquired our first dataset within a couple of months. The difference in customer conversations was immediate: researchers understood the value within minutes.

## Closing a Chapter

Spinning out a hardware company is demanding, and Covid arrived right as our first product was ready for conferences, customer visits, and commercial hiring. By the time we validated the NanoQNT path and secured a professional seed round to expand the team, I recognized that I had run out of energy to reinvent myself for the next phase—and made the decision to step away so the team could move forward cleanly.
