import numpy as np
import xml.etree.ElementTree as ET
from typing import List, Optional

class PetriNet:
    def __init__(
        self,
        place_ids: List[str],
        trans_ids: List[str],
        place_names: List[Optional[str]],
        trans_names: List[Optional[str]],
        I: np.ndarray,   
        O: np.ndarray, 
        M0: np.ndarray
    ):
        self.place_ids = place_ids
        self.trans_ids = trans_ids
        self.place_names = place_names
        self.trans_names = trans_names
        self.I = I
        self.O = O
        self.M0 = M0

    @classmethod
    def from_pnml(cls, filename: str) -> "PetriNet":
        """Parse a PNML file and construct a PetriNet object."""
        tree = ET.parse(filename)
        root = tree.getroot()
        
        # Handle namespace if present
        ns = {'pnml': 'http://www.pnml.org/version-2009/grammar/pnml'}
        if root.tag.startswith('{'):
            # Extract namespace
            ns_url = root.tag[1:root.tag.index('}')]
            ns = {'pnml': ns_url}
            use_ns = True
        else:
            use_ns = False
        
        def find_with_ns(element, tag):
            """Helper to find elements with or without namespace."""
            if use_ns:
                return element.findall(f'pnml:{tag}', ns)
            return element.findall(tag)
        
        def find_one_with_ns(element, tag):
            """Helper to find one element with or without namespace."""
            if use_ns:
                return element.find(f'pnml:{tag}', ns)
            return element.find(tag)
        
        # Find the net element
        net = find_one_with_ns(root, 'net')
        if net is None:
            net = root
        
        page = find_one_with_ns(net, 'page')
        if page is None:
            page = net
        
        # Parse places
        place_ids = []
        place_names = []
        initial_marking = {}
        
        for place in find_with_ns(page, 'place'):
            place_id = place.get('id')
            place_ids.append(place_id)
            
            # Get place name
            name_elem = find_one_with_ns(place, 'name')
            if name_elem is not None:
                text_elem = find_one_with_ns(name_elem, 'text')
                if text_elem is not None and text_elem.text:
                    place_names.append(text_elem.text.strip())
                else:
                    place_names.append(None)
            else:
                place_names.append(None)
            
            # Get initial marking
            marking_elem = find_one_with_ns(place, 'initialMarking')
            if marking_elem is not None:
                text_elem = find_one_with_ns(marking_elem, 'text')
                if text_elem is not None and text_elem.text:
                    initial_marking[place_id] = int(text_elem.text.strip())
                else:
                    initial_marking[place_id] = 0
            else:
                initial_marking[place_id] = 0
        
        # Parse transitions
        trans_ids = []
        trans_names = []
        
        for trans in find_with_ns(page, 'transition'):
            trans_id = trans.get('id')
            trans_ids.append(trans_id)
            
            # Get transition name
            name_elem = find_one_with_ns(trans, 'name')
            if name_elem is not None:
                text_elem = find_one_with_ns(name_elem, 'text')
                if text_elem is not None and text_elem.text:
                    trans_names.append(text_elem.text.strip())
                else:
                    trans_names.append(None)
            else:
                trans_names.append(None)
        
        # Build index maps
        place_idx = {pid: i for i, pid in enumerate(place_ids)}
        trans_idx = {tid: i for i, tid in enumerate(trans_ids)}
        
        n_places = len(place_ids)
        n_trans = len(trans_ids)
        
        # Initialize incidence matrices
        I = np.zeros((n_places, n_trans), dtype=int)
        O = np.zeros((n_places, n_trans), dtype=int)
        
        # Parse arcs
        for arc in find_with_ns(page, 'arc'):
            source = arc.get('source')
            target = arc.get('target')
            
            # Get arc weight (default is 1)
            weight = 1
            inscription = find_one_with_ns(arc, 'inscription')
            if inscription is not None:
                text_elem = find_one_with_ns(inscription, 'text')
                if text_elem is not None and text_elem.text:
                    weight = int(text_elem.text.strip())
            
            # Determine if arc is from place to transition or vice versa
            if source in place_idx and target in trans_idx:
                # Place to transition (input arc)
                p = place_idx[source]
                t = trans_idx[target]
                I[p, t] = weight
            elif source in trans_idx and target in place_idx:
                # Transition to place (output arc)
                t = trans_idx[source]
                p = place_idx[target]
                O[p, t] = weight
        
        # Build initial marking vector
        M0 = np.array([initial_marking.get(pid, 0) for pid in place_ids], dtype=int)
        
        return cls(place_ids, trans_ids, place_names, trans_names, I, O, M0)

    def __str__(self) -> str:
        s = []
        s.append("Places: " + str(self.place_ids))
        s.append("Place names: " + str(self.place_names))
        s.append("\nTransitions: " + str(self.trans_ids))
        s.append("Transition names: " + str(self.trans_names))
        s.append("\nI (input) matrix:")
        s.append(str(self.I))
        s.append("\nO (output) matrix:")
        s.append(str(self.O))
        s.append("\nInitial marking M0:")
        s.append(str(self.M0))
        return "\n".join(s)