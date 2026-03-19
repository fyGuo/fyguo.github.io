#!/usr/bin/env python3
"""
Build HTML files from config.json
Run this after editing config.json to regenerate your website
"""

import json
from pathlib import Path

def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

def generate_index(config):
    publications_html = ""
    for pub in config['publications'][:3]:  # Show first 3 recent
        journal_link = f'[<a href="{pub["journal_url"]}" target="_blank">Journal</a>]' if pub['journal_url'] else ""
        publications_html += f'''
                    <div class="pub-item">
                        <p class="pub-title">
                            <strong>{pub['title']}</strong>
                        </p>
                        <p class="pub-authors">
                            {pub['authors']}
                        </p>
                        <p class="pub-meta">
                            <em>{pub['journal']}</em>, Vol. {pub['volume']}, No. {pub.get('issue', 'N/A')}, pp. {pub.get('pages', 'N/A')}, {pub['year']}.
                            {journal_link}
                        </p>
                    </div>'''

    news_html = ""
    for item in config['news']:
        news_html += f'''
                <div class="news-item">
                    <span class="news-date">{item['date']}</span>
                    <p>{item['content']}</p>
                </div>'''

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{config['name']} - {config['institution']}</title>
    <meta name="description" content="{config['about']}" />
    <meta name="keywords" content="{config['name']}, epidemiology, biostatistics, public health, research" />
    <link rel="canonical" href="https://fyguo.github.io/" />
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <header class="header">
            <h1 class="name">{config['name']}</h1>
            <nav class="nav">
                <a href="index.html" class="nav-link active">Home</a>
                <a href="research.html" class="nav-link">Research</a>
                <a href="teaching.html" class="nav-link">Teaching</a>
                <a href="{config.get('cv_file', 'CV.pdf')}" class="nav-link" target="_blank" rel="noopener noreferrer">CV</a>
            </nav>
        </header>

        <script type="application/ld+json">
        {{
            "@context": "https://schema.org",
            "@type": "Person",
            "name": "{config['name']}",
            "url": "https://fyguo.github.io/",
            "sameAs": [
                "{config['google_scholar']}",
                "{config['orcid']}"
            ]
        }}
        </script>

        <main class="content">
            <section class="about">
                <div class="about-image">
                    <img src="profile.jpg" alt="{config['name']}" class="profile-img">
                </div>
                <div class="about-text">
                    <h2>About</h2>
                    <p>{config['about']}</p>
                    <p>{config['bio2']}</p>

                    <div class="contact-info">
                        <h3>Contact</h3>
                        <p><strong>Email:</strong> <a href="mailto:{config['email']}">{config['email']}</a></p>
                        <p><strong>Phone:</strong> {config['phone']}</p>
                        <p><strong>Google Scholar:</strong> <a href="{config['google_scholar']}" target="_blank">Profile</a></p>
                        <p><strong>ORCID:</strong> <a href="{config['orcid']}" target="_blank">0000-0001-8437-8702</a></p>
                    </div>
                </div>
            </section>

            <section class="news">
                <h2>Latest News</h2>
                <div class="news-list">{news_html}
                </div>
            </section>

            <section class="publications">
                <h2>Recent Publications</h2>
                <div class="pub-list">{publications_html}
                </div>
                <p class="more-link"><a href="research.html">View all publications →</a></p>
            </section>
        </main>

        <footer class="footer">
            <p>&copy; 2024 {config['name']}. All rights reserved.</p>
        </footer>
    </div>
</body>
</html>'''
    return html

def generate_research(config):
    pubs_by_year = {}
    for pub in config['publications']:
        year = pub['year']
        if year not in pubs_by_year:
            pubs_by_year[year] = []
        pubs_by_year[year].append(pub)

    publications_html = ""
    for year in sorted(pubs_by_year.keys(), reverse=True):
        publications_html += f'<h3 style="margin-top: 30px; margin-bottom: 15px; font-size: 1.1em; color: #333;">{year}</h3>\n'
        publications_html += '<div class="pub-list">\n'
        for pub in pubs_by_year[year]:
            journal_link = f'[<a href="{pub["journal_url"]}" target="_blank">Journal</a>]' if pub['journal_url'] else ""
            publications_html += f'''                    <div class="pub-item">
                        <p class="pub-title">
                            <strong>{pub['title']}</strong>
                        </p>
                        <p class="pub-authors">
                            {pub['authors']}
                        </p>
                        <p class="pub-meta">
                            <em>{pub['journal']}</em>, Vol. {pub['volume']}, {pub.get('pages', '')}, {year}.
                            {journal_link}
                        </p>
                    </div>\n'''
        publications_html += '                </div>\n'

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Research - {config['name']}</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <header class="header">
            <h1 class="name">{config['name']}</h1>
            <nav class="nav">
                <a href="index.html" class="nav-link">Home</a>
                <a href="research.html" class="nav-link active">Research</a>
                <a href="teaching.html" class="nav-link">Teaching</a>
                <a href="#cv" class="nav-link">CV</a>
            </nav>
        </header>

        <main class="content">
            <section class="publications">
                <h2>Research Interests</h2>
                <p style="margin-bottom: 30px;">
                    {config['research_interests']}
                </p>

                <h2 style="margin-top: 40px;">Publications</h2>
                {publications_html}
            </section>
        </main>

        <footer class="footer">
            <p>&copy; 2024 {config['name']}. All rights reserved.</p>
        </footer>
    </div>
</body>
</html>'''
    return html

def generate_teaching(config):
    teaching_html = ""
    for inst in config['teaching']:
        teaching_html += f'<h3 style="margin-top: 30px; margin-bottom: 20px; font-size: 1.15em; color: #1a1a1a;">{inst["institution"]} (Teaching Assistant)</h3>\n'
        for semester_block in inst['courses']:
            teaching_html += f'''                <div style="margin-bottom: 25px; padding-left: 15px; border-left: 3px solid #e0e0e0;">
                    <p style="font-weight: 600; color: #333; margin-bottom: 10px;">{semester_block['semester']}</p>
                    <ul style="list-style: none; color: #555;">
'''
            for course in semester_block['courses_list']:
                teaching_html += f'                        <li>• {course}</li>\n'
            teaching_html += '''                    </ul>
                </div>
'''

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Teaching - {config['name']}</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <header class="header">
            <h1 class="name">{config['name']}</h1>
            <nav class="nav">
                <a href="index.html" class="nav-link">Home</a>
                <a href="research.html" class="nav-link">Research</a>
                <a href="teaching.html" class="nav-link active">Teaching</a>
                <a href="#cv" class="nav-link">CV</a>
            </nav>
        </header>

        <main class="content">
            <section class="publications">
                <h2>Teaching Experience</h2>
                <p style="margin-bottom: 30px; color: #666; font-weight: 500;">
                    <strong>Award:</strong> Distinction in teaching during the academic year 2023-2024, Harvard Biostatistics Department
                </p>
                {teaching_html}
            </section>
        </main>

        <footer class="footer">
            <p>&copy; 2024 {config['name']}. All rights reserved.</p>
        </footer>
    </div>
</body>
</html>'''
    return html

def main():
    config = load_config()
    
    # Generate HTML files
    with open('index.html', 'w') as f:
        f.write(generate_index(config))
    
    with open('research.html', 'w') as f:
        f.write(generate_research(config))
    
    with open('teaching.html', 'w') as f:
        f.write(generate_teaching(config))
    
    print("✓ Generated index.html")
    print("✓ Generated research.html")
    print("✓ Generated teaching.html")
    print("\nYour website is ready!")

if __name__ == '__main__':
    main()
