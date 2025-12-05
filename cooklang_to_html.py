#!/usr/bin/env python3
"""
CookLang to HTML Recipe Converter
Converts .cook files to HTML pages for Cristian's website
"""

import re
import sys
from pathlib import Path

def parse_cooklang(content):
    """Parse a CookLang file and extract metadata, ingredients, tools, and steps."""
    lines = content.split('\n')
    
    metadata = {}
    ingredients = []
    tools = []
    steps = []
    current_section = None
    intro = ""
    tips = []
    portioning_guide = []
    
    for line in lines:
        # Parse metadata
        if line.startswith('>>'):
            key, value = line[2:].split(':', 1)
            metadata[key.strip()] = value.strip()
            continue
        
        # Parse title
        if line.startswith('# '):
            metadata['title'] = line[2:].strip()
            continue
        
        # Section headers
        if line.startswith('## '):
            current_section = line[3:].strip()
            continue
        
        # Empty lines
        if not line.strip():
            continue
        
        # Handle each section
        if current_section == "Portioning Guide":
            portioning_guide.append(line.strip())
        
        elif current_section == "Ingredients":
            # Remove the leading dash and parse ingredient
            line = line.lstrip('- ').strip()
            # Extract from CookLang format
            clean_line = line
            # Remove CookLang markup but keep the info
            clean_line = re.sub(r'@([^{]+)\{([^}]*)\}(?:\{([^}]*)\})?', lambda m: format_ingredient(m), clean_line)
            if clean_line:
                ingredients.append(clean_line)
        
        elif current_section == "Tools":
            # Remove the leading dash and extract tool name
            line = line.lstrip('- ').strip()
            tool_match = re.search(r'#([^{]+)\{\}', line)
            if tool_match:
                tools.append(tool_match.group(1).strip())
        
        elif current_section == "Instructions":
            # Clean instructions of CookLang syntax for display
            clean_line = line.strip()
            if clean_line:
                steps.append(clean_line)
        
        elif current_section == "Tips":
            # Remove leading dash
            tips.append(line.lstrip('- ').strip())
        
        elif current_section is None and not line.startswith('>>'):
            # Intro text
            intro += line.strip() + " "
    
    return {
        'metadata': metadata,
        'intro': intro.strip(),
        'portioning_guide': portioning_guide,
        'ingredients': ingredients,
        'tools': tools,
        'steps': steps,
        'tips': tips
    }

def format_ingredient(match):
    """Format an ingredient from CookLang syntax to readable text."""
    name = match.group(1).strip()
    quantity_unit = match.group(2) if match.group(2) else ""
    notes = match.group(3) if match.lastindex >= 3 and match.group(3) else ""
    
    # Parse quantity and unit
    if '%' in quantity_unit:
        parts = quantity_unit.split('%')
        quantity = parts[0] if parts[0] else ""
        unit = parts[1] if len(parts) > 1 else ""
        result = f"{quantity} {unit} {name}".strip()
    elif quantity_unit:
        result = f"{quantity_unit} {name}".strip()
    else:
        result = name
    
    if notes:
        result += f", {notes}"
    
    return result

