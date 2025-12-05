# Academic Website with Cooking Section

A professional academic website with an integrated cooking/recipe section. Built for hosting on GitHub Pages.

## 🌟 Features

### Main Academic Site
- Clean, modern design that's professional but approachable
- Sections: About, Research, Publications, Teaching, CV
- Responsive design (works on mobile, tablet, desktop)
- Smooth scrolling navigation

### Cooking Section
- Separate, warmer design aesthetic
- Recipe cards with filtering by category
- Individual recipe pages with detailed instructions
- "Food Musings" blog section for writing about techniques
- More casual, personal tone

## 🚀 Getting Started

### Setting Up on GitHub

1. **Create a new repository**
   - Go to GitHub.com and create a new repository
   - Name it `username.github.io` (replace `username` with your GitHub username)
   - Make it public
   - Don't initialize with README

2. **Upload your files**
   ```bash
   # In your terminal, navigate to the folder with these files
   cd path/to/your/files
   
   # Initialize git
   git init
   
   # Add all files
   git add .
   
   # Commit
   git commit -m "Initial commit"
   
   # Add your GitHub repo as remote
   git remote add origin https://github.com/username/username.github.io.git
   
   # Push to GitHub
   git branch -M main
   git push -u origin main
   ```

3. **Enable GitHub Pages**
   - Go to your repository settings
   - Scroll to "Pages" section
   - Under "Source", select "Deploy from a branch"
   - Choose "main" branch and "/ (root)" folder
   - Save

4. **Wait a few minutes**
   - Your site will be live at `https://username.github.io`

## 📝 Customizing Your Site

### Basic Information

1. **Personal Details** (in `index.html`):
   - Replace "Your Name" with your actual name
   - Update university, department, email
   - Add your GitHub, Google Scholar, LinkedIn links
   - Write your bio in the About section

2. **Profile Image**:
   - Add a photo named `profile.jpg` to the root folder
   - Recommended size: 500x500px

### Adding Content

#### Adding a New Recipe

1. **Update the recipe card** (in `cooking.html`):
   ```html
   <div class="recipe-card" data-category="dinner">
       <div class="recipe-image">
           <img src="your-recipe-image.jpg" alt="Recipe name">
       </div>
       <div class="recipe-content">
           <h3>Your Recipe Name</h3>
           <p class="recipe-description">Brief description...</p>
           <div class="recipe-meta">
               <span>🕐 30 min</span>
               <span>👥 4 servings</span>
           </div>
           <a href="recipe-yourrecipe.html" class="recipe-link">View Recipe →</a>
       </div>
   </div>
   ```

2. **Create the recipe page**:
   - Duplicate `recipe-roast-chicken.html`
   - Rename it (e.g., `recipe-pasta.html`)
   - Update the content with your recipe

#### Adding a New Food Musing

1. **Update the musings list** (in `cooking.html`):
   ```html
   <article class="musing">
       <div class="musing-date">January 2025</div>
       <h3>Your Title</h3>
       <p>Preview text...</p>
       <a href="musing-yourpost.html" class="read-more">Read more →</a>
   </article>
   ```

2. **Create the musing page**:
   - Duplicate `musing-maillard.html`
   - Rename it (e.g., `musing-knives.html`)
   - Write your content

#### Adding Publications

In `index.html`, find the Publications section and add:
```html
<div class="publication">
    <p class="pub-title">Your Paper Title</p>
    <p class="pub-authors"><strong>Your Name</strong>, Co-Authors</p>
    <p class="pub-venue">Conference/Journal Name, Year</p>
    <div class="pub-links">
        <a href="paper.pdf">PDF</a>
        <a href="https://arxiv.org/...">arXiv</a>
        <a href="https://github.com/...">Code</a>
    </div>
</div>
```

### Recipe Categories

To add a new recipe category:
1. Add a filter button in `cooking.html`
2. Use the same category name in recipe card `data-category` attribute

Available categories by default:
- `dinner`
- `baking`
- `breakfast`
- `sides`

## 🎨 Customizing Colors

Edit `styles.css` at the top where colors are defined:

```css
:root {
    /* Main site colors */
    --primary-color: #2c5f7d;      /* Main accent color */
    --secondary-color: #d4a574;    /* Secondary accent */
    
    /* Cooking section colors */
    --cooking-primary: #c25b3f;    /* Cooking page accent */
    --cooking-secondary: #f4a261;  /* Cooking highlights */
}
```

## 📱 Mobile Responsiveness

The site is already responsive! It automatically adapts to:
- Desktop (1100px+ wide)
- Tablet (768px-1099px)
- Mobile (320px-767px)

## 🔧 File Structure

```
├── index.html                    # Main academic page
├── cooking.html                  # Cooking section main page
├── styles.css                    # All styles
├── script.js                     # JavaScript (smooth scroll, filtering)
├── recipe-roast-chicken.html     # Example recipe
├── musing-maillard.html          # Example blog post
├── profile.jpg                   # Your photo (add this)
├── cv.pdf                        # Your CV (add this)
└── README.md                     # This file
```

## 💡 Tips

- **Keep it updated**: Add new publications and projects regularly
- **Images**: Optimize images before uploading (compress to ~200KB)
- **CV**: Keep a PDF version synced with your page
- **Recipe photos**: Not required, but they make the cooking section nicer
- **Consistent naming**: Use lowercase, hyphens for filenames (e.g., `recipe-pasta.html`)

## 🐛 Troubleshooting

**Site not loading?**
- Wait 5-10 minutes after pushing to GitHub
- Check GitHub Pages settings are correct
- Make sure repository is public

**Images not showing?**
- Check file paths are correct
- Make sure image files are in the same folder
- Use lowercase filenames

**Recipe filtering not working?**
- Check that `data-category` matches filter button values
- Make sure `script.js` is loaded

## 📄 License

Feel free to use this template for your own academic website! No attribution needed, though it's appreciated.

## 🤝 Need Help?

If you get stuck:
1. Check the GitHub Pages documentation
2. Make sure all files are in the root of your repository
3. Verify file names match the links in HTML files

---

Built with care (and a lot of coffee). Happy cooking and researching! 🎓🍳
