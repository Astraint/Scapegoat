from __future__ import annotations

from typing import Union, List, Mapping

from Utils import markdownify, TAB

class Element:
    
    FAKE_TAG : str = "mapldo,ek,kfe154mm!!"
    
    def __init__(self : Element, name : str, filename : str, depth : int, tag : str = FAKE_TAG) -> Element:
        self.name : str = name
        self.depth : int = depth
        self.filename : str = filename
        self.tag : str = tag if tag != Element.FAKE_TAG else name
        
    def __str__(self : Element) -> str:
        indent : str = TAB * self.depth
        tag = "#" + markdownify(self.tag) if self.tag != "" else ""
        return f"{indent}- [{self.name}](<{self.filename}{tag}>)"

class Tree:
    
    ROOT : str = "ROOT_NODE_NOT_TOC_14d88e2sl:ù$ùd$s!!ùs$x"
    INDENT : int = 0
    
    def __init__(self : Tree, key : str = ROOT, predecessor : Union[Tree, None] = None) -> Tree:
        self.predecessor : Union[Tree, None] = predecessor
        self.key : str = key
        self.successors : Mapping[str, Tree] = {}
        self.elements : List[Element] = []
    
    def prev(self : Tree) -> Tree:
        if self.predecessor is None: raise IndexError
        return self.predecessor
    
    def has_predecessor(self  : Tree) -> bool:
        return self.predecessor is not None
    
    def get_successor(self : Tree, key : str) -> Tree:
        if not self.is_successor(key): raise IndexError
        return self.successors[key]
    
    def is_successor(self : Tree, key : str) -> bool:
        return key in self.successors
    
    def add_successor(self : Tree, key : str) -> None:
        if self.is_successor(key): return
        self.successors[key] = Tree(key, predecessor=self)
        
    def __add_element(self : Tree, keys : List[str], index : int, element : Element) -> None:
        if len(keys) == index: self.elements.append(element); return
        if not self.is_successor(keys[index]): self.add_successor(keys[index])
        self.get_successor(keys[index]).__add_element(keys, index + 1, element)
    
    def add_element(self : Tree, path : str, element : Element) -> None:
        path : List[str] = path.split("/")
        keys = path[:-1]
        self.__add_element(keys, 0, element)
        
    def __str__(self : Tree) -> str:
        s = ""
        if self.key == Tree.ROOT:
            for successor in self.successors:
                s += f"{self.successors[successor]}\n"
            s = s.rstrip("\n")
        else:
            tabs : str = Tree.INDENT * TAB
            s += f"{tabs}- {self.key}\n"
            for element in self.elements:
                if element.depth >= 3: continue
                s += f"{tabs}{TAB}{element}\n"
            Tree.INDENT += 1
            for successor in self.successors:
                s += f"{self.successors[successor]}\n"
            s = s.rstrip("\n")
            Tree.INDENT -= 1
        return s
        