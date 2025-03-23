import re

def add_numbering_to_markdown(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    numbering = []  # Keeps track of the current number for each level
    header_pattern = re.compile(r'^(#{1,6})\s*(.*)$')
    new_lines = []

    for line in lines:
        match = header_pattern.match(line)
        if match:
            hashes, title = match.groups()
            level = len(hashes)

            # Expand or trim the numbering list to current level
            if len(numbering) < level:
                numbering += [0] * (level - len(numbering))
            else:
                numbering = numbering[:level]

            # Increment the current level
            numbering[-1] += 1

            # Compose the numbered header
            number_str = '.'.join(str(n) for n in numbering)
            new_title = f'{hashes} {number_str}. {title.strip()}'
            new_lines.append(new_title + '\n')
        else:
            new_lines.append(line)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print(f"Numbered headers written to {output_file}")

# === Usage ===
# Change filenames below as needed
input_md_file = r'..\01_3FS_DeepSeek_Copilot_2.md'
output_md_file = r'..\01_3FS_DeepSeek_Copilot_3.md'
add_numbering_to_markdown(input_md_file, output_md_file)
