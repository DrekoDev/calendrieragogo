import os
import re

# Configuration
# Script is in nouveau_site/, so backup is ../backup
BACKUP_DIR = "../backup"
NEW_SITE_DIR = "." # Current dir (nouveau_site)
TEMPLATE_FILE = "page_template.html" # Not used directly, embedded in string

# Ensure output directory exists
os.makedirs(NEW_SITE_DIR, exist_ok=True)

# Template for the new pages
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="css/style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
</head>
<body>

    <!-- Header -->
    <header>
        <div class="container navbar">
            <a href="index.html" class="logo">
                <img src="images/logo2022bleu.png" alt="Calendrier à GoGo Logo">
            </a>
            <div class="hamburger">
                <i class="fas fa-bars fa-lg"></i>
            </div>
            <nav class="nav-links">
                <a href="index.html">Accueil</a>
                <a href="#">Association</a>
                <a href="#">Entreprise</a>
                <a href="#">École</a>
                <a href="devis.html" class="btn-cta">Demander un Devis</a>
            </nav>
        </div>
    </header>

    <!-- Page Header -->
    <section class="hero" style="height: 30vh; min-height: 250px; background-image: linear-gradient(rgba(15, 23, 42, 0.7), rgba(15, 23, 42, 0.7)), url('images/bannieresite.jpg');">
        <div class="container hero-content">
            <h1>{header_title}</h1>
        </div>
    </section>

    <!-- Main Content -->
    <section class="container" style="padding: 4rem 0;">
        {content}
    </section>

    <!-- Footer -->
    <footer>
        <div class="container">
            <div class="footer-grid">
                <div class="footer-col">
                    <h4>Navigation</h4>
                    <ul>
                        <li><a href="index.html">Accueil</a></li>
                        <li><a href="quisommesnous.html">Qui sommes nous</a></li>
                        <li><a href="contact.html">Contact</a></li>
                        <li><a href="devis.html">Demande de devis</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h4>Nos Produits</h4>
                    <ul>
                        <li><a href="sousmainasso.html">Pour Associations</a></li>
                        <li><a href="bancairesouple.html">Pour Entreprises</a></li>
                        <li><a href="calendrier12pages.html">Pour Écoles</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h4>Contact</h4>
                    <p>Calendrier à GoGo</p>
                    <p>Tel : 06 50 83 43 04</p>
                    <p>Email : calendrieragogo@sfr.fr</p>
                </div>
            </div>
            <div class="copyright">
                &copy; 2025 Calendrier à GoGo. Tous droits réservés.
            </div>
        </div>
    </footer>

    <script src="js/main.js"></script>
    <script>
        // Simple Tab Script for migrated content
        document.addEventListener('DOMContentLoaded', function() {{
            const tabs = document.querySelectorAll('.nav-tabs a');
            tabs.forEach(tab => {{
                tab.addEventListener('click', function(e) {{
                    e.preventDefault();
                    
                    // Remove active class from all tabs and panes
                    document.querySelectorAll('.nav-tabs li').forEach(li => li.classList.remove('active'));
                    document.querySelectorAll('.tab-pane').forEach(pane => pane.classList.remove('active'));
                    
                    // Add active class to clicked tab and target pane
                    this.parentElement.classList.add('active');
                    const targetId = this.getAttribute('href').substring(1);
                    document.getElementById(targetId).classList.add('active');
                }});
            }});
        }});
    </script>
</body>
</html>
"""

def extract_content(html_content):
    # Try to find the main content section
    match = re.search(r'<section class="main-content">(.*?)</section>\s*<section id="footer-bar">', html_content, re.DOTALL)
    if match:
        return match.group(1)
    
    # Fallback: try to find content between header_text and footer-bar
    match = re.search(r'</section>\s*<section class="main-content">(.*?)</section>\s*<section id="footer-bar">', html_content, re.DOTALL)
    if match:
        return match.group(1)
        
    return "<p>Contenu non trouvé.</p>"

def extract_title(html_content):
    match = re.search(r'<title>(.*?)</title>', html_content, re.DOTALL)
    if match:
        title = match.group(1)
        # Split by common separators and take the first relevant part
        # Priority: Split by '.' then ',' then '-'
        if '.' in title:
            return title.split('.')[1].strip() if 'Calendrier à GoGo' in title.split('.')[0] else title.split('.')[0].strip()
        return title.split(',')[0].strip()
    return "Calendrier à GoGo"

def migrate_file(filename):
    if filename in ['index.html', 'devis.html', 'point_relais.html']:
        return # Skip already handled files

    print(f"Migrating {filename}...")
    
    try:
        with open(os.path.join(BACKUP_DIR, filename), 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        # Extract parts
        page_title = extract_title(content)
        main_content = extract_content(content)
        
        # Clean up content
        # Replace image paths
        main_content = main_content.replace('themes/images/', 'images/')
        
        # Create new HTML
        new_html = HTML_TEMPLATE.format(
            title=page_title,
            header_title=page_title.replace('Calendrier à GoGo', '').strip() or page_title,
            content=main_content
        )
        
        # Write to new file
        with open(os.path.join(NEW_SITE_DIR, filename), 'w', encoding='utf-8') as f:
            f.write(new_html)
            
    except Exception as e:
        print(f"Error migrating {filename}: {e}")

def main():
    files = [f for f in os.listdir(BACKUP_DIR) if f.endswith('.html')]
    for file in files:
        migrate_file(file)

if __name__ == "__main__":
    main()
