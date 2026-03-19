# Fuyu Guo - Personal Academic Website

Your website is now **content-driven**. All text, publications, news, and teaching info is in `config.json`. Just edit that file!

## Quick Start

### 1. Edit Your Content

Open `config.json` and update:
- **Personal info**: name, email, phone, institution
- **About section**: Update the `about` and `bio2` fields
- **News**: Add/edit items in the `news` array
- **Publications**: Add papers to the `publications` array
- **Teaching**: Update courses in the `teaching` array

### 2. Rebuild Your Website

After editing `config.json`, run:
```bash
python build.py
```

This regenerates `index.html`, `research.html`, and `teaching.html` automatically.

### 3. View Your Site

Open in browser:
```bash
python -m http.server 8000
```
Visit `http://localhost:8000`

---

## config.json Structure

```json
{
  "name": "Your Name",
  "email": "your.email@example.com",
  "phone": "+1 xxx-xxx-xxxx",
  "about": "Your bio paragraph 1",
  "bio2": "Your bio paragraph 2",
  "research_interests": "What you research",
  "news": [
    {"date": "Month Year", "content": "News item"}
  ],
  "publications": [
    {
      "year": 2024,
      "title": "Paper title",
      "authors": "Author names",
      "journal": "Journal name",
      "volume": "X",
      "pages": "X-X",
      "journal_url": "https://doi.org/xxxxx"
    }
  ],
  "teaching": [
    {
      "institution": "University Name",
      "courses": [
        {"semester": "2024 Fall", "courses_list": ["COURSE 101: Name"]}
      ]
    }
  ]
}
```

---

## Adding/Editing Content

### Add a Publication
In `config.json`, add to the `publications` array:
```json
{
  "year": 2025,
  "title": "Your new paper",
  "authors": "You, Co-Author",
  "journal": "Journal Name",
  "volume": "10",
  "pages": "1-10",
  "journal_url": "https://doi.org/xxxxx"
}
```
Then run `python build.py`

### Add News
In `config.json`, add to the `news` array:
```json
{
  "date": "March 2026",
  "content": "Your news here"
}
```
Then run `python build.py`

### Change Styling
Edit `styles.css` directly. Colors, fonts, spacing all there.

---

## Deploy to GitHub Pages

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/fuyuguo/fuyuguo.github.io.git
git push -u origin main
```

Your site goes live at `https://fuyuguo.github.io`

---

## Files Explained

- **`config.json`** – All your content (edit this!)
- **`build.py`** – Script that reads config.json and generates HTML
- **`index.html`**, **`research.html`**, **`teaching.html`** – Generated automatically (don't edit directly)
- **`styles.css`** – Styling (edit this to change colors/fonts)
- **`profile.jpg`** – Add your photo here

---

**Workflow:**
1. Edit `config.json`
2. Run `python build.py`
3. View in browser or push to GitHub

That's it!
