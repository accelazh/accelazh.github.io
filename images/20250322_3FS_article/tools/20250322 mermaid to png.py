import os
import re
import subprocess

input_md = r"..\01_3FS_DeepSeek_Copilot_4.md"
output_dir = r"..\images"

updated_md = r"..\01_3FS_DeepSeek_Copilot_4_updated.md"
image_dir = r"./images"

os.makedirs(output_dir, exist_ok=True)

with open(input_md, "r", encoding="utf-8") as f:
    content = f.read()

pattern = re.compile(r"```mermaid\s*\n(.*?)```", re.DOTALL)
matches = pattern.findall(content)

for i, diagram in enumerate(matches):
    mmd_path = os.path.join(output_dir, f"diagram_{i+1}.mmd")
    png_path = os.path.join(output_dir, f"diagram_{i+1}.png")

    with open(mmd_path, "w", encoding="utf-8") as f:
        f.write(diagram)

    subprocess.run([
        r"C:\Users\yilzhao\AppData\Roaming\npm\mmdc.cmd",
        "-i", mmd_path,
        "-o", png_path,
        "--scale", "8",
        "-t", "default"  # or dark, forest, neutral
    ], check=True)

replace_mermaid_to_img = False
if replace_mermaid_to_img:
    new_md = content
    for i, match in enumerate(matches):
        img_link = f"![diagram_{i+1}]({image_dir}/diagram_{i+1}.png)"
        new_md = new_md.replace(f"```mermaid\n{match}```", img_link)

    with open(updated_md, "w", encoding="utf-8") as f:
        f.write(new_md)

print(f"Exported {len(matches)} diagram(s) to {output_dir}")
