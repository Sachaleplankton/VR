import unreal
from pathlib import Path

# --- CONFIGURATION ---
FBX_SOURCE_DIR = Path("C:/Unreal Projects/fichiersFBX")
FBX_DEST = "/Game/Meshes"
BP_DEST = "/Game/Blueprints"
PARENT_BLUEPRINT_PATH = "/Game/Models/Meshes/BuildActor"  # Référence de ton Blueprint parent

# --- FBX IMPORT UTILS ---

def build_options() -> unreal.FbxImportUI:
    options = unreal.FbxImportUI()
    options.set_editor_property("import_mesh", True)
    options.set_editor_property("import_textures", False)
    options.set_editor_property("import_materials", False)
    options.set_editor_property("import_as_skeletal", False)
    options.static_mesh_import_data.set_editor_property("import_uniform_scale", 1.0)
    options.static_mesh_import_data.set_editor_property("combine_meshes", True)
    options.static_mesh_import_data.set_editor_property("auto_generate_collision", True)
    return options

def build_import_task(mesh_name: str, filename: Path, destination_path: str, options: unreal.FbxImportUI):
    task = unreal.AssetImportTask()
    task.set_editor_property("automated", True)
    task.set_editor_property("destination_name", mesh_name)
    task.set_editor_property("destination_path", destination_path)
    task.set_editor_property("filename", str(filename))
    task.set_editor_property("replace_existing", True)
    task.set_editor_property("save", True)
    task.set_editor_property("options", options)
    return task

def find_fbx_files(source_dir: Path) -> dict:
    return {
        f"SM_{file.stem}": file
        for file in source_dir.glob("*.fbx")
    }

def import_all_meshes(mesh_data: dict):
    options = build_options()
    tasks = [
        build_import_task(name, fbx_path, FBX_DEST, options)
        for name, fbx_path in mesh_data.items()
    ]
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)

# --- BLUEPRINT CREATION ---

def make_blueprint(package_path, asset_name, parent_class):
    if not unreal.EditorAssetLibrary.does_directory_exist(package_path):
        unreal.EditorAssetLibrary.make_directory(package_path)

    bp_factory = unreal.BlueprintFactory()
    bp_factory.set_editor_property("ParentClass", parent_class)

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    bp = asset_tools.create_asset(
        asset_name=asset_name,
        package_path=package_path,
        asset_class=unreal.Blueprint,
        factory=bp_factory
    )

    if not bp:
        raise Exception(f"❌ Échec de la création du Blueprint '{asset_name}' dans '{package_path}'")
    
    print(f"✅ Blueprint créé : {package_path}/{asset_name}")
    return bp

# --- STATIC MESH ASSIGNMENT ---
def add_static_mesh_component_to_blueprint(bp_path, mesh_path):
    # Convertir les chemins en AssetData
    bp_asset = unreal.EditorAssetLibrary.find_asset_data(bp_path)
    mesh_asset = unreal.EditorAssetLibrary.find_asset_data(mesh_path)

    if not bp_asset.is_valid():
        unreal.SystemLibrary.print_string(None, f"Failed to load blueprint from {bp_path}")
        return

    if not mesh_asset.is_valid():
        unreal.SystemLibrary.print_string(None, f"Failed to load mesh from {mesh_path}")
        return

    # Charger le blueprint et le mesh depuis l'AssetData
    blueprint = bp_asset.get_asset()
    mesh = mesh_asset.get_asset()

    # Créer un composant StaticMesh et lui assigner le mesh
    static_mesh_component = unreal.StaticMeshComponent()
    static_mesh_component.set_static_mesh(mesh)

    # Ajouter le composant StaticMesh au Blueprint
    # Assure-toi que le Blueprint est valide et qu'il peut recevoir un composant
    blueprint.add_actor_component(static_mesh_component)

    # Sauvegarder le blueprint après modification
    unreal.EditorAssetLibrary.save_asset(bp_path)
    #return True

# --- MAIN ---

def main():
    mesh_data = find_fbx_files(FBX_SOURCE_DIR)
    if not mesh_data:
        print("⚠️ Aucun fichier FBX trouvé.")
        return

    print(f"🔍 Fichiers détectés : {list(mesh_data.keys())}")

    import_all_meshes(mesh_data)

    # Charger la classe générée du Blueprint parent
    bp_generated_class = unreal.EditorAssetLibrary.load_blueprint_class(PARENT_BLUEPRINT_PATH)
    if not bp_generated_class:
        raise Exception(f"❌ Classe générée introuvable pour le Blueprint parent : {PARENT_BLUEPRINT_PATH}")

    for mesh_name in mesh_data:
        bp_name = f"BP_{mesh_name}"
        mesh_path = f"{FBX_DEST}/{mesh_name}.{mesh_name}"
        bp = make_blueprint(BP_DEST, bp_name, bp_generated_class)
        add_static_mesh_component_to_blueprint(bp, mesh_path)

if __name__ == "__main__":
    main()
