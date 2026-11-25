#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Aquiles Carattino'
SITENAME = 'Aquiles Carattino'
SITEURL = 'https://www.aquiles.me'
CANONICAL_SITEURL = 'https://www.aquiles.me'

PATH = 'content'

TIMEZONE = 'Europe/Amsterdam'

DEFAULT_LANG = 'en'

# Feed settings
FEED_ALL_ATOM = None
FEED_ALL_RSS = 'feed.rss'
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Theme settings
THEME = 'themes/aquiles_theme'

# Template settings
DIRECT_TEMPLATES = ['index', 'archives', '404', 'sitemap', 'llms']
PAGINATED_TEMPLATES = {}
DEFAULT_PAGINATION = False
ARCHIVES_SAVE_AS = 'articles/index.html'
ARCHIVES_URL = 'articles/'
AUTHOR_SAVE_AS = ''
AUTHORS_SAVE_AS = ''
SITEMAP_SAVE_AS = 'sitemap.xml'
LLMS_SAVE_AS = 'llms.txt'

# URL settings
ARTICLE_URL = '{slug}/'
ARTICLE_SAVE_AS = '{slug}/index.html'
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'
TAG_URL = 'tag/{slug}/'
TAG_SAVE_AS = 'tag/{slug}/index.html'
CATEGORY_URL = 'category/{slug}/'
CATEGORY_SAVE_AS = 'category/{slug}/index.html'

# Static files
# Images in content/images/ will be copied to output/images/
# Reference them in markdown as: ![alt text](/images/filename.png)
STATIC_PATHS = ['images', 'extra']
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/favicon.ico': {'path': 'favicon.ico'},
    'extra/favicon.svg': {'path': 'favicon.svg'},
    'extra/apple-touch-icon.png': {'path': 'apple-touch-icon.png'},
    'extra/_headers': {'path': '_headers'},
    'extra/_redirects': {'path': '_redirects'},
}

# Exclude templates folder from being parsed as articles/pages
ARTICLE_EXCLUDES = ['templates']
PAGE_EXCLUDES = ['templates']

# Plugin settings
# pelican-yaml-metadata plugin handles YAML frontmatter (--- delimited)
PLUGINS = ['pelican.plugins.yaml_metadata']

# Markdown extensions
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
        'markdown.extensions.smarty': {},
    },
    'output_format': 'html5',
}

# Metadata
DEFAULT_METADATA = {
    'status': 'published',
}

# Date format
DEFAULT_DATE_FORMAT = '%B %d, %Y'

# SEO & Entity Metadata (Synced with LinkedIn source of truth)
SITESUBTITLE = 'Deep-Tech Product & Engineering Leader | Quantum Computing & Scientific Instrumentation'
SITE_TITLE = 'Aquiles Carattino'
SITE_DESCRIPTION = (
    'Aquiles Carattino leads Product Development at Orange Quantum Systems in Delft. '
    '10+ years taking quantum and scientific instrumentation from lab to market.'
)
DEFAULT_OG_IMAGE = 'images/og/default.png'
TWITTER_USERNAME = None
GITHUB_USERNAME = 'aquilesC'
LINKEDIN_USERNAME = 'aquic'
DIGITAL_GARDEN_URL = 'https://notes.aquiles.me/digital_garden'
PYTHON_FOR_THE_LAB_URL = 'https://www.pythonforthelab.com'
ORCID_URL = 'https://orcid.org/0000-0002-1781-7565'
DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_TAGS_ON_MENU = False

PERSON_PROFILE = {
    'name': 'Aquiles Carattino',
    'alternate_name': 'Dr. Aquiles Carattino',
    'job_title': 'Team Lead, Product Development',
    'headline': 'Leading Product Development @ OrangeQS (Quantum Chip Testing) | Deep-Tech Lab-to-Market | Ex-Founder & Author',
    'employer': 'Orange Quantum Systems',
    'employer_short': 'OrangeQS',
    'employer_url': 'https://orangeqs.com',
    'location': 'Delft, South Holland, Netherlands',
    'region': 'The Randstad, Netherlands',
    'same_as': [
        'https://www.linkedin.com/in/aquic/',
        'https://github.com/aquilesC',
        'https://www.pythonforthelab.com',
        'https://notes.aquiles.me/digital_garden',
        'https://orcid.org/0000-0002-1781-7565',
    ],
    'knows_about': [
        'Quantum Computing',
        'Quantum Processing Unit (QPU) Testing and Characterization',
        'Deep-Tech Product Development',
        'Engineering Management',
        'Product Leadership',
        'Scientific Instrumentation',
        'Lab-to-Market Commercialization',
        'Systems Engineering',
        'Semiconductor Equipment Calibration',
        'Nanoparticle Characterization',
        'Jobs to be Done (JTBD)',
        'Python for Scientific Instrumentation',
    ],
    'languages': [
        {'name': 'English', 'level': 'Full professional proficiency'},
        {'name': 'Spanish', 'level': 'Native or bilingual proficiency'},
        {'name': 'Portuguese', 'level': 'Full professional proficiency'},
        {'name': 'Italian', 'level': 'Professional working proficiency'},
        {'name': 'French', 'level': 'Limited working proficiency'},
    ],
}