def generate_html(recipe_data, output_file):
    """Generate HTML from parsed recipe data."""
    
    meta = recipe_data['metadata']
    title = meta.get('title', 'Recipe')
    servings = meta.get('servings', '2-4')
    total_time = meta.get('time', '30 minutes')
    prep_time = meta.get('prep_time', '15 minutes')
    cook_time = meta.get('cook_time', total_time)
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Cristian Villatoro</title>
    <link rel="stylesheet" href="styles.css">
    <style>
        .recipe-detail {{
            max-width: 800px;
            margin: 0 auto;
        }}
        
        .recipe-header {{
            padding: 3rem 0 2rem;
            border-bottom: 2px solid var(--cooking-secondary);
            margin-bottom: 2rem;
        }}
        
        .recipe-header h1 {{
            font-family: var(--font-serif);
            font-size: 2.5rem;
            color: var(--cooking-dark);
            margin-bottom: 1rem;
        }}
        
        .recipe-intro {{
            color: var(--text-medium);
            font-size: 1.1rem;
            line-height: 1.7;
            margin-bottom: 1.5rem;
        }}
        
        .recipe-stats {{
            display: flex;
            gap: 2rem;
            flex-wrap: wrap;
            padding: 1.5rem;
            background-color: var(--cooking-bg);
            border-radius: 8px;
        }}
        
        .stat {{
            display: flex;
            flex-direction: column;
        }}
        
        .stat-label {{
            font-size: 0.85rem;
            color: var(--text-light);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.25rem;
        }}
        
        .stat-value {{
            font-size: 1.1rem;
            color: var(--cooking-dark);
            font-weight: 600;
        }}
        
        .recipe-section {{
            margin: 3rem 0;
        }}
        
        .recipe-section h2 {{
            font-size: 1.75rem;
            color: var(--cooking-dark);
            margin-bottom: 1rem;
            border-bottom: 2px solid var(--cooking-secondary);
            padding-bottom: 0.5rem;
        }}
        
        .ingredients-list {{
            list-style: none;
            padding: 0;
        }}
        
        .ingredients-list li {{
            padding: 0.75rem;
            border-bottom: 1px solid var(--border-color);
            color: var(--text-dark);
        }}
        
        .ingredients-list li:hover {{
            background-color: var(--cooking-bg);
        }}
        
        .instructions-list {{
            list-style: none;
            counter-reset: step-counter;
            padding: 0;
        }}
        
        .instructions-list li {{
            counter-increment: step-counter;
            position: relative;
            padding: 1.5rem 0 1.5rem 4rem;
            border-bottom: 1px solid var(--border-color);
            color: var(--text-dark);
            line-height: 1.7;
        }}
        
        .instructions-list li:before {{
            content: counter(step-counter);
            position: absolute;
            left: 0;
            top: 1.25rem;
            width: 2.5rem;
            height: 2.5rem;
            background-color: var(--cooking-primary);
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            font-size: 1.1rem;
        }}
        
        .recipe-notes {{
            background-color: var(--cooking-bg);
            padding: 1.5rem;
            border-left: 4px solid var(--cooking-secondary);
            border-radius: 4px;
            margin: 2rem 0;
        }}
        
        .recipe-notes h3 {{
            color: var(--cooking-dark);
            margin-bottom: 0.75rem;
            font-size: 1.2rem;
        }}
        
        .recipe-notes p, .recipe-notes ul {{
            color: var(--text-medium);
            line-height: 1.7;
            margin-bottom: 0.75rem;
        }}
        
        .recipe-notes ul {{
            padding-left: 1.5rem;
        }}
        
        .recipe-notes p:last-child {{
            margin-bottom: 0;
        }}
        
        .back-link {{
            display: inline-block;
            margin-bottom: 2rem;
            color: var(--cooking-primary);
            text-decoration: none;
            font-weight: 500;
        }}
        
        .back-link:hover {{
            text-decoration: underline;
        }}

        .portioning-guide {{
            background-color: var(--bg-light);
            padding: 1.5rem;
            border-radius: 8px;
            margin: 2rem 0;
        }}

        .portioning-guide h3 {{
            color: var(--cooking-dark);
            margin-bottom: 1rem;
            font-size: 1.2rem;
        }}

        .portioning-guide p {{
            color: var(--text-medium);
            line-height: 1.7;
            margin-bottom: 0.5rem;
        }}
    </style>
</head>
<body class="cooking-page">
    <nav class="navbar cooking-nav">
        <div class="nav-container">
            <div class="nav-brand"><a href="index.html">Cristian Villatoro</a></div>
            <ul class="nav-menu">
                <li><a href="cooking.html">← Back to Cooking</a></li>
            </ul>
        </div>
    </nav>

    <div class="container">
        <article class="recipe-detail">
            <a href="cooking.html#recipes" class="back-link">← All Recipes</a>
            
            <div class="recipe-header">
                <h1>{title}</h1>
                <p class="recipe-intro">{recipe_data['intro']}</p>
                
                <div class="recipe-stats">
                    <div class="stat">
                        <span class="stat-label">Prep Time</span>
                        <span class="stat-value">{prep_time}</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">Cook Time</span>
                        <span class="stat-value">{cook_time}</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">Total Time</span>
                        <span class="stat-value">{total_time}</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">Servings</span>
                        <span class="stat-value">{servings}</span>
                    </div>
                </div>
            </div>
'''
    
    # Add portioning guide if present
    if recipe_data['portioning_guide']:
        html += '''
            <div class="portioning-guide">
                <h3>🧮 Portioning Guide</h3>
'''
        for line in recipe_data['portioning_guide']:
            html += f'                <p>{line}</p>\n'
        html += '            </div>\n'
    
    # Ingredients section
    html += '''
            <section class="recipe-section">
                <h2>Ingredients</h2>
                <ul class="ingredients-list">
'''
    for ingredient in recipe_data['ingredients']:
        html += f'                    <li>{ingredient}</li>\n'
    
    html += '''                </ul>
            </section>
