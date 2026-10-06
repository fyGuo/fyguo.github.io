#!/usr/bin/env python3
"""
Build HTML files from config.json
Run this after editing config.json to regenerate your website
"""

import json
from pathlib import Path

# Inline brand logos shown before the Google Scholar and ORCID links
SCHOLAR_ICON = '<svg class="link-icon" viewBox="0 0 24 24" aria-hidden="true"><path fill="#4285F4" d="M5.242 13.769L0 9.5 12 0l12 9.5-5.242 4.269C17.548 11.249 14.978 9.5 12 9.5c-2.977 0-5.548 1.748-6.758 4.269zM12 10a7 7 0 1 0 0 14 7 7 0 0 0 0-14z"/></svg>'
ORCID_ICON = '<svg class="link-icon" viewBox="0 0 24 24" aria-hidden="true"><path fill="#A6CE39" d="M12 0C5.372 0 0 5.372 0 12s5.372 12 12 12 12-5.372 12-12S18.628 0 12 0zM7.369 4.378c.525 0 .947.431.947.947s-.422.947-.947.947a.95.95 0 0 1-.947-.947c0-.525.422-.947.947-.947zm-.722 3.038h1.444v10.041H6.647V7.416zm3.562 0h3.9c3.712 0 5.344 2.653 5.344 5.025 0 2.578-2.016 5.025-5.325 5.025h-3.919V7.416zm1.444 1.303v7.444h2.297c3.272 0 4.022-2.484 4.022-3.722 0-2.016-1.284-3.722-4.097-3.722h-2.222z"/></svg>'

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

    awards_html = ""
    for award in config.get('awards', []):
        awards_html += f'''
                <div class="news-item">
                    <span class="news-date">{award['year']}</span>
                    <p>{award['title']}, <em>{award['org']}</em></p>
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
                <a href="{config['google_scholar']}" class="nav-link" target="_blank" rel="noopener noreferrer">{SCHOLAR_ICON}Google Scholar</a>
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
                        <p>{SCHOLAR_ICON}<strong>Google Scholar:</strong> <a href="{config['google_scholar']}" target="_blank">Profile</a></p>
                        <p>{ORCID_ICON}<strong>ORCID:</strong> <a href="{config['orcid']}" target="_blank">0000-0001-8437-8702</a></p>
                    </div>
                </div>
            </section>

            <section class="news">
                <h2>Latest News</h2>
                <div class="news-list">{news_html}
                </div>
            </section>

            <section class="news">
                <h2>Honors and Awards</h2>
                <div class="news-list">{awards_html}
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

    grants_html = ""
    for grant in config.get('grants', []):
        grants_html += f'''                    <div class="pub-item">
                        <p class="pub-title">
                            <strong>{grant['title']}</strong>
                        </p>
                        <p class="pub-authors">
                            {grant['role']}
                        </p>
                        <p class="pub-meta">
                            <em>{grant['funder']}</em>, {grant['period']}. Grant number: {grant['number']}
                        </p>
                    </div>\n'''

    talks_html = ""
    for talk in config.get('talks', []):
        talks_html += f'''                    <div class="pub-item">
                        <p class="pub-title">
                            <strong>{talk['title']}</strong>
                        </p>
                        <p class="pub-meta">
                            <em>{talk['venue']}</em>, {talk['year']}.
                        </p>
                    </div>\n'''

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
                <a href="{config.get('cv_file', 'CV.pdf')}" class="nav-link" target="_blank" rel="noopener noreferrer">CV</a>
                <a href="{config['google_scholar']}" class="nav-link" target="_blank" rel="noopener noreferrer">{SCHOLAR_ICON}Google Scholar</a>
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

                <h2 style="margin-top: 40px;">Grants</h2>
                <div class="pub-list">
{grants_html}                </div>

                <h2 style="margin-top: 40px;">Invited Talks</h2>
                <div class="pub-list">
{talks_html}                </div>
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

    awards_html = ""
    for award in config.get('awards', []):
        if award.get('teaching'):
            awards_html += f'''                <p style="margin-bottom: 10px; color: #666; font-weight: 500;">
                    <strong>Award:</strong> {award['title']} during the academic year {award['year']}, {award['org']}
                </p>
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
                <a href="{config.get('cv_file', 'CV.pdf')}" class="nav-link" target="_blank" rel="noopener noreferrer">CV</a>
                <a href="{config['google_scholar']}" class="nav-link" target="_blank" rel="noopener noreferrer">{SCHOLAR_ICON}Google Scholar</a>
            </nav>
        </header>

        <main class="content">
            <section class="publications">
                <h2>Teaching Experience</h2>
{awards_html}                {teaching_html}
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