# Career Highlights for Homepage (executive snapshot)
CAREER_HIGHLIGHTS = [
    {
        'company': 'Orange Quantum Systems',
        'role': 'Team Lead, Product Development',
        'period': 'Jun 2026 – Present',
        'location': 'Delft, Netherlands',
        'summary': (
            'Leading a 14-person team of software engineers, instrumentation specialists, quantum test engineers, '
            'and systems engineers building automated testing and characterization systems for quantum processing units (QPUs).'
        ),
        'url': '/orange-quantum-systems/',
        'cta': 'Read Case Study',
    },
    {
        'company': 'VSParticle',
        'role': 'Product Manager & Business Developer',
        'period': 'Jan 2025 – Jun 2026',
        'location': 'Delft, Netherlands',
        'summary': (
            'Built customer-centered product roadmaps for the P1 nanoprinter and G1 generator using Jobs Theory (JTBD), '
            'then led semiconductor business development for Spark Ablation nanoparticle calibration.'
        ),
        'url': '/vsparticle/',
        'cta': 'Read Case Study',
    },
    {
        'company': 'Dispertech',
        'role': 'Co-Founder',
        'period': 'Aug 2018 – Jun 2023',
        'location': 'Amsterdam, Netherlands',
        'summary': (
            'Co-founded a university spinout building nanoparticle and exosome characterization instruments. '
            'Raised pre-seed (NWO Take-Off + VC) and seed funding, launched NanoCET, and led the pivot to NanoQNT.'
        ),
        'url': '/dispertech/',
        'cta': 'Read Case Study',
    },
    {
        'company': 'Python for the Lab & Leiden PhD',
        'role': 'Author, Instructor & Physicist',
        'period': '2012 – 2025',
        'location': 'Netherlands & Europe',
        'summary': (
            'Authored the book Python for the Lab, trained engineering and research teams across Europe, '
            'and completed a Physics PhD at Leiden University in gold nanorod photoluminescence and nano-thermometry.'
        ),
        'url': '/python-for-the-lab/',
        'cta': 'Explore Book & Research',
    },
]

