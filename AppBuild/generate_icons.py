"""
Script de génération automatique d'icônes PWA/Android/Electron
Génère des icônes professionnelles sans intervention manuelle
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_pharmacy_icon(size, output_path):
    """
    Crée une icône professionnelle de pharmacie avec croix verte et caducée
    
    Args:
        size: Taille de l'icône (ex: 192, 512)
        output_path: Chemin de sortie
    """
    # Couleurs professionnelles de pharmacie
    green_primary = (46, 125, 50)    # Vert pharmacie principal
    green_dark = (27, 94, 32)         # Vert foncé pour l'ombre
    white = (255, 255, 255)
    
    # Créer l'image avec coins arrondis
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Dessiner un carré arrondi (fond)
    corner_radius = size // 8
    draw.rounded_rectangle(
        [(0, 0), (size, size)],
        radius=corner_radius,
        fill=green_primary
    )
    
    # Dimensions de la croix (70% de la taille)
    cross_size = int(size * 0.7)
    cross_thickness = int(cross_size * 0.25)
    start_pos = (size - cross_size) // 2
    
    # Dessiner la croix verte plus claire
    cross_color = (76, 175, 80)  # Vert plus clair pour la croix
    
    # Barre horizontale
    draw.rounded_rectangle(
        [
            (start_pos, start_pos + (cross_size - cross_thickness) // 2),
            (start_pos + cross_size, start_pos + (cross_size + cross_thickness) // 2)
        ],
        radius=cross_thickness // 4,
        fill=cross_color
    )
    
    # Barre verticale
    draw.rounded_rectangle(
        [
            (start_pos + (cross_size - cross_thickness) // 2, start_pos),
            (start_pos + (cross_size + cross_thickness) // 2, start_pos + cross_size)
        ],
        radius=cross_thickness // 4,
        fill=cross_color
    )
    
    # Dessiner le symbole du caducée simplifié au centre
    center_x = size // 2
    center_y = size // 2
    caducee_height = int(cross_thickness * 1.8)
    caducee_width = int(cross_thickness * 0.15)
    
    # Bâton central du caducée
    staff_width = max(2, size // 80)
    draw.rectangle(
        [
            (center_x - staff_width, center_y - caducee_height // 2),
            (center_x + staff_width, center_y + caducee_height // 2)
        ],
        fill=white
    )
    
    # Serpent simplifié (forme en S)
    snake_width = max(2, size // 100)
    points_left = []
    points_right = []
    
    for i in range(20):
        t = i / 19.0
        y = center_y - caducee_height // 2 + t * caducee_height
        x_offset = int((caducee_width / 2) * (1 if (i // 5) % 2 == 0 else -1))
        
        if i % 5 < 3:
            points_left.append((center_x + x_offset, int(y)))
        else:
            points_right.append((center_x + x_offset, int(y)))
    
    # Dessiner le serpent
    if len(points_left) > 1:
        draw.line(points_left, fill=white, width=snake_width)
    if len(points_right) > 1:
        draw.line(points_right, fill=white, width=snake_width)
    
    # Coupe au sommet (petit cercle)
    cup_radius = max(3, size // 50)
    draw.ellipse(
        [
            (center_x - cup_radius, center_y - caducee_height // 2 - cup_radius),
            (center_x + cup_radius, center_y - caducee_height // 2 + cup_radius)
        ],
        fill=white
    )
    
    # Sauvegarder
    img.save(output_path, 'PNG', quality=95)
    print(f"✅ Icône créée: {output_path} ({size}x{size})")

def generate_all_icons():
    """Génère toutes les icônes nécessaires pour PWA, Android et Electron"""
    
    # Chemins de sortie
    base_dir = os.path.dirname(os.path.abspath(__file__))
    icons_dir = os.path.join(base_dir, 'static', 'icons')
    
    # Créer le dossier si nécessaire
    os.makedirs(icons_dir, exist_ok=True)
    
    print("🎨 Génération des icônes professionnelles PharmaCare...")
    print(f"📁 Dossier de sortie: {icons_dir}\n")
    
    # Icônes PWA (Android)
    sizes_pwa = [192, 512]
    for size in sizes_pwa:
        output_path = os.path.join(icons_dir, f'icon-{size}x{size}.png')
        create_pharmacy_icon(size, output_path)
    
    # Icônes supplémentaires pour Android/PWA
    additional_sizes = [72, 96, 128, 144, 152, 384]
    for size in additional_sizes:
        output_path = os.path.join(icons_dir, f'icon-{size}x{size}.png')
        create_pharmacy_icon(size, output_path)
    
    # Icône Electron (Windows)
    electron_dir = os.path.join(base_dir, 'electron-app', 'build')
    os.makedirs(electron_dir, exist_ok=True)
    
    electron_sizes = [16, 32, 64, 128, 256, 512, 1024]
    for size in electron_sizes:
        output_path = os.path.join(electron_dir, f'icon-{size}x{size}.png')
        create_pharmacy_icon(size, output_path)
    
    # Icône .ico pour Windows (combinaison de plusieurs tailles)
    print("\n🖼️ Création de l'icône Windows (.ico)...")
    try:
        ico_images = []
        for size in [16, 32, 48, 64, 128, 256]:
            img_path = os.path.join(electron_dir, f'icon-{size}x{size}.png')
            if os.path.exists(img_path):
                ico_images.append(Image.open(img_path))
        
        if ico_images:
            ico_path = os.path.join(electron_dir, 'icon.ico')
            ico_images[0].save(
                ico_path,
                format='ICO',
                sizes=[(img.width, img.height) for img in ico_images]
            )
            print(f"✅ Icône Windows créée: {ico_path}")
    except Exception as e:
        print(f"⚠️ Erreur création .ico: {e}")
    
    # Icône Capacitor (Android)
    android_res_dir = os.path.join(base_dir, 'android-app', 'android', 'app', 'src', 'main', 'res')
    android_icons = {
        'mipmap-ldpi': 36,
        'mipmap-mdpi': 48,
        'mipmap-hdpi': 72,
        'mipmap-xhdpi': 96,
        'mipmap-xxhdpi': 144,
        'mipmap-xxxhdpi': 192
    }
    
    for folder, size in android_icons.items():
        folder_path = os.path.join(android_res_dir, folder)
        os.makedirs(folder_path, exist_ok=True)
        
        # ic_launcher
        output_path = os.path.join(folder_path, 'ic_launcher.png')
        create_pharmacy_icon(size, output_path)
        
        # ic_launcher_round (icône ronde)
        output_path_round = os.path.join(folder_path, 'ic_launcher_round.png')
        create_pharmacy_icon(size, output_path_round)
    
    print("\n" + "="*60)
    print("🎉 Toutes les icônes ont été générées avec succès !")
    print("="*60)
    print(f"\n📂 Emplacements:")
    print(f"   • PWA/Web: {icons_dir}")
    print(f"   • Electron: {electron_dir}")
    print(f"   • Android: {android_res_dir}")

if __name__ == '__main__':
    try:
        generate_all_icons()
    except Exception as e:
        print(f"\n❌ Erreur lors de la génération: {e}")
        print("\n💡 Assurez-vous d'avoir installé Pillow:")
        print("   pip install Pillow")
