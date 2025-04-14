 



import unreal
import os

# 🔧 PARAMÈTRES À ADAPTER
source_folder = "C:/Unreal Projects/fichiersFBX"  # Dossier sur disque contenant les FBX à importer
import_destination = "/Game/ImportedAssets"       # Où seront importés les Static Mesh (dans le Content Browser)
blueprint_folder = "/Game/Blueprint_Antoine/Generated"  # Dossier pour les Blueprints générés
data_table_path = "/Game/Blueprint_Antoine/NewDataTable"  # Chemin vers la DataTable
interface_path = "/Game/Blueprint_Antoine/BPI_Grab"         # Chemin vers l'interface à implémenter (optionnel)
thumbnail_path = "/Game/StarterContent/Textures/T_Checker_Noise_M.T_Checker_Noise_M"  # Chemin vers la texture miniature par défaut

# 🔁 Accès Unreal
asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
editor_util = unreal.EditorAssetLibrary

# 📦 Chargement des assets Unreal
interface_class = editor_util.load_asset(interface_path)
thumbnail_texture = editor_util.load_asset(thumbnail_path)
data_table = editor_util.load_asset(data_table_path)

# --- Utilitaire pour nettoyer les noms (remplacer les espaces par des underscores) ---
def clean_name(name: str) -> str:
    return name.replace(" ", "_")

# 💬 Fonction : importer un FBX et retourner le StaticMesh
def import_fbx(fbx_path, asset_name):
    task = unreal.AssetImportTask()
    task.filename = fbx_path
    task.destination_path = import_destination
    task.destination_name = asset_name
    task.replace_existing = True
    task.automated = True
    task.save = True

    options = unreal.FbxImportUI()
    options.import_mesh = True
    options.import_as_skeletal = False
    options.mesh_type_to_import = unreal.FBXImportType.FBXIT_STATIC_MESH
    options.static_mesh_import_data.combine_meshes = True
    task.options = options

    asset_tools.import_asset_tasks([task])
    return f"{import_destination}/{asset_name}.{asset_name}"

# 💬 Fonction : créer un Blueprint Actor avec un StaticMeshComponent
def create_actor_blueprint(asset_name, static_mesh):
    clean_asset_name = clean_name(asset_name)
    bp_name = f"BP_{clean_asset_name}"
    bp_path = f"{blueprint_folder}/{bp_name}"

    # Vérifier si le Blueprint existe déjà pour éviter les doublons
    if editor_util.does_asset_exist(bp_path):
        print(f"Blueprint {bp_name} déjà existant, utilisation de l'asset existant.")
        return editor_util.load_asset(bp_path)

    blueprint_factory = unreal.BlueprintFactory()
    blueprint_factory.set_editor_property("parent_class", unreal.Actor)

    bp = asset_tools.create_asset(bp_name, blueprint_folder, None, blueprint_factory)
    
    # Ajout du composant via BlueprintEditorLibrary
    comp = unreal.BlueprintEditorLibrary.add_component(bp, unreal.StaticMeshComponent, "StaticMeshComponent")
    comp.set_editor_property("static_mesh", static_mesh)

    # Ajouter l'interface, si définie
    if interface_class:
        unreal.BlueprintEditorLibrary.add_interface(bp, interface_class.get_path_name())

    unreal.EditorAssetLibrary.save_asset(bp.get_path_name())
    return bp

# 💬 Fonction : ajouter une ligne dans la DataTable
def add_to_data_table(row_name, blueprint_obj):
    clean_row_name = clean_name(row_name)
    
    # Création d'un dictionnaire dont les clés correspondent aux noms de propriétés définies dans ta structure (par ex. model_name, model_blueprint, thumbnail)
    row_data = {
        "model_name": clean_row_name,
        "model_blueprint": blueprint_obj.generated_class,
        "thumbnail": thumbnail_texture
    }

    added = data_table.add_row(unreal.Name(clean_row_name), row_data)
    if added:
        print(f"✔️ Ajouté à la DataTable : {clean_row_name}")
    else:
        print(f"⚠️ Échec ajout DataTable pour : {clean_row_name}")

# 📁 Boucle sur les fichiers FBX du dossier source
for file_name in os.listdir(source_folder):
    if file_name.lower().endswith(".fbx"):
        asset_name = os.path.splitext(file_name)[0]
        fbx_path = os.path.join(source_folder, file_name).replace("\\", "/")

        print(f"📥 Import de {asset_name}")
        asset_full_path = import_fbx(fbx_path, clean_name(asset_name))

        static_mesh = editor_util.load_asset(asset_full_path)
        if static_mesh:
            blueprint = create_actor_blueprint(asset_name, static_mesh)
            add_to_data_table(asset_name, blueprint)

