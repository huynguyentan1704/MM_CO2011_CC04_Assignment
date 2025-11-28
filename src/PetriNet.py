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
        tree = ET.parse(filename)
        root = tree.getroot()

        # tạo object rỗng
        obj = cls([], [], [], [], None, None, None)

        # tìm net
        net_el = root.find(".//{*}net")

        # ---------------------------
        # 1) Đọc PLACE giữ nguyên thứ tự
        # ---------------------------
        place_ids = []
        place_names = []
        markings = []

        for p in net_el.findall(".//{*}place"):
            pid = p.get("id")

            # name (có thể None)
            text_el = p.find(".//{*}name/{*}text")
            name = text_el.text.strip() if text_el is not None else None

            # initial marking
            m_el = p.find(".//{*}initialMarking/{*}text")
            if m_el is not None and m_el.text:
                m = int(m_el.text.strip())
            else:
                m = 0

            place_ids.append(pid)
            place_names.append(name)
            markings.append(m)

        # ---------------------------
        # 2) Đọc TRANSITION giữ nguyên thứ tự
        # ---------------------------
        trans_ids = []
        trans_names = []

        for t in net_el.findall(".//{*}transition"):
            tid = t.get("id")

            text_el = t.find(".//{*}name/{*}text")
            name = text_el.text.strip() if text_el is not None else None

            trans_ids.append(tid)
            trans_names.append(name)

        # Lưu vào object
        obj.place_ids = place_ids
        obj.place_names = place_names
        obj.trans_ids = trans_ids
        obj.trans_names = trans_names
        obj.M0 = np.array(markings, dtype=int)

        # ---------------------------
        # 3) Precompute index lookup
        # ---------------------------
        place_index = {pid: i for i, pid in enumerate(place_ids)}
        trans_index = {tid: j for j, tid in enumerate(trans_ids)}


        # ---------------------------
        # 4) Tạo I và O (PxT)
        # ---------------------------
        P = len(place_ids)
        T = len(trans_ids)

        I = np.zeros((T, P), dtype=int)  # T dòng, P cột
        O = np.zeros((T, P), dtype=int)


        # ---------------------------
        # 5) Duyệt ARC → gán I/O
        # ---------------------------
        for arc in net_el.findall(".//{*}arc"):
            src = arc.get("source")
            tgt = arc.get("target")

            # weight mặc định = 1
            w_el = arc.find(".//{*}inscription/{*}text")
            if w_el is not None and w_el.text:
                try:
                    w = int(w_el.text.strip())
                except:
                    w = 1
            else:
                w = 1

            # place → transition (input)
            if src in place_index and tgt in trans_index:
                j = place_index[src]
                i = trans_index[tgt]
                I[i, j] += w
            # transition → place (output)
            if src in trans_index and tgt in place_index:
                i = trans_index[src]
                j = place_index[tgt]
                O[i, j] += w

        obj.I = I
        obj.O = O

        return obj


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


