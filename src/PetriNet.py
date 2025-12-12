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

    @classmethod
    def from_pnml(cls, filename: str) -> "PetriNet":


        """
        from_pnml: Step-by-step PNML parsing (summary)

        1. Parse the XML file and locate the <net> element.
        2. Read all places in order:
        - Extract id, optional name, and initial marking (default 0).
        - Check: id exists, no duplicates, marking is non-negative.
        3. Read all transitions in order:
        - Extract id and optional name.
        - Check: id exists, no duplicates, not overlapping with place ids.
        4. Build index lookup tables for places and transitions.
        5. Initialize I and O matrices with shape (T × P).
        6. Iterate through all arcs:
        - Extract source, target, and weight (default = 1).
        - Check: source/target exist, weight > 0.
        - Allowed connections:
            • place → transition → assign to I
            • transition → place → assign to O
            Invalid forms (place→place, trans→trans) raise an error.
        7. Validate matrix shapes and the length of M0.
        8. Ensure each transition has at least one incoming or outgoing arc.
        9. Return a fully constructed and validated PetriNet object.
        """

        tree = ET.parse(filename)
        root = tree.getroot()

        # ---------------------------
        # [CHECK] Phải có <net> trong file PNML
        # ---------------------------
        net_el = root.find(".//{*}net")
        if net_el is None:
            raise ValueError("PNML file does not contain a <net> element")

        # ---------------------------
        # 1) Đọc PLACE (giữ nguyên thứ tự)
        # ---------------------------
        place_ids = []
        place_names = []
        markings = []

        for p in net_el.findall(".//{*}place"):
            pid = p.get("id")

            # [CHECK] Mỗi place phải có id
            if pid is None:
                raise ValueError("Found a <place> without an id")

            # name (có thể None)
            text_el = p.find(".//{*}name/{*}text")
            name = text_el.text.strip() if text_el is not None and text_el.text else None

            # initial marking (mặc định = 0 nếu không có)
            m_el = p.find(".//{*}initialMarking/{*}text")
            if m_el is not None and m_el.text:
                m = int(m_el.text.strip())
                # [CHECK] Initial marking không được âm
                if m < 0:
                    raise ValueError(f"Initial marking of place '{pid}' must be non-negative")
            else:
                m = 0

            place_ids.append(pid)
            place_names.append(name)
            markings.append(m)

        # ---------------------------
        # [CHECK] Phải có ít nhất 1 place
        # ---------------------------
        if not place_ids:
            raise ValueError("PNML net has no places")

        # [CHECK] Không được trùng id giữa các place
        if len(place_ids) != len(set(place_ids)):
            raise ValueError("Duplicated place id detected in PNML")

        # ---------------------------
        # 2) Đọc TRANSITION (giữ nguyên thứ tự)
        # ---------------------------
        trans_ids = []
        trans_names = []

        for t in net_el.findall(".//{*}transition"):
            tid = t.get("id")

            # [CHECK] Mỗi transition phải có id
            if tid is None:
                raise ValueError("Found a <transition> without an id")

            text_el = t.find(".//{*}name/{*}text")
            name = text_el.text.strip() if text_el is not None and text_el.text else None

            trans_ids.append(tid)
            trans_names.append(name)

        # ---------------------------
        # [CHECK] Phải có ít nhất 1 transition
        # ---------------------------
        if not trans_ids:
            raise ValueError("PNML net has no transitions")

        # [CHECK] Không được trùng id giữa các transition
        if len(trans_ids) != len(set(trans_ids)):
            raise ValueError("Duplicated transition id detected in PNML")

        # [CHECK] Không được có id dùng cho cả place và transition
        if set(place_ids) & set(trans_ids):
            raise ValueError("Some ids are used both as place and transition")

        # ---------------------------
        # 3) Lưu các field cơ bản + M0
        # ---------------------------
        M0 = np.array(markings, dtype=int)

        # ---------------------------
        # 4) Precompute index lookup
        # ---------------------------
        place_index = {pid: i for i, pid in enumerate(place_ids)}
        trans_index = {tid: j for j, tid in enumerate(trans_ids)}

        # ---------------------------
        # 5) Tạo I và O (T x P) - T dòng, P cột
        # ---------------------------
        P = len(place_ids)
        T = len(trans_ids)

        I = np.zeros((T, P), dtype=int)  # I[t, p]
        O = np.zeros((T, P), dtype=int)  # O[t, p]

        # ---------------------------
        # 6) Duyệt ARC → gán I/O
        #    + Consistency check:
        #      - source/target phải tồn tại
        #      - chỉ cho phép place->transition hoặc transition->place
        #      - weight phải dương
        # ---------------------------
        for arc in net_el.findall(".//{*}arc"):
            arc_id = arc.get("id")
            src = arc.get("source")
            tgt = arc.get("target")

            # [CHECK] Arc phải có source và target
            if src is None or tgt is None:
                raise ValueError(f"Arc {arc_id}: missing source or target")

            src_is_place = src in place_index
            src_is_trans = src in trans_index
            tgt_is_place = tgt in place_index
            tgt_is_trans = tgt in trans_index

            # [CHECK] source phải là place hoặc transition đã khai báo
            if not (src_is_place or src_is_trans):
                raise ValueError(f"Arc {arc_id}: unknown source '{src}'")

            # [CHECK] target phải là place hoặc transition đã khai báo
            if not (tgt_is_place or tgt_is_trans):
                raise ValueError(f"Arc {arc_id}: unknown target '{tgt}'")

            # ---------------------------
            # Đọc weight, mặc định = 1.
            # Nếu parse int fail → raise để tránh model mơ hồ.
            # ---------------------------
            w_el = arc.find(".//{*}inscription/{*}text")
            if w_el is not None and w_el.text:
                try:
                    w = int(w_el.text.strip())
                except ValueError:
                    raise ValueError(f"Arc {arc_id}: weight must be an integer")
            else:
                w = 1

            # [CHECK] Trọng số phải dương
            if w <= 0:
                raise ValueError(f"Arc {arc_id}: weight must be positive, got {w}")

            # ---------------------------
            # Phân loại kiểu arc:
            #   - place -> transition  (input arc)  → I
            #   - transition -> place  (output arc) → O
            #   - place->place / trans->trans: vô nghĩa → lỗi
            # ---------------------------
            if src_is_place and tgt_is_trans:
                # place -> transition: input
                p = place_index[src]
                t = trans_index[tgt]
                I[t, p] += w

            elif src_is_trans and tgt_is_place:
                # transition -> place: output
                t = trans_index[src]
                p = place_index[tgt]
                O[t, p] += w

            else:
                # [CHECK] Cấm place->place và transition->transition
                raise ValueError(
                    f"Arc {arc_id}: invalid connection '{src}' -> '{tgt}'. "
                    "Only place->transition or transition->place are allowed."
                )

        # ---------------------------
        # 7) Sanity check cuối cùng cho shape
        # ---------------------------
        if I.shape != (T, P) or O.shape != (T, P):
            raise ValueError("I or O matrix has inconsistent shape with (T, P)")

        if M0.shape != (P,):
            raise ValueError("Initial marking M0 has inconsistent length with number of places")

        # ---------------------------
        # 8) Optional: check transition không bị "cô đơn"
        #    (không có input và không có output) → thường là model lỗi.
        # ---------------------------
        for t_idx, tid in enumerate(trans_ids):
            if I[t_idx, :].sum() == 0 and O[t_idx, :].sum() == 0:
                raise ValueError(f"Transition '{tid}' has no incident arcs")

        # ---------------------------
        # 9) Tạo object PetriNet đầy đủ
        # ---------------------------
        return cls(
            place_ids=place_ids,
            trans_ids=trans_ids,
            place_names=place_names,
            trans_names=trans_names,
            I=I,
            O=O,
            M0=M0,
        )


