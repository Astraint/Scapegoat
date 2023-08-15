from __future__ import annotations

from Utils import find, find_all, relpath, markdownify, run, count_lstrip

from typing import Set, Mapping, Union, Iterable, List
from Tree import Tree, Element
from Utils import SOURCE_DIR, TARGET_DIR

TOC : str = "Table Of Contents.md"
TOC_STR : str = "[Go back to ToC]"

def linkify(toc : Tree, files : List[str]) -> List[str]:
    commands : List[str] = []
    for element in toc.elements:
        # if element.depth >= 2: continue
        for file in files:
            path = relpath(element.filename, file).replace("/", "\/")
            tag = markdownify(element.name).replace("/", "\/")
            name = element.name.replace("/", "\/").split(" (")[0]
            file = file.replace(" ", "\ ")
            commands.append(f"sed -i 's/ {name}/ [{name}](<{path}\#{tag}>)/g' {TARGET_DIR + file}")
    for successor in toc.successors:
        # new_path = path  if toc.key != Tree.ROOT else ""
        commands = commands + linkify(toc.successors[successor], files)
    return commands

def make_toc(files : List[str]) -> Tree:
    toc : Tree = Tree()
    for filename in files:
        with open(SOURCE_DIR + filename, "r") as file:
            for line in file:
                # TODO
                if line.startswith("#"):
                    line, depth = count_lstrip(line, "#")
                    line = line.lstrip("\t\n ").rstrip("\n \t")
                    toc.add_element(filename, Element(line, filename, depth - 1))
                # if line.startswith("## "):
                #     toc.add_element(filename, Element(line[3:].rstrip("\n \t"), filename, 1))
                # if line.startswith("### "):
                #     toc.add_element(filename, Element(line[4:].rstrip("\n \t"), filename, 2))
            if "NPC" in filename: toc.add_element(filename, Element("Sheet", filename.replace(".md", ".pdf"), 2, tag = ""))
    with open(TARGET_DIR + TOC, "w") as file:
        file.write("# Table Of Contents\n\n")
        file.write(str(toc))
    return toc

def tocify() -> None:
    toc_path : str = TARGET_DIR + TOC
    md_files : List[str] = find_all("*.md", TARGET_DIR)
    toc = make_toc(md_files)
    
    for filename in md_files:
        with open(TARGET_DIR + filename, "r+") as file:
            expected_line : str = f"[Go back to ToC](<{relpath(toc_path, filename)}>)\n"
            existing_content = file.read()
            if not existing_content.startswith(expected_line):
                if existing_content.startswith(TOC_STR):
                    existing_content = "\n".join(existing_content.split("\n")[1:])
                file.seek(0)
                file.write(expected_line + "\n" + existing_content)
                
    commands = linkify(toc, md_files)
    for cmd in commands:
        run(cmd)       