'''
    
    # Instructions section
    html += '''
            <section class="recipe-section">
                <h2>Instructions</h2>
                <ol class="instructions-list">
'''
    for step in recipe_data['steps']:
        html += f'                    <li>{step}</li>\n'
    
    html += '''                </ol>
            </section>
'''
    
    # Tips section
    if recipe_data['tips']:
        html += '''
            <div class="recipe-notes">
                <h3>✨ Tips</h3>
                <ul>
'''
        for tip in recipe_data['tips']:
            html += f'                    <li>{tip}</li>\n'
        html += '''                </ul>
            </div>
'''
    
    html += '''        </article>
    </div>

    <footer class="cooking-footer">
        <div class="container">
            <p><a href="cooking.html">← Back to all recipes</a></p>
        </div>
    </footer>
</body>
</html>
'''
    
    return html

def main():
    if len(sys.argv) < 2:
        print("Usage: python cooklang_to_html.py recipe.cook")
        print("Output: recipe.html")
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    
    if not input_file.exists():
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)
    
    # Read CookLang file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse recipe
    recipe_data = parse_cooklang(content)
    
    # Generate HTML
    html = generate_html(recipe_data, input_file.stem)
    
    # Write output
    output_file = input_file.with_suffix('.html')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ Converted {input_file} → {output_file}")
    print(f"📊 Ingredients: {len(recipe_data['ingredients'])}")
    print(f"🔧 Tools: {len(recipe_data['tools'])}")
    print(f"📝 Steps: {len(recipe_data['steps'])}")

if __name__ == "__main__":
    main()


def generate_html(recipe_data, output_file):
    """Generate HTML from parsed recipe data."""
    
    meta = recipe_data['metadata']
    title = meta.get('title', 'Recipe')
    source = meta.get('source', 'Cristian Villatoro')
    servings = meta.get('servings', '2-4')
    total_time = meta.get('time', '30 minutes')
    
    # Calculate rough prep/cook time (you can adjust this logic)
    prep_time = "15 minutes"
    cook_time = total_time
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Cristian Villatoro</title>
    <link rel="stylesheet" href="styles.css">
    <style>
        .recipe-detail {{
            max-width: 800px;
            margin: 0 auto;
        }}
        
        .recipe-header {{
            padding: 3rem 0 2rem;
            border-bottom: 2px solid var(--cooking-secondary);
            margin-bottom: 2rem;
        }}
        
        .recipe-header h1 {{
            font-family: var(--font-serif);
            font-size: 2.5rem;
            color: var(--cooking-dark);
            margin-bottom: 1rem;
        }}
        
        .recipe-intro {{
            color: var(--text-medium);
            font-size: 1.1rem;
            line-height: 1.7;
            margin-bottom: 1.5rem;
        }}
        
        .recipe-stats {{
            display: flex;
            gap: 2rem;
            flex-wrap: wrap;
            padding: 1.5rem;
            background-color: var(--cooking-bg);
            border-radius: 8px;
        }}
        
        .stat {{
            display: flex;
            flex-direction: column;
        }}
        
        .stat-label {{
            font-size: 0.85rem;
            color: var(--text-light);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.25rem;
        }}
        
        .stat-value {{
            font-size: 1.1rem;
            color: var(--cooking-dark);
            font-weight: 600;
        }}
        
        .recipe-section {{
            margin: 3rem 0;
        }}
        
        .recipe-section h2 {{
            font-size: 1.75rem;
            color: var(--cooking-dark);
            margin-bottom: 1rem;
            border-bottom: 2px solid var(--cooking-secondary);
            padding-bottom: 0.5rem;
        }}
        
        .ingredients-list {{
            list-style: none;
            padding: 0;
        }}
        
        .ingredients-list li {{
            padding: 0.75rem;
            border-bottom: 1px solid var(--border-color);
            color: var(--text-dark);
        }}
        
        .ingredients-list li:hover {{
            background-color: var(--cooking-bg);
        }}
        
        .instructions-list {{
            list-style: none;
            counter-reset: step-counter;
            padding: 0;
        }}
        
        .instructions-list li {{
            counter-increment: step-counter;
            position: relative;
            padding: 1.5rem 0 1.5rem 4rem;
            border-bottom: 1px solid var(--border-color);
            color: var(--text-dark);
            line-height: 1.7;
        }}
        
        .instructions-list li:before {{
            content: counter(step-counter);
            position: absolute;
            left: 0;
            top: 1.25rem;
            width: 2.5rem;
            height: 2.5rem;
            background-color: var(--cooking-primary);
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            font-size: 1.1rem;
        }}
        
        .recipe-notes {{
            background-color: var(--cooking-bg);
            padding: 1.5rem;
            border-left: 4px solid var(--cooking-secondary);
            border-radius: 4px;
            margin: 2rem 0;
        }}
        
        .recipe-notes h3 {{
            color: var(--cooking-dark);
            margin-bottom: 0.75rem;
            font-size: 1.2rem;
        }}
        
        .recipe-notes p, .recipe-notes ul {{
            color: var(--text-medium);
            line-height: 1.7;
            margin-bottom: 0.75rem;
        }}
        
        .recipe-notes ul {{
            padding-left: 1.5rem;
        }}
        
        .recipe-notes p:last-child {{
            margin-bottom: 0;
        }}
        
        .back-link {{
            display: inline-block;
            margin-bottom: 2rem;
            color: var(--cooking-primary);
            text-decoration: none;
            font-weight: 500;
        }}
        
        .back-link:hover {{
            text-decoration: underline;
        }}

        .portioning-guide {{
            background-color: var(--bg-light);
            padding: 1.5rem;
            border-radius: 8px;
            margin: 2rem 0;
        }}

        .portioning-guide h3 {{
            color: var(--cooking-dark);
            margin-bottom: 1rem;
            font-size: 1.2rem;
        }}

        .portioning-guide p {{
            color: var(--text-medium);
            line-height: 1.7;
            margin-bottom: 0.5rem;
        }}
    </style>
</head>
<body class="cooking-page">
    <nav class="navbar cooking-nav">
        <div class="nav-container">
            <div class="nav-brand"><a href="index.html">Cristian Villatoro</a></div>
            <ul class="nav-menu">
                <li><a href="cooking.html">← Back to Cooking</a></li>
            </ul>
        </div>
    </nav>

    <div class="container">
        <article class="recipe-detail">
            <a href="cooking.html#recipes" class="back-link">← All Recipes</a>
            
            <div class="recipe-header">
                <h1>{title}</h1>
                <p class="recipe-intro">{recipe_data['intro']}</p>
                
                <div class="recipe-stats">
                    <div class="stat">
                        <span class="stat-label">Prep Time</span>
                        <span class="stat-value">{prep_time}</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">Cook Time</span>
                        <span class="stat-value">{cook_time}</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">Total Time</span>
                        <span class="stat-value">{total_time}</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">Servings</span>
                        <span class="stat-value">{servings}</span>
                    </div>
                </div>
            </div>
'''
    
    # Add portioning guide if present
    if recipe_data['portioning_guide']:
        html += '''
            <div class="portioning-guide">
                <h3>🧮 Portioning Guide</h3>
'''
        for line in recipe_data['portioning_guide']:
            html += f'                <p>{line}</p>\n'
        html += '            </div>\n'
    
    # Ingredients section
    html += '''
            <section class="recipe-section">
                <h2>Ingredients</h2>
                <ul class="ingredients-list">
'''
    for ingredient in recipe_data['ingredients']:
        html += f'                    <li>{ingredient}</li>\n'
    
    html += '''                </ul>
            </section>
'''
    
    # Instructions section
    html += '''
            <section class="recipe-section">
                <h2>Instructions</h2>
                <ol class="instructions-list">
'''
    for step in recipe_data['steps']:
        html += f'                    <li>{step}</li>\n'
    
    html += '''                </ol>
            </section>
'''
    
    # Tips section
    if recipe_data['tips']:
        html += '''
            <div class="recipe-notes">
                <h3>✨ Final Tips</h3>
                <ul>
'''
        for tip in recipe_data['tips']:
            html += f'                    <li>{tip}</li>\n'
        html += '''                </ul>
            </div>
'''
    
    html += '''        </article>
    </div>

    <footer class="cooking-footer">
        <div class="container">
            <p><a href="cooking.html">← Back to all recipes</a></p>
        </div>
    </footer>
</body>
</html>
'''
    
    return html

def main():
    if len(sys.argv) < 2:
        print("Usage: python cooklang_to_html.py recipe.cook")
        print("Output: recipe.html")
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    
    if not input_file.exists():
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)
    
    # Read CookLang file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse recipe
    recipe_data = parse_cooklang(content)
    
    # Generate HTML
    html = generate_html(recipe_data, input_file.stem)
    
    # Write output
    output_file = input_file.with_suffix('.html')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ Converted {input_file} → {output_file}")
    print(f"📊 Ingredients: {len(recipe_data['ingredients'])}")
    print(f"🔧 Tools: {len(recipe_data['tools'])}")
    print(f"📝 Steps: {len(recipe_data['steps'])}")

if __name__ == "__main__":
    main()