# Full Chronological Experience Timeline (synced 1:1 with LinkedIn)
EXPERIENCE_TIMELINE = [
    {
        'role': 'Team Lead, Product Development',
        'company': 'Orange Quantum Systems (OrangeQS)',
        'period': 'Jun 2026 – Present',
        'location': 'Delft, Netherlands · On-site',
        'summary': (
            'Lead the 14-person Product Development team building, deploying, and operating automated screening, '
            'testing, and characterization systems for quantum processing units (QPUs). Established clear team '
            'responsibilities for faster learning cycles with minimal downtime, broke down silos between software '
            'and hardware engineering, and built integration processes with R&D and commercial teams.'
        ),
        'skills': ['Engineering Management', 'Quantum Technology', 'Systems Engineering', 'Team Leadership'],
        'case_study_url': '/orange-quantum-systems/',
    },
    {
        'role': 'Business Developer',
        'company': 'VSParticle',
        'period': 'Jan 2026 – Jun 2026',
        'location': 'Delft, Netherlands · On-site',
        'summary': (
            'Led commercial exploration introducing Spark Ablation single-nanoparticle generation for semiconductor '
            'process development and equipment calibration, mapping customer pain points around yield, accuracy, and reliability.'
        ),
        'skills': ['Business Development', 'Semiconductor', 'Market Analysis'],
        'case_study_url': '/vsparticle/',
    },
    {
        'role': 'Product Manager',
        'company': 'VSParticle',
        'period': 'Jan 2025 – Jan 2026',
        'location': 'Delft, Netherlands · On-site',
        'summary': (
            'Established customer-centered product innovation through customer interviews, citation/patent network analysis, '
            'and Jobs Theory (JTBD). Owned roadmaps and value propositions for the P1 nanoprinter and G1 generator across '
            'R&D, marketing, and sales.'
        ),
        'skills': ['Product Management', 'Jobs to be Done', 'Product Roadmapping', 'Deep Tech'],
        'case_study_url': '/vsparticle/',
    },
    {
        'role': 'Instrumentation Software Specialist & Deep-Tech Product Advisor',
        'company': 'Python for the Lab & Scipreneurs',
        'period': 'Jul 2023 – Jan 2025',
        'location': 'Paris, France',
        'summary': (
            'Advised hardware and scientific instrumentation companies on software architecture, technical hiring, code reviews, '
            'team training, MVP scoping, and multi-year product strategy for analytical instruments, automation, and sensing.'
        ),
        'skills': ['Python', 'Instrumentation Software', 'Product Strategy', 'Technical Hiring'],
        'case_study_url': '/python-for-the-lab/',
    },
    {
        'role': 'Co-Founder',
        'company': 'Dispertech',
        'period': 'Aug 2018 – Jun 2023',
        'location': 'Amsterdam, Netherlands · On-site',
        'summary': (
            'Co-founded a scientific instrumentation startup for exosome and lipid nanoparticle characterization. '
            'Raised pre-seed (NWO Take-Off and VC) and seed funding, built and launched the NanoCET, pivoted to the '
            'NanoQNT light-sheet platform, and led product management, IT, and customer relations.'
        ),
        'skills': ['Startup Leadership', 'Product Management', 'Hardware Integration', 'Fundraising'],
        'case_study_url': '/dispertech/',
    },
    {
        'role': 'Workshop Instructor & Author',
        'company': 'Python for the Lab',
        'period': 'Jan 2017 – Feb 2020',
        'location': 'Amsterdam, Netherlands & Europe',
        'summary': (
            'Created and delivered 3-day instrumentation software workshops at top European universities and startups, '
            'published the book Python for the Lab, and grew pythonforthelab.com to top Google rankings on core queries.'
        ),
        'skills': ['Python', 'Scientific Instrumentation', 'Technical Writing', 'Training'],
        'case_study_url': '/python-for-the-lab/',
    },
    {
        'role': 'Scientific Software Developer',
        'company': 'Uetke',
        'period': 'Jan 2017 – Dec 2018',
        'location': 'Amsterdam, Netherlands',
        'summary': (
            'Built modular MVC-based instrument control, data acquisition, and metadata storage software for research labs, '
            'with production programs running across multiple laboratories for over seven years.'
        ),
        'skills': ['MVC Architecture', 'Data Acquisition', 'Python'],
        'case_study_url': None,
    },
    {
        'role': 'Doctoral Researcher (PhD, Physics)',
        'company': 'Leiden University',
        'period': 'Sep 2012 – Dec 2016',
        'location': 'Leiden, Netherlands · On-site',
        'summary': (
            'Experimental physics PhD in the Single-Molecule Optics group studying gold nanorod photoluminescence. '
            'Automated optical setups to study oxidative etching, developed anti-Stokes background-free imaging, and '
            'pioneered calibration-free optical nano-thermometry.'
        ),
        'skills': ['Optics', 'Microscopy', 'Nanophotonics', 'Python'],
        'case_study_url': '/phd/',
    },
    {
        'role': 'Research Assistant',
        'company': 'Tenaris',
        'period': 'Jun 2011 – Jul 2012',
        'location': 'Campana, Buenos Aires, Argentina',
        'summary': (
            'Modeled radiation and electromagnetic induction heating in industrial steel-tube reheat furnaces. '
            'Modernized Fortran 77 simulation code to Fortran 90, automated Python/Matlab analysis pipelines, and ran COMSOL models.'
        ),
        'skills': ['R&D', 'Numerical Modeling', 'Python', 'Fortran'],
        'case_study_url': None,
    },
]

# Education (synced with LinkedIn)
EDUCATION_LIST = [
    {
        'institution': 'Leiden University',
        'degree': 'Doctor of Philosophy (PhD), Physics',
        'period': '2012 – 2016',
        'details': 'Thesis: Gold nanorod photoluminescence: applications to imaging and temperature sensing. Active in LEO (Leids Promovendi Overleg).',
        'url': '/phd/',
    },
    {
        'institution': 'University of Buenos Aires (UBA)',
        'degree': 'Licenciatura en Ciencias Físicas (Physics)',
        'period': '2004 – 2010',
        'details': 'Five-year combined BSc/MSc equivalent degree in experimental and theoretical physics.',
        'url': None,
    },
    {
        'institution': 'Universidade Estadual de Campinas (UNICAMP)',
        'degree': 'Exchange Student, Physics',
        'period': '2008',
        'details': 'International academic exchange supported by the AUGM scholarship.',
        'url': None,
    },
]

# Selected Publications & Book (synced with LinkedIn)
PUBLICATIONS_LIST = [
    {
        'title': 'Python for the Lab',
        'venue': 'Self-published Book',
        'year': '2020',
        'date_iso': '2020-10-11',
        'type': 'Book',
        'description': 'Hands-on guide to controlling scientific instruments with Python, covering environment setup, drivers, Model-View-Controller architecture, and reproducible experiments.',
        'url': 'https://www.pythonforthelab.com/books/',
    },
    {
        'title': 'Challenges of implementing nano-specific safety and safe-by-design principles in academia',
        'venue': 'NanoImpact',
        'year': '2020',
        'date_iso': '2020-07-01',
        'type': 'ScholarlyArticle',
        'description': 'Peer-reviewed analysis of practical barriers to implementing safe-by-design nanomaterials workflows in academic research.',
        'url': 'https://www.sciencedirect.com/science/article/pii/S2452074820300379',
    },
    {
        'title': 'Gold Nanoparticles as Absolute Nanothermometers',
        'venue': 'Nano Letters',
        'year': '2017',
        'date_iso': '2017-12-22',
        'type': 'ScholarlyArticle',
        'description': 'Calibration-free optical nano-thermometry based on anti-Stokes photoluminescence of single gold nanorods.',
        'url': 'https://pubs.acs.org/doi/abs/10.1021/acs.nanolett.7b04145',
    },
    {
        'title': 'Background Suppression in Imaging Gold Nanorods through Detection of Anti-Stokes Emission',
        'venue': 'Biophysical Journal',
        'year': '2016',
        'date_iso': '2016-12-06',
        'type': 'ScholarlyArticle',
        'description': 'High-contrast, background-free optical imaging strategy for metallic nanoparticles in complex biological environments.',
        'url': 'https://www.sciencedirect.com/science/article/pii/S0006349516309948',
    },
    {
        'title': 'In situ tuning of gold nanorod plasmon through oxidative cyanide etching',
        'venue': 'Physical Chemistry Chemical Physics (PCCP)',
        'year': '2016',
        'date_iso': '2016-05-19',
        'type': 'ScholarlyArticle',
        'description': 'Automated single-particle spectroscopy tracking real-time shape and plasmon resonance changes during chemical etching.',
        'url': 'https://pubs.rsc.org/en/content/articlehtml/2016/cp/c6cp01679k',
    },
    {
        'title': 'Influence of the Glass Transition on Rotational Dynamics of Dyes in Thin Polymer Films: Single-Molecule and Ensemble Experiments',
        'venue': 'Journal of Physical Chemistry A',
        'year': '2014',
        'date_iso': '2014-05-29',
        'type': 'ScholarlyArticle',
        'description': 'Single-molecule and ensemble fluorescence measurements probing nanoscale polymer dynamics near the glass transition.',
        'url': 'https://pubs.acs.org/doi/abs/10.1021/jp500272y',
    },
]

# Theme helpers
import datetime as _dt
from pathlib import Path as _Path

CURRENT_YEAR = _dt.date.today().year
# Full ISO 8601 datetime with timezone: Google rejects a bare date for
# structured-data dateModified. Also valid for sitemap <lastmod>.
BUILD_DATE = _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat()

import hashlib as _hashlib
import time as _time

def _get_asset_version(rel_path):
    p = _Path(__file__).parent / rel_path
    if p.exists():
        return _hashlib.md5(p.read_bytes()).hexdigest()[:10]
    return str(int(_time.time()))

CSS_VERSION = _get_asset_version('themes/aquiles_theme/static/css/style.css')
JS_VERSION = _get_asset_version('themes/aquiles_theme/static/js/particles.js')

# Slugs that have a generated Open Graph image (see generate_og_images.py)
OG_IMAGES = {p.stem for p in (_Path(__file__).parent / 'content' / 'images' / 'og').glob('*.png')}
# Hue (0-360, OKLCH) used for the generated card covers of each category
CATEGORY_HUES = {
    'personal': 45,
    'science': 175,
    'science-commercialization': 250,
    'deep-tech-strategy': 285,
    'entrepreneurship': 20,
}

# Low-key Speaking & Advisory offerings (footer/contact only; no full-time consulting retainers)
ADVISORY_OFFERINGS = [
    {
        'title': 'Guest Talks & Workshops',
        'summary': (
            'Sessions for universities, research institutes, incubators, and deep-tech conferences on taking '
            'scientific instrumentation from lab prototypes to commercial products and building software-literate hardware teams.'
        ),
        'details': 'Speaking & University Workshops',
        'link_text': 'Workshop Overview',
        'link_url': '/services/workshop/'
    },
    {
        'title': 'Founder & Product Sparring',
        'summary': (
            'Occasional 1-hour conversations with technical founders, postdocs, and product leaders working through '
            'specific deep-tech roadmap, customer discovery, or lab-to-market decisions.'
        ),
        'details': 'Selective 1:1 Conversation',
        'link_text': 'Learn More',
        'link_url': '/services/golden-hour/'
    },
]

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
